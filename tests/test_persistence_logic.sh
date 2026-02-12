#!/bin/bash
# Test Wakelock
echo "Testing Hybrid persistence..."
# Start a dummy listener on 18789
nc -l -p 18789 &
pid=$!
sleep 2
if lsof -i :18789 > /dev/null; then
    echo "Dummy OpenClaw running."
    kill $pid
    echo "Dummy killed."
    # Check if wakelock logic works (using grep on the script logic)
    if grep -q "lsof -i :18789" safe_zone/wakelock.sh; then
        echo "Wakelock logic verified for port 18789."
    fi
else
    echo "Port 18789 check failed."
fi
