#!/usr/bin/env python3
"""Web Application Scanner Module"""
import requests
import urllib3
urllib3.disable_warnings()

class WebScanner:
    def __init__(self, target):
        self.target = target if target.startswith("http") else f"http://{target}"
        self.results = {"target": self.target, "findings": []}

    def check_headers(self):
        try:
            r = requests.get(self.target, verify=False, timeout=5)
            headers = dict(r.headers)
            security_headers = ["X-Frame-Options","X-Content-Type-Options","Strict-Transport-Security","Content-Security-Policy","X-XSS-Protection"]
            for h in security_headers:
                if h not in headers:
                    finding = {"type":"missing_header","header":h,"severity":"medium","detail":f"Missing {h} header"}
                    self.results["findings"].append(finding)
                    print(f"  [!] Missing header: {h}")
            self.results["status_code"] = r.status_code
            self.results["server"] = headers.get("Server","Unknown")
            print(f"  [+] Server: {self.results[\"server\"]}")
        except Exception as e:
            self.results["error"] = str(e)

    def check_common_paths(self):
        paths = ["/admin","/login","/wp-admin","/phpmyadmin","/.env","/.git/config","/robots.txt","/sitemap.xml","/api","/swagger","/graphql","/.well-known/security.txt"]
        for path in paths:
            try:
                r = requests.get(self.target + path, verify=False, timeout=3, allow_redirects=False)
                if r.status_code < 400:
                    finding = {"type":"exposed_path","path":path,"status":r.status_code,"severity":"high" if path in ["/.env","/.git/config"] else "info"}
                    self.results["findings"].append(finding)
                    print(f"  [!] Found: {path} ({r.status_code})")
            except:
                pass

    def check_ssl(self):
        if self.target.startswith("https"):
            try:
                r = requests.get(self.target, verify=True, timeout=5)
                self.results["ssl_valid"] = True
            except requests.exceptions.SSLError:
                self.results["ssl_valid"] = False
                self.results["findings"].append({"type":"ssl_issue","severity":"high","detail":"Invalid SSL certificate"})
                print("  [!] Invalid SSL certificate")

    def run(self):
        print(f"  [*] Scanning {self.target}...")
        self.check_headers()
        self.check_common_paths()
        self.check_ssl()
        return self.results

