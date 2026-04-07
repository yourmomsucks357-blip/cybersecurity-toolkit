import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

def connect_ssh(hostname=None, port=None, username=None, password=None):
    hostname = hostname or os.getenv("SERVER_HOST")
    port = int(port or os.getenv("SERVER_PORT", 22))
    username = username or os.getenv("USER_NAME")
    password = password or os.getenv("PASSWORD")
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
        print(f"[+] Connected to {hostname}:{port}")
        return ssh_client
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return None

def run_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode()
    errors = stderr.read().decode()
    if output:
        print(output)
    if errors:
        print(f"STDERR: {errors}")
    return output

def check_gpu(ssh_client):
    print("[*] Checking GPU...")
    return run_command(ssh_client, "nvidia-smi")

def interactive_shell(ssh_client):
    print("[*] Interactive mode. Type 'exit' to quit.")
    while True:
        cmd = input("$ ")
        if cmd.lower() == "exit":
            break
        run_command(ssh_client, cmd)

if __name__ == "__main__":
    import sys
    host = sys.argv[1] if len(sys.argv) > 1 else None
    client = connect_ssh(hostname=host)
    if client:
        if len(sys.argv) > 2:
            run_command(client, " ".join(sys.argv[2:]))
        else:
            interactive_shell(client)
        client.close()
