#!/usr/bin/env bash
set -euo pipefail

# Optional overrides:
# - VAST_REPO_URL: repository to clone when code is not already present
# - VAST_REPO_DIR: destination path for cloned repository
REPO_URL="${VAST_REPO_URL:-https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git}"
REPO_DIR="${VAST_REPO_DIR:-/workspace/cybersecurity-toolkit}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -f "${SCRIPT_DIR}/../go.py" ]]; then
  REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
fi

if command -v apt-get >/dev/null 2>&1; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    nmap \
    python3 \
    python3-pip \
    wget
  rm -rf /var/lib/apt/lists/*
fi

if [[ ! -d "${REPO_DIR}/.git" ]]; then
  git clone "${REPO_URL}" "${REPO_DIR}"
else
  git -C "${REPO_DIR}" pull --ff-only origin main || true
fi

python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir -r "${REPO_DIR}/requirements.txt" flask

cd "${REPO_DIR}"
exec python3 web/launch.py
