#!/bin/bash
# ClawGuardian Hybrid Wakelock & Persistence
# Monitors Streamlit, Heartbeat, and OpenClaw Gateway.

SAFE_ZONE="./safe_zone"
LOG_DIR="$SAFE_ZONE/logs"
mkdir -p "$LOG_DIR"

echo "🦞 Starting ClawGuardian Hybrid Persistence loop..."

while true; do
    # 1. Check Streamlit (Port 8501)
    if ! lsof -i :8501 > /dev/null; then
        echo "[$(date)] Streamlit not found. Restarting..."
        nohup streamlit run streamlit_app.py --server.port 8501 --server.headless true > "$LOG_DIR/streamlit.log" 2>&1 &
    fi

    # 2. Check Heartbeat Script
    if ! pgrep -f "python3 safe_zone/heartbeat.py" > /dev/null; then
        echo "[$(date)] Heartbeat not found. Restarting..."
        nohup python3 safe_zone/heartbeat.py > "$LOG_DIR/heartbeat_process.log" 2>&1 &
    fi

    # 3. Check OpenClaw Gateway (Port 18789)
    if ! lsof -i :18789 > /dev/null; then
        echo "[$(date)] OpenClaw Gateway not found. Restarting..."
        cd openclaw_repo && nohup npm run gateway > "../$LOG_DIR/openclaw.log" 2>&1 &
        cd ..
    fi

    # 10 minute check interval
    sleep 600
done
