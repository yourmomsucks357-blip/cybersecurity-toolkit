from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

OLLAMA_URL = "https://kurt-ago-james-expansys.trycloudflare.com/v1/chat/completions"
OLLAMA_TOKEN = "YOUR_VAST_TOKEN"
ANTHROPIC_KEY = "YOUR_ANTHROPIC_KEY"

def query_dolphin(prompt):
    r = requests.post(OLLAMA_URL, json={
        "model": "dolphin3",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }, headers={"Authorization": f"Bearer {OLLAMA_TOKEN}", "Content-Type": "application/json"})
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]
    return f"Dolphin error: {r.status_code}"

def query_claude(prompt):
    r = requests.post("https://api.anthropic.com/v1/messages", json={
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }, headers={
        "x-api-key": ANTHROPIC_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    })
    if r.status_code == 200:
        return r.json()["content"][0]["text"]
    return f"Claude error: {r.status_code}"

@app.route("/dolphin", methods=["POST"])
def dolphin_endpoint():
    prompt = request.json.get("prompt", "")
    return jsonify({"response": query_dolphin(prompt)})

@app.route("/claude", methods=["POST"])
def claude_endpoint():
    prompt = request.json.get("prompt", "")
    return jsonify({"response": query_claude(prompt)})

@app.route("/both", methods=["POST"])
def both_endpoint():
    prompt = request.json.get("prompt", "")
    return jsonify({
        "dolphin": query_dolphin(prompt),
        "claude": query_claude(prompt)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

