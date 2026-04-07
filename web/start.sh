#!/bin/bash
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/src:$PYTHONPATH"
cd web
pip install -q flask
python app.py
