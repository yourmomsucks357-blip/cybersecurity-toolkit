from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
OLLAMA_URL = "REPLACE_WITH_TUNNEL_URL/v1/chat/completions"
OLLAMA_TOKEN = "REPLACE_WITH_TOKEN"
ANTHROPIC_KEY = "REPLACE_WITH_KEY"

def query_dolphin(prompt):
    r = requests.post(OLLAMA_URL, json={"model":"dolphin3","messages":[{"role":"user","content":prompt}],"stream":False}, headers={"Authorization":f"Bearer {OLLAMA_TOKEN}","Content-Type":"application/json"})
    return r.json()["choices"][0]["message"]["content"] if r.status_code==200 else f"Error {r.status_code}"

def query_claude(prompt):
    r = requests.post("https://api.anthropic.com/v1/messages", json={"model":"claude-sonnet-4-20250514","max_tokens":1024,"messages":[{"role":"user","content":prompt}]}, headers={"x-api-key":ANTHROPIC_KEY,"anthropic-version":"2023-06-01","Content-Type":"application/json"})
    return r.json()["content"][0]["text"] if r.status_code==200 else f"Error {r.status_code}"

@app.route("/dolphin", methods=["POST"])
def dolphin(): return jsonify({"response":query_dolphin(request.json.get("prompt",""))})

@app.route("/claude", methods=["POST"])
def claude(): return jsonify({"response":query_claude(request.json.get("prompt",""))})

@app.route("/both", methods=["POST"])
def both():
    p=request.json.get("prompt","")
    return jsonify({"dolphin":query_dolphin(p),"claude":query_claude(p)})

if __name__=="__main__": app.run(host="0.0.0.0",port=5000,debug=True)

