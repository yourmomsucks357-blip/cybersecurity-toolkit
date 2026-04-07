import requests
import base64

class GitHubDeployer:
    def __init__(self, token, username="yourmomsucks357-blip"):
        self.token = token
        self.username = username
        self.headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}

    def create_repo(self, repo_name, description="", private=False):
        r = requests.post("https://api.github.com/user/repos", json={"name": repo_name, "description": description, "auto_init": True, "private": private}, headers=self.headers)
        print(f"Repo {repo_name}: {r.status_code}")
        return r.status_code == 201

    def push_file(self, repo, filepath, content, message="auto deploy"):
        url = f"https://api.github.com/repos/{self.username}/{repo}/contents/{filepath}"
        encoded = base64.b64encode(content.encode()).decode()
        r = requests.get(url, headers=self.headers)
        payload = {"message": message, "content": encoded}
        if r.status_code == 200:
            payload["sha"] = r.json()["sha"]
        r = requests.put(url, json=payload, headers=self.headers)
        status = "Updated" if r.status_code == 200 else "Created" if r.status_code == 201 else f"Error {r.status_code}"
        print(f"{status}: {filepath}")
        return r.status_code in [200, 201]

    def delete_file(self, repo, filepath, message="delete"):
        url = f"https://api.github.com/repos/{self.username}/{repo}/contents/{filepath}"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            requests.delete(url, json={"message": message, "sha": r.json()["sha"]}, headers=self.headers)
            print(f"Deleted: {filepath}")

    def list_files(self, repo, path=""):
        r = requests.get(f"https://api.github.com/repos/{self.username}/{repo}/contents/{path}", headers=self.headers)
        return [f["name"] for f in r.json()] if r.status_code == 200 else []

if __name__ == "__main__":
    import sys
    token = sys.argv[1] if len(sys.argv) > 1 else input("Token: ")
    d = GitHubDeployer(token)
    print("Ready. Use d.push_file() or d.create_repo()")

