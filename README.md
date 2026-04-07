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

## Run on Vast.ai
You now have two paths:

### Option 1: Startup script on a standard Vast.ai instance
Use this when you launch an Ubuntu/Python image and want a single command to bootstrap everything.

```bash
git clone https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git
cd cybersecurity-toolkit
chmod +x scripts/vastai_start.sh
./scripts/vastai_start.sh
```

The script will:
- install system deps (`python3`, `pip`, `nmap`, `wget`)
- install Python deps from `requirements.txt`
- start `web/launch.py` (which also creates a Cloudflare public URL)

Optional env vars before start:
```bash
export NEWSAPI_KEY=your_key
export ANTHROPIC_API_KEY=your_key
export GITHUB_TOKEN=your_token
```

### Option 2: Custom Docker image for Vast.ai
Build from `Dockerfile.vastai` and push to your registry, then use that image in Vast.ai.

```bash
docker build -f Dockerfile.vastai -t your-registry/cybersecurity-toolkit:vast .
docker push your-registry/cybersecurity-toolkit:vast
```

Container default command:
```bash
python web/launch.py
```

It exposes port `7860` internally and also prints a Cloudflare URL once tunnel startup is complete.

## Built by JP Donovan
