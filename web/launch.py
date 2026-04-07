import subprocess, sys, os, time, threading, re

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.getcwd(), "src"))

# Download cloudflared
if not os.path.exists("/tmp/cf"):
    print("[*] Downloading tunnel...")
    subprocess.run(["wget","-q","https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64","-O","/tmp/cf"])
    subprocess.run(["chmod","+x","/tmp/cf"])

# Start tunnel in background thread
tunnel_url = []
def run_tunnel():
    p = subprocess.Popen(["/tmp/cf","tunnel","--url","http://localhost:7860"], stderr=subprocess.PIPE, text=True)
    for line in p.stderr:
        m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
        if m:
            tunnel_url.append(m.group(0))
            print(f"\n{'='*50}")
            print(f"PUSSY MAGNET IS LIVE AT:")
            print(f"{m.group(0)}")
            print(f"{'='*50}\n")

t = threading.Thread(target=run_tunnel, daemon=True)
t.start()

# Start Flask
print("[*] Starting PUSSY MAGNET web interface...")
time.sleep(2)

from web.app import app
app.run(host="0.0.0.0", port=7860, debug=False)
