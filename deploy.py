import os, subprocess, sys

def deploy(target):
    repo = "https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git"
    if not os.path.exists("cybersecurity-toolkit"):
        subprocess.run(["git", "clone", repo])
    else:
        subprocess.run(["git", "-C", "cybersecurity-toolkit", "pull"])
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "cybersecurity-toolkit/requirements.txt"])
    subprocess.run([sys.executable, "cybersecurity-toolkit/src/main.py", "-t", target])

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else input("Target IP: ")
    deploy(target)

