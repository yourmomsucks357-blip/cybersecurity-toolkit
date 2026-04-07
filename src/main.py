import argparse, sys

def banner():
    print("""
    PUSSY MAGNET v1.0
    =================
    Built by JP Donovan
    """)

def main():
    banner()
    parser = argparse.ArgumentParser(description="PUSSY MAGNET")
    parser.add_argument("--target", "-t", required=True)
    parser.add_argument("--module", "-m", choices=["recon","web","creds","scan","full"], default="full")
    parser.add_argument("--output", "-o", default="results/report.json")
    args = parser.parse_args()
    print(f"[*] Target: {args.target}")
    print(f"[*] Module: {args.module}")
    results = {}
    if args.module in ["recon", "full"]:
        from recon import NetworkRecon
        results["recon"] = NetworkRecon(args.target).run()
    if args.module in ["web", "full"]:
        from web_scanner import WebScanner
        results["web"] = WebScanner(args.target).run()
    if args.module in ["creds", "full"]:
        from credential_tester import CredentialTester
        results["creds"] = CredentialTester(args.target).run()
    if args.module in ["scan", "full"]:
        from port_scanner import scan_ports
        results["scan"] = scan_ports(args.target)
    from report_generator import ReportGenerator
    ReportGenerator(results, args.output).generate()
    print(f"[+] Report: {args.output}")

if __name__ == "__main__":
    main()
