import subprocess,os,sys
subprocess.run(["git","-C","cybersecurity-toolkit","pull"],capture_output=True)
os.chdir("cybersecurity-toolkit")
subprocess.run([sys.executable,"web/launch.py"])
