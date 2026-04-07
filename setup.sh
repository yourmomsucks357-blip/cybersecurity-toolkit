#!/bin/bash
echo "=== JEFE TOOLKIT SETUP ==="
git clone https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git
cd cybersecurity-toolkit
pip install -r requirements.txt
echo "=== SETUP COMPLETE ==="
echo "Set your keys:"
echo "  export GITHUB_TOKEN=your_token"
echo "  export NEWSAPI_KEY=your_key"
echo "  export ANTHROPIC_API_KEY=your_key"
echo ""
echo "Run: python src/main.py -t TARGET_IP"

