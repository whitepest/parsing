import time
import subprocess

while True:
    # Run the script
    subprocess.run(["python3", "create_access_token.py"])
    # Wait for an hour (3600 seconds)
    time.sleep(3600)
