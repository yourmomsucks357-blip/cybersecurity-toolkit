import os, subprocess, sys

if not os.path.exists("cybersecurity-toolkit"):
    subprocess.run(["git", "clone", "https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git"])
else:
    subprocess.run(["git", "-C", "cybersecurity-toolkit", "pull"])

os.chdir("cybersecurity-toolkit")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])

tools = {
    1: ("Port Scanner", "src/port_scanner.py"),
    2: ("Network Recon", "src/recon.py"),
    3: ("Web Scanner", "src/web_scanner.py"),
    4: ("Credential Tester", "src/credential_tester.py"),
    5: ("Network Sniffer", "src/network_sniffer.py"),
    6: ("News Headlines", "src/tool1_news.py"),
    7: ("Full Scan", "src/main.py"),
    8: ("Dual Brain (Dolphin+Claude)", "src/dual_brain.py"),
}

print("\n=== JEFE CYBERSECURITY TOOLKIT ===\n")
while True:
    for k, v in tools.items():
        print(f"  {k}: {v[0]}")
    print("  0: Exit\n")
    choice = input("Pick a tool: ")
    if choice == "0":
        break
    try:
        num = int(choice)
        if num in tools:
            if num in [2, 3, 4, 7]:
                target = input("Target IP: ")
                subprocess.run([sys.executable, tools[num][1], "-t", target])
            elif num == 8:
                subprocess.run([sys.executable, tools[num][1]])
            else:
                subprocess.run([sys.executable, tools[num][1]])
        else:
            print("Invalid.")
    except ValueError:
        print("Enter a number.")
