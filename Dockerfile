# PUSSY MAGNET — run on Vast.ai (Entrypoint) or any Docker host.
# Template: expose port 7860, e.g. Docker options: -p 7860:7860
# For raw packet tools (port scan / sniffer), add capability: --cap-add=NET_RAW --cap-add=NET_ADMIN
FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    git \
    libpcap0.8 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app/src

EXPOSE 7860

CMD ["python", "web/app.py"]
