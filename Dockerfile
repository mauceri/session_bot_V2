FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    libssl-dev \
    pkg-config \
    libsodium-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Create volumes directories
RUN mkdir -p /data /plugins

# Set environment variables
ENV PYTHONPATH=/app
ENV DATA_DIR=/data
ENV PLUGINS_DIR=/plugins

# Run the application
CMD ["python", "-m", "core.main"]
