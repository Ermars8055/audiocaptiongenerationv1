FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    libsndfile1 \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY video_captioner.py .

# Set environment variables for better compatibility
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "video_captioner.py"]
