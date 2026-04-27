FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap git libpcap0.8 wget && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Required to pull private repos during build
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

COPY . .

# Securely clone private brains
RUN git clone https://Cunt1257:${HF_TOKEN}@github.com/yourmomsucks357-blip/gangster.git /app/models/gangster
RUN git clone https://Cunt1257:${HF_TOKEN}@github.com/yourmomsucks357-blip/fah-qu1257.git /app/src/fah_qu

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/src:/app/src/fah_qu:$PYTHONPATH
ENV PORT=7860
EXPOSE 7860

CMD ["python", "web/app.py"]
