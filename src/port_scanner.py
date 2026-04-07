from scapy.all import sr, IP, TCP
import json

def scan_ports(ip_address):
    results = []
    for port in range(1, 1001):
        packet = IP(dst=ip_address)/TCP(sport=port, dport=port, flags="S")
        response, _ = sr(packet, timeout=2, verbose=False)
        if len(response) > 0:
            results.append({"port": port, "status": "open", "banner": get_banner(response[0][1])})
    return results

def get_banner(packet):
    if hasattr(packet, "payload"):
        payload = bytes(packet.payload)
        if b"HTTP" in payload: return "Web Server"
        elif b"SSH" in payload: return "SSH Server"
        elif b"FTP" in payload: return "FTP Server"
        elif b"SMTP" in payload: return "Mail Server"
        elif b"SQL" in payload: return "SQL Server"
        else: return "Unknown"
    return "No Payload"

def main():
    ip_address = input("Enter IP address to scan: ")
    results = scan_ports(ip_address)
    output_file = f"{ip_address}_scan.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Scan complete. {len(results)} open ports. Results: {output_file}")

if __name__ == "__main__":
    main()

