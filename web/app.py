from flask import Flask, render_template_string, request, jsonify
import subprocess, sys, os, json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PUSSY MAGNET</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#d4af37;font-family:monospace;min-height:100vh}
h1{text-align:center;padding:20px;font-size:28px;letter-spacing:6px;text-shadow:0 0 10px #d4af37}
h2{text-align:center;color:#888;font-size:12px;margin-bottom:20px}
.tools{display:flex;flex-wrap:wrap;gap:10px;padding:15px;justify-content:center}
.btn{background:#1a1a1a;color:#d4af37;border:1px solid #d4af37;padding:15px 20px;font-family:monospace;font-size:14px;border-radius:6px;cursor:pointer;min-width:140px;text-align:center}
.btn:active{background:#d4af37;color:#000}
.input-row{display:flex;gap:8px;padding:0 15px 15px;max-width:500px;margin:0 auto}
.input-row input{flex:1;background:#1a1a1a;color:#d4af37;border:1px solid #333;padding:12px;font-family:monospace;font-size:16px;border-radius:4px}
#results{margin:15px;padding:15px;background:#111;border:1px solid #333;border-radius:6px;white-space:pre-wrap;font-size:13px;color:#00ff41;min-height:100px;max-height:60vh;overflow-y:auto}
#status{text-align:center;color:#ff3333;font-size:12px;padding:5px}
</style>
</head>
<body>
<h1>PUSSY MAGNET</h1>
<h2>Built by JP Donovan</h2>
<div class="input-row">
<input id="target" placeholder="Target IP or URL">
</div>
<div class="tools">
<div class="btn" onclick="run('web')">Web Scanner</div>
<div class="btn" onclick="run('recon')">Network Recon</div>
<div class="btn" onclick="run('ports')">Port Scanner</div>
<div class="btn" onclick="run('creds')">Cred Tester</div>
<div class="btn" onclick="run('nmap')">Nmap Scan</div>
<div class="btn" onclick="run('sniff')">Sniffer</div>
<div class="btn" onclick="run('news')">News</div>
<div class="btn" onclick="run('ssh')">SSH Tool</div>
</div>
<div id="status"></div>
<div id="results">Ready. Enter a target and tap a tool.</div>
<script>
function run(tool){
var t=document.getElementById("target").value;
if(!t&&tool!="news"){document.getElementById("status").textContent="Enter a target first";return}
document.getElementById("status").textContent="Running "+tool+"...";
document.getElementById("results").textContent="Working...";
fetch("/run",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({tool:tool,target:t})})
.then(function(r){return r.json()})
.then(function(d){document.getElementById("results").textContent=d.output||d.error;document.getElementById("status").textContent="Done"})
.catch(function(e){document.getElementById("results").textContent="Error: "+e;document.getElementById("status").textContent="Failed"})
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/run", methods=["POST"])
def run_tool():
    data = request.json
    tool = data.get("tool", "")
    target = data.get("target", "")
    
    try:
        if tool == "web":
            from web_scanner import WebScanner
            result = WebScanner(target).run()
            return jsonify({"output": json.dumps(result, indent=2)})
        
        elif tool == "recon":
            from recon import NetworkRecon
            result = NetworkRecon(target).run()
            return jsonify({"output": json.dumps(result, indent=2)})
        
        elif tool == "ports":
            from port_scanner import scan_ports
            result = scan_ports(target)
            return jsonify({"output": json.dumps(result, indent=2)})
        
        elif tool == "creds":
            from credential_tester import CredentialTester
            result = CredentialTester(target).run()
            return jsonify({"output": json.dumps(result, indent=2)})
        
        elif tool == "nmap":
            r = subprocess.run([sys.executable, os.path.join("..", "src", "nmap_scanner.py"), target], capture_output=True, text=True, timeout=60)
            return jsonify({"output": r.stdout + r.stderr})
        
        elif tool == "sniff":
            from network_sniffer import NetworkSniffer
            result = NetworkSniffer(count=20).run()
            return jsonify({"output": json.dumps(result, indent=2)})
        
        elif tool == "news":
            import requests as req
            key = os.environ.get("NEWSAPI_KEY", "")
            if not key:
                return jsonify({"output": "Set NEWSAPI_KEY env var first"})
            r = req.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}")
            titles = [a["title"] for a in r.json().get("articles", [])]
            return jsonify({"output": "\n".join(titles)})
        
        elif tool == "ssh":
            return jsonify({"output": "SSH tool requires interactive terminal. Use Jupyter or command line."})
        
        else:
            return jsonify({"error": "Unknown tool"})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)
