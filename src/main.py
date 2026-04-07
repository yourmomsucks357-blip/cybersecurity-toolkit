#!/usr/bin/env python3
"""JEFE Cybersecurity Toolkit - Main Entry Point"""
import argparse
import sys
from recon import NetworkRecon
from web_scanner import WebScanner
from credential_tester import CredentialTester
from report_generator import ReportGenerator

def banner():
    print("""
     ██╗███████╗███████╗███████╗
     ██║██╔════╝██╔════╝██╔════╝
     ██║█████╗  █████╗  █████╗  
██   ██║██╔══╝  ██╔══╝  ██╔══╝  
╚█████╔╝███████╗██║     ███████╗
 ╚════╝ ╚══════╝╚═╝     ╚══════╝
    Cybersecurity Toolkit v1.0
    """)

def main():
    banner()
    parser = argparse.ArgumentParser(description="JEFE Security Toolkit")
    parser.add_argument("--target", "-t", required=True, help="Target IP or domain")
    parser.add_argument("--module", "-m", choices=["recon","web","creds","full"], default="full", help="Module to run")
    parser.add_argument("--output", "-o", default="results/report.json", help="Output file")
    args = parser.parse_args()

    print(f"[*] Target: {args.target}")
    print(f"[*] Module: {args.module}")

    results = {}

    if args.module in ["recon", "full"]:
        print("[+] Running Network Reconnaissance...")
        recon = NetworkRecon(args.target)
        results["recon"] = recon.run()

    if args.module in ["web", "full"]:
        print("[+] Running Web Scanner...")
        scanner = WebScanner(args.target)
        results["web"] = scanner.run()

    if args.module in ["creds", "full"]:
        print("[+] Running Credential Tester...")
        tester = CredentialTester(args.target)
        results["creds"] = tester.run()

    report = ReportGenerator(results, args.output)
    report.generate()
    print(f"[+] Report saved to {args.output}")

if __name__ == "__main__":
    main()

