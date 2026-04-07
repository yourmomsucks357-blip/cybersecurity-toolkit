#!/usr/bin/env python3
"""Network Traffic Analysis Module"""
from collections import Counter

class NetworkSniffer:
    def __init__(self, interface="eth0", count=100):
        self.interface = interface
        self.count = count
        self.results = {"packets_captured": 0, "protocols": {}, "connections": []}

    def capture(self):
        try:
            from scapy.all import sniff, IP, TCP, UDP
            print(f"  [*] Capturing {self.count} packets on {self.interface}...")
            packets = sniff(iface=self.interface, count=self.count, timeout=30)
            self.results["packets_captured"] = len(packets)
            protos = Counter()
            conns = set()
            for pkt in packets:
                if IP in pkt:
                    src = pkt[IP].src
                    dst = pkt[IP].dst
                    if TCP in pkt:
                        protos["TCP"] += 1
                        conns.add(f"{src}:{pkt[TCP].sport} -> {dst}:{pkt[TCP].dport}")
                    elif UDP in pkt:
                        protos["UDP"] += 1
                        conns.add(f"{src} -> {dst} (UDP)")
                    else:
                        protos["Other"] += 1
            self.results["protocols"] = dict(protos)
            self.results["connections"] = list(conns)[:50]
            print(f"  [+] Captured {len(packets)} packets")
        except ImportError:
            print("  [-] scapy not installed")
        except Exception as e:
            print(f"  [-] Capture error: {e}")
        return self.results

    def run(self):
        return self.capture()

