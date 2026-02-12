#!/bin/bash
# ClawGuardian Wakelock & Persistence
# Ensures the Streamlit app and Heartbeat script run continuously.

SAFE_ZONE="./safe_zone"
LOG_DIR="$SAFE_ZONE/logs"
mkdir -p "$LOG_DIR"

echo "Starting ClawGuardian persistence loop..."

while true; do
    # Check if Streamlit is running
    if ! lsof -i :8501 > /dev/null; then
        echo "[$(date)] Streamlit not found. Restarting..."
        nohup streamlit run streamlit_app.py --server.port 8501 --server.headless true > "$LOG_DIR/streamlit.log" 2>&1 &
    fi

    # Check if Heartbeat is running
    if ! pgrep -f "python3 safe_zone/heartbeat.py" > /dev/null; then
        echo "[$(date)] Heartbeat not found. Restarting..."
        nohup python3 safe_zone/heartbeat.py > "$LOG_DIR/heartbeat_process.log" 2>&1 &
    fi

    # 10 minute check interval for the watcher itself
    sleep 600
done
