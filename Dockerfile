# Use python 3.11 as specified in your original Dockerfile
FROM python:3.11-slim-bookworm

# Install system dependencies for port scanning, sniffing, and git operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    git \
    libpcap0.8 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set environment variables for the app and modules
ENV PYTHONPATH=/app/src
ENV PORT=7860

# Hugging Face Spaces require port 7860
EXPOSE 7860

# Run the web interface
CMD ["python", "web/app.py"]
