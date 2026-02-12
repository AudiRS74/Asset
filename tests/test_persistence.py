import socket
import subprocess
import time
import os

def test_persistence():
    print("Testing persistence logic...")
    # 1. Check if ports are in wakelock.sh
    with open("safe_zone/wakelock.sh", "r") as f:
        content = f.read()
        if "lsof -i :8501" in content and "lsof -i :18789" in content:
            print("SUCCESS: Ports 8501 and 18789 are monitored in wakelock.sh")
        else:
            print("FAILURE: Ports missing from wakelock.sh")
            return False

    # 2. Check script syntax
    res = subprocess.run(["bash", "-n", "safe_zone/wakelock.sh"])
    if res.returncode == 0:
        print("SUCCESS: wakelock.sh has valid bash syntax.")
    else:
        print("FAILURE: wakelock.sh syntax error.")
        return False

    return True

if __name__ == "__main__":
    if test_persistence():
        print("TEST PASSED")
    else:
        print("TEST FAILED")
