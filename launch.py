import os, sys, subprocess, time

os.chdir("/cybersecurity-toolkit")
subprocess.run(["git", "pull", "origin", "main"])
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "flask"])

os.environ["PYTHONPATH"] = os.path.join(os.getcwd(), "src") + ":" + os.environ.get("PYTHONPATH", "")

subprocess.run(["wget", "-q", "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", "-O", "./cloudflared"])
os.chmod("./cloudflared", 0o755)

print("[*] Starting PUSSY MAGNET...")
subprocess.Popen([sys.executable, "web/app.py"])
time.sleep(3)

print("[*] Starting tunnel... look for the trycloudflare.com URL below:")
subprocess.run(["./cloudflared", "tunnel", "--url", "http://localhost:7860"])
