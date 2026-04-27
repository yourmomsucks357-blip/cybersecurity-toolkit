# PUSSY MAGNET Integrated Build
FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap git libpcap0.8 wget && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy primary toolkit
COPY . .

# Pull in the gangster model and fah-qu logic
RUN git clone https://github.com/yourmomsucks357-blip/gangster.git /app/models/gangster
RUN git clone https://github.com/yourmomsucks357-blip/fah-qu1257.git /app/src/fah_qu

# Final dependency install
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/src:/app/src/fah_qu:$PYTHONPATH
ENV PORT=7860
EXPOSE 7860

CMD ["python", "web/app.py"]
