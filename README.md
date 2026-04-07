# PUSSY MAGNET

Offensive security toolkit. Built from a phone in Florida.

## Run It
```
python go.py
```

## Vast.ai Server

The easiest way to run the web UI on a Vast.ai instance is to expose port `7860`
and start the Flask app in Docker.

### Option 1: Docker on Vast.ai

Build the image on the instance:

```bash
docker build -t pussy-magnet-vast .
```

Run it and publish the web port:

```bash
docker run --rm -p 7860:7860 --env-file .env pussy-magnet-vast
```

Then expose TCP port `7860` in the Vast.ai instance settings and open:

```text
http://<your-instance-ip>:7860
```

### Option 2: Run directly on the server

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo apt-get update && sudo apt-get install -y nmap
./start_vast.sh
```

### Environment variables

The web server reads `.env` automatically if present. Useful values:

```bash
HOST=0.0.0.0
PORT=7860
NEWSAPI_KEY=your_key
ANTHROPIC_API_KEY=your_key
GITHUB_TOKEN=your_token
```

### Notes for Vast.ai

- `nmap` is installed in the Docker image; install it manually if you use the
  direct server setup.
- The packet sniffer may require running as root or adding container
  capabilities such as `NET_ADMIN` and `NET_RAW`.
- The Flask app now binds to `HOST` and `PORT`, so you can change the listening
  port if your Vast.ai template expects a different one.

## Modules
- Port Scanner - SYN scan 1-1000
- Network Recon - banner grab, service detection
- Web Scanner - headers, paths, SSL
- Credential Tester - default cred attacks
- Network Sniffer - packet capture
- News Headlines - OSINT news feed
- Dual Brain - Dolphin (uncensored) + Claude (legal/research)

## Setup
```
git clone https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git
cd cybersecurity-toolkit
python go.py
```

## Built by JP Donovan
