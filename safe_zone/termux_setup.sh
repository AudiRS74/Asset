#!/data/data/com.termux/files/usr/bin/bash
# ClawGuardian Termux Setup Script
# Created for Auctus - February 2026

echo "🦞 Initializing ClawGuardian for Termux..."

# Update and install system dependencies
pkg update -y && pkg upgrade -y
pkg install -y python git android-tools ffmpeg libjpeg-turbo

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Provide a helper for tunneling (Cloudflare)
echo "--------------------------------------------------"
echo "Setup Complete."
echo "To launch ClawGuardian with a secure remote link:"
echo "1. Run: streamlit run streamlit_app.py"
echo "2. In a NEW Termux session, run: pkg install cloudflared && cloudflared tunnel --url http://localhost:8501"
echo "--------------------------------------------------"
