#!/bin/bash
set -eo pipefail

REPO_URL="https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git"
INSTALL_DIR="/workspace/cybersecurity-toolkit"

if [ -d "$INSTALL_DIR/.git" ]; then
    echo "[*] Updating toolkit..."
    git -C "$INSTALL_DIR" pull origin main
else
    echo "[*] Cloning toolkit..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"
pip install -q -r requirements.txt flask

export PYTHONPATH="$INSTALL_DIR/src:$PYTHONPATH"
env | grep _ >> /etc/environment

echo "[*] Starting PUSSY MAGNET on port 7860..."
nohup python web/app.py > /var/log/pussy_magnet.log 2>&1 &

echo "[*] PUSSY MAGNET is running on port 7860"
echo "[*] Use the Vast.ai instance IP and mapped port to access the web UI"
