#!/bin/bash
set -e

usage() {
    echo "Deploy PUSSY MAGNET to a Vast.ai instance"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --api-key KEY      Vast.ai API key (or set VASTAI_API_KEY env var)"
    echo "  --gpu-type TYPE    GPU type filter, e.g. 'RTX_3090' (default: any)"
    echo "  --max-price PRICE  Max price per hour in \$/hr (default: 0.50)"
    echo "  --disk DISK        Disk space in GB (default: 20)"
    echo "  --help             Show this help message"
    echo ""
    echo "Requirements: pip install vastai"
    exit 0
}

API_KEY="${VASTAI_API_KEY:-}"
GPU_TYPE=""
MAX_PRICE="0.50"
DISK="20"

while [[ $# -gt 0 ]]; do
    case $1 in
        --api-key)   API_KEY="$2"; shift 2 ;;
        --gpu-type)  GPU_TYPE="$2"; shift 2 ;;
        --max-price) MAX_PRICE="$2"; shift 2 ;;
        --disk)      DISK="$2"; shift 2 ;;
        --help)      usage ;;
        *)           echo "Unknown option: $1"; usage ;;
    esac
done

if [ -z "$API_KEY" ]; then
    echo "Error: Vast.ai API key required. Use --api-key or set VASTAI_API_KEY"
    exit 1
fi

if ! command -v vastai &> /dev/null; then
    echo "[*] Installing vastai CLI..."
    pip install vastai
fi

vastai set api-key "$API_KEY"

ONSTART_CMD=$(cat <<'SCRIPT'
apt-get update && apt-get install -y git nmap net-tools iputils-ping dnsutils openssh-client libpcap-dev tcpdump;
cd /workspace;
git clone https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git || git -C cybersecurity-toolkit pull;
cd cybersecurity-toolkit;
pip install -r requirements.txt flask;
export PYTHONPATH="/workspace/cybersecurity-toolkit/src:$PYTHONPATH";
env | grep _ >> /etc/environment;
nohup python web/app.py > /var/log/pussy_magnet.log 2>&1 &
SCRIPT
)

echo "[*] Searching for available instances..."

QUERY="reliability>0.95 inet_down>100 disk_space>=${DISK}"
if [ -n "$GPU_TYPE" ]; then
    QUERY="$QUERY gpu_name=$GPU_TYPE"
fi
QUERY="$QUERY dph<=$MAX_PRICE"

echo "[*] Query: $QUERY"
echo ""
vastai search offers "$QUERY" --order "dph" --limit 10

echo ""
echo "To create an instance, run:"
echo ""
echo "  vastai create instance <OFFER_ID> \\"
echo "    --image python:3.11-slim \\"
echo "    --disk $DISK \\"
echo "    --ssh \\"
echo "    --direct \\"
echo "    --env '-p 7860:7860' \\"
echo "    --onstart-cmd '<onstart commands>'"
echo ""
echo "Or use the pre-built Docker image (if pushed to a registry):"
echo ""
echo "  vastai create instance <OFFER_ID> \\"
echo "    --image <your-dockerhub-user>/pussy-magnet:latest \\"
echo "    --disk $DISK \\"
echo "    --ssh \\"
echo "    --direct \\"
echo "    --env '-p 7860:7860'"
