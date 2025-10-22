# Use Python 3.11 slim image (better compatibility with PyTorch)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port 8000 (Azure Web Apps default)
EXPOSE 8000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Run the application with gunicorn for production
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 app:app
