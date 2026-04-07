#!/usr/bin/env python3
"""Credential Testing Module"""
import requests
import urllib3
urllib3.disable_warnings()

class CredentialTester:
    def __init__(self, target):
        self.target = target if target.startswith("http") else f"http://{target}"
        self.results = {"target": self.target, "findings": []}
        self.default_creds = [
            ("admin","admin"),("admin","password"),("admin","123456"),
            ("root","root"),("root","toor"),("root","password"),
            ("user","user"),("test","test"),("guest","guest"),
            ("admin",""),("administrator","administrator")
        ]

    def test_http_auth(self):
        paths = ["/admin","/login","/manager","/phpmyadmin"]
        for path in paths:
            url = self.target + path
            for user, pwd in self.default_creds:
                try:
                    r = requests.get(url, auth=(user,pwd), verify=False, timeout=3)
                    if r.status_code == 200:
                        finding = {"type":"default_creds","path":path,"username":user,"password":pwd,"severity":"critical"}
                        self.results["findings"].append(finding)
                        print(f"  [!!!] DEFAULT CREDS WORK: {path} - {user}:{pwd}")
                except:
                    pass

    def test_ssh(self):
        try:
            import paramiko
            ip = self.target.replace("http://","").replace("https://","").split(":")[0]
            for user, pwd in self.default_creds:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip, port=22, username=user, password=pwd, timeout=3)
                    finding = {"type":"ssh_default_creds","username":user,"password":pwd,"severity":"critical"}
                    self.results["findings"].append(finding)
                    print(f"  [!!!] SSH DEFAULT CREDS: {user}:{pwd}")
                    ssh.close()
                except:
                    pass
        except ImportError:
            print("  [-] paramiko not installed, skipping SSH test")

    def run(self):
        print(f"  [*] Testing credentials on {self.target}...")
        self.test_http_auth()
        self.test_ssh()
        return self.results

