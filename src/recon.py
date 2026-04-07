#!/usr/bin/env python3
"""Network Reconnaissance Module"""
import socket
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

class NetworkRecon:
    def __init__(self, target):
        self.target = target
        self.results = {"target": target, "ports": [], "services": [], "banners": []}

    def resolve_target(self):
        try:
            ip = socket.gethostbyname(self.target)
            self.results["ip"] = ip
            print(f"  [+] Resolved {self.target} -> {ip}")
            return ip
        except socket.gaierror:
            self.results["ip"] = self.target
            return self.target

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.results["ip"], port))
            if result == 0:
                banner = self.grab_banner(sock, port)
                self.results["ports"].append(port)
                self.results["banners"].append({"port": port, "banner": banner})
                print(f"  [+] Port {port} OPEN - {banner}")
            sock.close()
        except:
            pass

    def grab_banner(self, sock, port):
        try:
            sock.send(b"HEAD / HTTP/1.1\r\n\r\n")
            return sock.recv(1024).decode(errors="ignore").strip()[:200]
        except:
            return "No banner"

    def port_scan(self, ports=None):
        if ports is None:
            ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,1521,3306,3389,5432,5900,8080,8443,8888,9090]
        target_ip = self.results.get("ip", self.target)
        print(f"  [*] Scanning {len(ports)} ports on {target_ip}...")
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(self.scan_port, ports)

    def detect_services(self):
        service_map = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",135:"RPC",139:"NetBIOS",143:"IMAP",443:"HTTPS",445:"SMB",993:"IMAPS",995:"POP3S",1433:"MSSQL",1521:"Oracle",3306:"MySQL",3389:"RDP",5432:"PostgreSQL",5900:"VNC",8080:"HTTP-Proxy",8443:"HTTPS-Alt",8888:"HTTP-Alt",9090:"Web-Admin"}
        for port in self.results["ports"]:
            service = service_map.get(port, "Unknown")
            self.results["services"].append({"port": port, "service": service})

    def run(self):
        self.resolve_target()
        self.port_scan()
        self.detect_services()
        return self.results

