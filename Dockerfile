FROM python:3.12-slim

WORKDIR /app

# Install ffmpeg for audio processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Command will be overridden in docker-compose.yml
CMD ["python", "-m", "api.main"]