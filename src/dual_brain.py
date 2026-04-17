from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/v1/chat/completions")

def query(model, prompt):
    r = requests.post(OLLAMA_URL, json={"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}, headers={"Content-Type": "application/json"})
    return r.json()["choices"][0]["message"]["content"] if r.status_code == 200 else f"Error {r.status_code}"

@app.route("/dolphin", methods=["POST"])
def dolphin(): return jsonify({"response": query("dolphin3", request.json.get("prompt", ""))})

@app.route("/llama", methods=["POST"])
def llama(): return jsonify({"response": query("artifish/llama3.2-uncensored", request.json.get("prompt", ""))})

@app.route("/both", methods=["POST"])
def both():
    p = request.json.get("prompt", "")
    return jsonify({"dolphin": query("dolphin3", p), "llama": query("artifish/llama3.2-uncensored", p)})

if __name__=="__main__": app.run(host="0.0.0.0", port=5000, debug=True)

