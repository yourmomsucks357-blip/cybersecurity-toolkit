FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget curl nmap net-tools iputils-ping dnsutils openssh-client \
    libpcap-dev tcpdump \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/cybersecurity-toolkit

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt flask

COPY . .

ENV PYTHONPATH="/workspace/cybersecurity-toolkit/src:${PYTHONPATH}"

EXPOSE 7860

CMD ["python", "web/app.py"]
