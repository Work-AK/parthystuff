# ------------------------
# Base Image
# ------------------------
FROM python:3.12-slim

# ------------------------
# Set environment variables
# ------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ------------------------
# Set working directory
# ------------------------
WORKDIR /app

# ------------------------
# Copy application files
# ------------------------
COPY app.py /app/app.py

# ------------------------
# Install dependencies
# ------------------------
RUN pip install --no-cache-dir Flask==3.3.2

# ------------------------
# Expose port
# ------------------------
EXPOSE 8080

# ------------------------
# Run the app
# ------------------------
CMD ["python", "app.py"]
