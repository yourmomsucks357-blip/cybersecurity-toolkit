import os, subprocess

def push_to_github():
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("Set GITHUB_TOKEN environment variable first")
        return
    remote = f"https://{token}@github.com/yourmomsucks357-blip/cybersecurity-toolkit.git"
    subprocess.run(["git", "remote", "set-url", "origin", remote])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "auto deploy"])
    subprocess.run(["git", "push", "origin", "main"])
    print("Pushed to GitHub.")

if __name__ == "__main__":
    push_to_github()

