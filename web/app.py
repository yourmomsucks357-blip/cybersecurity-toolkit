from flask import Flask, render_template_string, request, jsonify
import subprocess, sys, os, json
from llama_cpp import Llama

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
app = Flask(__name__)

# Fixed path to look inside the cloned 'gangster' folder
MODEL_PATH = "/app/models/gangster/gangster_model.gguf"
local_brain = Llama(model_path=MODEL_PATH) if os.path.exists(MODEL_PATH) else None

try:
    from fah_qu import vision_logic
except ImportError:
    vision_logic = None

# ... (Keep your existing HTML variable here) ...

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/run", methods=["POST"])
def run_tool():
    data = request.json
    tool, target = data.get("tool", ""), data.get("target", "")
    try:
        if tool == "dual_brain":
            return jsonify({
                "gangster_local": local_brain(target)["choices"][0]["text"] if local_brain else "Model Offline",
                "fah_qu_uncensored": vision_logic.query(target) if vision_logic else "Module Offline"
            })
        # ... (Keep your other tool routes) ...
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
