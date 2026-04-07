from flask import Flask, request, render_template_string, send_from_directory, jsonify
import os

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Video Drop</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#d4af37;font-family:monospace;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}
h1{font-size:32px;letter-spacing:4px;margin-bottom:10px;text-shadow:0 0 10px #d4af37}
h2{color:#888;font-size:14px;margin-bottom:30px}
.drop{width:90%;max-width:400px;border:2px dashed #d4af37;border-radius:12px;padding:40px 20px;text-align:center;cursor:pointer}
.drop:active{background:#1a1a0a}
.drop p{font-size:16px;margin-bottom:10px}
.drop small{color:#888;font-size:12px}
input[type=file]{display:none}
#status{margin-top:20px;font-size:14px;color:#00ff41;min-height:20px}
#prog{width:90%;max-width:400px;height:6px;background:#1a1a1a;border-radius:3px;margin-top:10px;display:none}
#bar{height:100%;background:#d4af37;border-radius:3px;width:0%}
.files{margin-top:30px;width:90%;max-width:400px}
.f{background:#111;border:1px solid #333;padding:10px;margin:5px 0;border-radius:6px;font-size:12px;display:flex;justify-content:space-between}
.f a{color:#d4af37}
</style>
</head>
<body>
<h1>VIDEO DROP</h1>
<h2>Tap to upload or drag and drop</h2>
<div class="drop" id="drop" onclick="document.getElementById('fi').click()">
<p>Drop video here</p>
<small>MP4 MOV AVI MKV</small>
</div>
<input type="file" id="fi" accept="video/*" multiple>
<div id="prog"><div id="bar"></div></div>
<div id="status"></div>
<div class="files" id="files"></div>
<script>
var d=document.getElementById("drop"),fi=document.getElementById("fi"),st=document.getElementById("status"),bar=document.getElementById("bar"),prog=document.getElementById("prog");
d.ondragover=function(e){e.preventDefault()};
d.ondrop=function(e){e.preventDefault();up(e.dataTransfer.files)};
fi.onchange=function(){up(fi.files)};
function up(files){for(var i=0;i<files.length;i++){var f=files[i],fd=new FormData();fd.append("video",f);var x=new XMLHttpRequest();prog.style.display="block";x.upload.onprogress=function(e){if(e.lengthComputable)bar.style.width=(e.loaded/e.total*100)+"%"};x.onload=function(){st.textContent=x.status==200?"Uploaded!":"Failed";st.style.color=x.status==200?"#00ff41":"#ff3333";prog.style.display="none";bar.style.width="0%";lf()};x.open("POST","/upload");x.send(fd)}}
function lf(){fetch("/files").then(function(r){return r.json()}).then(function(d){var h="";for(var i=0;i<d.length;i++)h+="<div class=f>"+d[i].n+" ("+d[i].s+") <a href=/dl/"+encodeURIComponent(d[i].n)+">DL</a></div>";document.getElementById("files").innerHTML=h})}
lf();
</script>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("video")
    if not f or f.filename == "":
        return jsonify({"error": "No file"}), 400
    f.save(os.path.join(UPLOAD_DIR, f.filename))
    return jsonify({"ok": True})

@app.route("/files")
def list_files():
    files = []
    for name in os.listdir(UPLOAD_DIR):
        sz = os.path.getsize(os.path.join(UPLOAD_DIR, name))
        s = f"{sz/1048576:.1f} MB" if sz > 1048576 else f"{sz/1024:.1f} KB"
        files.append({"n": name, "s": s})
    return jsonify(files)

@app.route("/dl/<name>")
def dl(name):
    return send_from_directory(UPLOAD_DIR, name, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
