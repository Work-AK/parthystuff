from flask import Flask, render_template

app = Flask(__name__)

# In-memory "catalog" of YouTube videos
videos = [
    {"id": "dQw4w9WgXcQ", "title": "Classic Hit 🎵"},
    {"id": "3JZ_D3ELwOQ", "title": "Inspiring Speech"},
    {"id": "L_jWHffIx5E", "title": "Throwback Song"},
    {"id": "kJQP7kiw5Fk", "title": "World Hit 🌎"},
    {"id": "eVTXPUF4Oz4", "title": "Emotional Track"},
]

@app.route("/")
def index():
    return render_template("index.html", videos=videos)

@app.route("/watch/<video_id>")
def watch(video_id):
    video = next((v for v in videos if v["id"] == video_id), None)
    if not video:
        return "Video not found", 404
    return render_template("watch.html", video=video)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
