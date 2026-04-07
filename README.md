# PUSSY MAGNET

Offensive security toolkit. Built from a phone in Florida.

## Run It
```
python go.py
```

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

## Deploy on Vast.ai

Run PUSSY MAGNET on a Vast.ai GPU/CPU server for always-on access or heavy scanning.

### Option 1: Onstart Script (Easiest)

1. Go to [vast.ai](https://vast.ai) and pick a template (e.g. `python:3.11-slim` or `vastai/base-image`)
2. Set **Launch Mode** to **SSH**
3. Under **Docker Options**, add: `-p 7860:7860`
4. Paste this into the **On-start Script** box:

```
apt-get update && apt-get install -y git nmap net-tools iputils-ping dnsutils openssh-client libpcap-dev tcpdump;
cd /workspace;
git clone https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git || git -C cybersecurity-toolkit pull;
cd cybersecurity-toolkit;
pip install -r requirements.txt flask;
export PYTHONPATH="/workspace/cybersecurity-toolkit/src:$PYTHONPATH";
env | grep _ >> /etc/environment;
nohup python web/app.py > /var/log/pussy_magnet.log 2>&1 &
```

5. Set your API keys in **Environment Variables**:
   - `-e NEWSAPI_KEY=your_key -e ANTHROPIC_API_KEY=your_key`
6. Create the instance and connect via the mapped port 7860

### Option 2: Docker Image

Build and push the image, then use it as a Vast.ai template:

```bash
docker build -t yourdockerhubuser/pussy-magnet:latest .
docker push yourdockerhubuser/pussy-magnet:latest
```

On Vast.ai, set the image to `yourdockerhubuser/pussy-magnet:latest` and add `-p 7860:7860` to Docker Options.

### Option 3: CLI Deploy Helper

Use the included helper script to search for instances and get the deploy command:

```bash
pip install vastai
bash vast_deploy.sh --api-key YOUR_KEY --max-price 0.30 --disk 20
```

### Environment Variables

Set these in Vast.ai template environment or in a `.env` file:

| Variable | Purpose |
|---|---|
| `NEWSAPI_KEY` | News headlines OSINT feed |
| `ANTHROPIC_API_KEY` | Claude AI for Dual Brain |
| `GITHUB_TOKEN` | GitHub deploy tools |

## Built by JP Donovan
