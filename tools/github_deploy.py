import os
import base64
import requests

class GitHubDeployer:
    def __init__(self, token, username="yourmomsucks357-blip"):
        self.token = token
        self.username = username
        self.headers = {
            "Authorization": f"token {token}",
            "Content-Type": "application/json"
        }

    def create_repo(self, repo_name, description="", private=False):
        url = "https://api.github.com/user/repos"
        payload = {
            "name": repo_name,
            "description": description,
            "auto_init": True,
            "private": private
        }
        r = requests.post(url, json=payload, headers=self.headers)
        if r.status_code == 201:
            print(f"Repo {repo_name} created.")
            return True
        else:
            print(f"Failed: {r.status_code} {r.json().get(message,)}")
            return False

    def push_file(self, repo_name, filepath, content, message="auto push"):
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/contents/{filepath}"
        encoded = base64.b64encode(content.encode()).decode()
        
        # Check if file exists (need sha to update)
        r = requests.get(url, headers=self.headers)
        sha = r.json().get("sha", "") if r.status_code == 200 else ""
        
        payload = {"message": message, "content": encoded}
        if sha:
            payload["sha"] = sha
            
        r = requests.put(url, json=payload, headers=self.headers)
        if r.status_code in [200, 201]:
            print(f"Pushed {filepath}")
            return True
        else:
            print(f"Failed {filepath}: {r.status_code}")
            return False

    def push_directory(self, repo_name, file_dict, message="batch push"):
        for filepath, content in file_dict.items():
            self.push_file(repo_name, filepath, content, message)

    def delete_file(self, repo_name, filepath, message="delete"):
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/contents/{filepath}"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            sha = r.json()["sha"]
            payload = {"message": message, "sha": sha}
            requests.delete(url, json=payload, headers=self.headers)
            print(f"Deleted {filepath}")

    def list_files(self, repo_name, path=""):
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/contents/{path}"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return [f["name"] for f in r.json()]
        return []

if __name__ == "__main__":
    import sys
    token = sys.argv[1] if len(sys.argv) > 1 else input("GitHub token: ")
    deployer = GitHubDeployer(token)
    print("Deployer ready. Use deployer.push_file() or deployer.create_repo()")

