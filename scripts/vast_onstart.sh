#!/usr/bin/env bash
# Paste into Vast.ai template "On-start" (SSH or Jupyter), or run after SSH login.
# Prerequisites in Docker options: -p 7860:7860
# Optional: export API keys before start, e.g. -e ANTHROPIC_API_KEY=... -e NEWSAPI_KEY=...
# For sniffer/port-scan raw sockets, add Docker caps if your template allows it.
set -euo pipefail

REPO="${VAST_REPO_URL:-https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git}"
TARGET="${VAST_WORKDIR:-/workspace/cybersecurity-toolkit}"
export PYTHONPATH="${TARGET}/src:${PYTHONPATH:-}"

if [[ ! -d "${TARGET}/.git" ]]; then
  git clone "${REPO}" "${TARGET}"
else
  git -C "${TARGET}" pull --ff-only || true
fi

cd "${TARGET}"
PY=python3
command -v python3 >/dev/null || PY=python
"${PY}" -m pip install -q -r requirements.txt

# Make template env vars visible in SSH sessions (Vast.ai note).
if [[ -w /etc/environment ]]; then
  env | grep -E '^[A-Z_][A-Z0-9_]*=' >>/etc/environment 2>/dev/null || true
fi

# Install and start Ollama
curl -fsSL https://ollama.com/install.sh | sh
nohup ollama serve >>/tmp/ollama.log 2>&1 &
sleep 5
ollama pull dolphin3
ollama pull artifish/llama3.2-uncensored

export PORT="${PORT:-7860}"
nohup "${PY}" web/app.py >>/tmp/pussy-magnet-web.log 2>&1 &
echo "PUSSY MAGNET web starting on port ${PORT} (logs: /tmp/pussy-magnet-web.log)"
echo "Use the Vast instance card / portal to open the mapped URL for that port."
