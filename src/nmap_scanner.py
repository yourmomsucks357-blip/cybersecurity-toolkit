import sys

try:
    import nmap
except ImportError:
    print("Installing python-nmap...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "python-nmap"])
    import nmap

def scan_host(host, ports="1-1000"):
    nm = nmap.PortScanner()
    print(f"[*] Scanning {host} ports {ports}...")
    nm.scan(host, ports)
    
    for h in nm.all_hosts():
        print(f"\nHost: {h} ({nm[h].hostname()})")
        print(f"State: {nm[h].state()}")
        
        for proto in nm[h].all_protocols():
            ports_list = nm[h][proto].keys()
            print(f"\nProtocol: {proto}")
            print(f"{'PORT':<10} {'STATE':<12} {'SERVICE'}")
            for port in sorted(ports_list):
                state = nm[h][proto][port]["state"]
                service = nm[h][proto][port]["name"]
                print(f"{port:<10} {state:<12} {service}")

def scan_range(ip_range, ports="1-1000"):
    nm = nmap.PortScanner()
    print(f"[*] Scanning range {ip_range}...")
    nm.scan(hosts=ip_range, ports=ports, arguments="-sV")
    
    for host in nm.all_hosts():
        scan_host(host, ports)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else input("Target IP or range: ")
    ports = sys.argv[2] if len(sys.argv) > 2 else "1-1000"
    scan_host(target, ports)
