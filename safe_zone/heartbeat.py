"""
ClawGuardian Heartbeat
Pings the local Streamlit application every 10 minutes.
Logs status to safe_zone/heartbeat.log.
Adheres to Rule 8: Logging and Transparency.
"""

import time
import requests
import datetime
import os

LOG_FILE = "safe_zone/heartbeat.log"
URL = "http://localhost:8501"
INTERVAL = 600  # 10 minutes

def log_heartbeat(status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Heartbeat Status: {status}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

def run():
    print(f"Starting ClawGuardian Heartbeat (Ping: {INTERVAL}s)...")
    while True:
        try:
            response = requests.get(URL, timeout=10)
            if response.status_code == 200:
                log_heartbeat("ALIVE")
            else:
                log_heartbeat(f"WARNING: HTTP {response.status_code}")
        except Exception as e:
            log_heartbeat(f"ERROR: {e}")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    run()
