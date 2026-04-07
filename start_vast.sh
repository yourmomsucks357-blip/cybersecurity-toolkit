#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
    PYTHON_BIN="python"
fi

export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-7860}"
export PYTHONPATH="${ROOT_DIR}/src:${PYTHONPATH:-}"

cd "${ROOT_DIR}"
exec "${PYTHON_BIN}" web/app.py
