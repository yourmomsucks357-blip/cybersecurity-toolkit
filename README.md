# PUSSY MAGNET



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

## Vast.ai

**Option A — Docker (Entrypoint)**  
Build and push an image from this repo (or use Vast’s “Custom Dockerfile”). Expose **7860**. Optional for raw scans: add capabilities `NET_RAW` and `NET_ADMIN`.

**Option B — SSH / Jupyter template**  
In Docker options add `-p 7860:7860`. In **On-start**, run the script from this repo (after clone) or paste the commands from `scripts/vast_onstart.sh`. Set `VAST_REPO_URL` if you use a fork. Optional: `-e ANTHROPIC_API_KEY=...` and `-e NEWSAPI_KEY=...`.

The web UI listens on `0.0.0.0`; use Vast’s instance portal / mapped port URL to open it.


