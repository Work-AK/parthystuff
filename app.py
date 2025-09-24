from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from datetime import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['DEBUG'] = True

# ------------------------
# Data Storage
# ------------------------
PARKING_SPOTS = [f"P{str(i).zfill(2)}" for i in range(1, 21)]  # 20 spots
TICKETS = []

# ------------------------
# Full HTML Template
# ------------------------
FULL_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Parking Ticket App</title>
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: #333;
        margin: 0;
        padding: 0;
    }
    .container {
        width: 90%;
        max-width: 900px;
        margin: auto;
        padding: 20px;
        background: #fff;
        margin-top: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    h1 {
        text-align: center;
        color: #333;
        margin-bottom: 30px;
    }
    .section-title {
        color: #2575fc;
        margin-bottom: 10px;
    }
    .spot, .ticket {
        background: #f7f9fc;
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 10px;
        border-left: 5px solid #2575fc;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .spot:hover, .ticket:hover {
        transform: scale(1.02);
    }
    form {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    select, button {
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #ccc;
        font-size: 1em;
    }
    button {
        background: #2575fc;
        color: white;
        border: none;
        cursor: pointer;
        transition: background 0.2s;
    }
    button:hover {
        background: #6a11cb;
    }
    @media (max-width: 600px) {
        form {
            flex-direction: column;
        }
        select, button {
            width: 100%;
            margin-bottom: 10px;
        }
    }
</style>
</head>
<body>
<div class="container">
<h1>🚗 Parking Ticket Management</h1>

<h2 class="section-title">Available Spots</h2>
{% if available_spots %}
<form method="post" action="{{ url_for('book') }}">
  <select name="spot">
    {% for spot in available_spots %}
      <option value="{{ spot }}">{{ spot }}</option>
    {% endfor %}
  </select>
  <button type="submit">Book Spot</button>
</form>
{% else %}
<p>All spots are currently booked!</p>
{% endif %}

<h2 class="section-title">Active Tickets</h2>
{% for ticket in tickets %}
<div class="ticket">
  <div>
    <strong>Ticket ID:</strong> {{ ticket['id'] }}<br>
    <strong>Spot:</strong> {{ ticket['spot'] }}<br>
    <strong>Time:</strong> {{ ticket['time'] }}
  </div>
</div>
{% else %}
<p>No active tickets.</p>
{% endfor %}

</div>
</body>
</html>
"""

# ------------------------
# Routes
# ------------------------
@app.route("/", methods=["GET"])
def index():
    booked_spots = [t["spot"] for t in TICKETS]
    available_spots = [s for s in PARKING_SPOTS if s not in booked_spots]
    return render_template_string(FULL_HTML, available_spots=available_spots, tickets=TICKETS)

@app.route("/book", methods=["POST"])
def book():
    spot = request.form.get("spot")
    if spot and spot in PARKING_SPOTS and spot not in [t["spot"] for t in TICKETS]:
        ticket = {
            "id": f"T{random.randint(1000,9999)}",
            "spot": spot,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        TICKETS.append(ticket)
    return redirect(url_for("index"))

# ------------------------
# API Endpoints
# ------------------------
@app.route("/api/spots")
def api_spots():
    booked_spots = [t["spot"] for t in TICKETS]
    available_spots = [s for s in PARKING_SPOTS if s not in booked_spots]
    return jsonify({"available": available_spots, "booked": booked_spots})

@app.route("/api/tickets")
def api_tickets():
    return jsonify(TICKETS)

# ------------------------
# Run App
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
