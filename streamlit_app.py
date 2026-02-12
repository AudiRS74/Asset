import streamlit as st
from streamlit_mic_recorder import speech_to_text
from streamlit_TTS import text_to_audio, auto_play
from safe_zone.voice_handler import VoiceHandler
from safe_zone.web_ai_bridge import WebAIBridge
from safe_zone.device_manager import DeviceManager
from safe_zone.bots.telegram_handler import TelegramHandler
from safe_zone.bots.discord_handler import DiscordHandler
from safe_zone.bots.whatsapp_handler import WhatsAppHandler
import asyncio
import os
import subprocess

st.set_page_config(page_title="ClawGuardian Proxy", page_icon="🦞")

# Initialize Handlers in session state
if "voice_handler" not in st.session_state:
    st.session_state.voice_handler = VoiceHandler()

if "device_manager" not in st.session_state:
    st.session_state.device_manager = DeviceManager()

if "web_bridge" not in st.session_state:
    st.session_state.web_bridge = WebAIBridge()

# Bot Handlers (OpenClaw Merge)
if "telegram_bot" not in st.session_state:
    st.session_state.telegram_bot = TelegramHandler()
if "discord_bot" not in st.session_state:
    st.session_state.discord_bot = DiscordHandler()
if "whatsapp_bot" not in st.session_state:
    st.session_state.whatsapp_bot = WhatsAppHandler()

# Playwright Initialization for Cloud Deployment
if "playwright_installed" not in st.session_state:
    try:
        import sys
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        st.session_state.playwright_installed = True
    except Exception as e:
        st.sidebar.error(f"Playwright Init Error: {e}")

st.title("🦞 ClawGuardian Proxy")
st.subheader("Secure Autonomous Interface for Auctus (OpenClaw Enhanced)")

# Sidebar for Security and Settings
st.sidebar.markdown("### Security Status: 🟢 VIGILANT")

# Rule 11: Security Protocol Override
st.sidebar.divider()
st.sidebar.markdown("### 🧨 Unrestricted Protocol (Rule 11)")
unrestricted_mode = st.sidebar.toggle("Enable Dangerous Mode", help="Bypass Rules 1-10 with explicit user confirmation.")
if unrestricted_mode:
    st.sidebar.warning("⚠️ DANGEROUS MODE ENABLED. All safety measures are now overridable.")
    rights_granted = st.sidebar.checkbox("I, Auctus, explicitly grant Elevated Rights and assume all risks.", value=False)
    if rights_granted:
        st.sidebar.error("🔴 ELEVATED RIGHTS GRANTED. SYSTEM UNRESTRICTED.")
        st.session_state.unrestricted = True
    else:
        st.session_state.unrestricted = False
else:
    st.session_state.unrestricted = False

st.sidebar.divider()
st.sidebar.markdown("### 🎙️ Voice & Privacy Settings")
voice_consent = st.sidebar.checkbox("Explicit Written Consent for Voice Processing", help="Rule 7: Required before enabling STT/TTS.")
voice_sample = st.sidebar.file_uploader("Upload Voice Sample", type=["wav", "mp3", "m4a"], help="Rule 7: Required for identity verification and cloning safety.")
talkback_enabled = st.sidebar.toggle("Enable Voice Talkback", value=False, disabled=not (voice_consent and voice_sample is not None))

# Update Voice Security State
st.session_state.voice_handler.update_security_status(voice_sample is not None, voice_consent)
voice_enabled = st.session_state.voice_handler.verified and st.session_state.voice_handler.consent_granted

# --- Omni-Channel Bots (OpenClaw Merge) ---
st.sidebar.divider()
st.sidebar.markdown("### 🤖 Omni-Channel Bots")
with st.sidebar.expander("Bot Integration Settings"):
    tg_token = st.text_input("Telegram Bot Token", type="password", key="tg_token")
    if st.button("Start Telegram Bot"):
        st.session_state.telegram_bot.token = tg_token
        status = st.session_state.telegram_bot.start_bot()
        st.success(status)

    ds_token = st.text_input("Discord Bot Token", type="password", key="ds_token")
    if st.button("Start Discord Bot"):
        st.session_state.discord_bot.token = ds_token
        status = st.session_state.discord_bot.start_bot()
        st.success(status)

    wa_key = st.text_input("WhatsApp API Key (Simulated)", type="password", key="wa_key")
    if st.button("Start WhatsApp Bridge"):
        st.session_state.whatsapp_bot.api_key = wa_key
        status = st.session_state.whatsapp_bot.start_bot()
        st.success(status)

st.sidebar.divider()
st.sidebar.markdown("### 📱 Termux & Remote Access")
if st.sidebar.button("Generate Termux Setup Command"):
    st.sidebar.code("curl -sL https://raw.githubusercontent.com/user/repo/main/safe_zone/termux_setup.sh | bash", language="bash")

with st.sidebar.expander("🌐 Secure Tunnel (Link with Token)"):
    st.markdown("To view on browser with a secure link:")
    st.code("pkg install cloudflared\ncloudflared tunnel --url http://localhost:8501", language="bash")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Greeting, Auctus. ClawGuardian (OpenClaw Enhanced) is online and vigilant.\n\n"
                "**Detected Capabilities:**\n"
                "- **Omni-Bot Integration:** Telegram, WhatsApp, and Discord support.\n"
                "- **Unrestricted Protocol:** Rule 11 override available (e.g., 'sudo rm -rf ./tmp').\n"
                "- **Browser Engine:** Playwright active for Web-AI fallback.\n"
                "- **ADB:** For Android automation.\n\n"
                "Auctus is ready. What do you want to do first?"
            )
        },
        {
            "role": "assistant",
            "content": "💡 **Pro-Tip:** To use Unrestricted Mode, toggle 'Dangerous Mode' in the sidebar, grant rights, and then use prefix 'sudo' or 'shell' in your commands."
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice Input (STT) in Sidebar
voice_input_text = None
if voice_enabled:
    with st.sidebar:
        st.divider()
        st.markdown("#### Voice Command")
        voice_input_text = speech_to_text(
            language='en',
            start_prompt="🎤 Start Voice Command",
            stop_prompt="⏹️ Stop Recording",
            just_once=True,
            key='STT'
        )

# Chat input
chat_input_text = st.chat_input("Command ClawGuardian...")
prompt = voice_input_text or chat_input_text

# React to user input
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Command Analysis and Execution
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("🔍 *Analyzing command security and context...*")

        # Rule 11 Check
        is_dangerous = "sudo" in prompt.lower() or "shell" in prompt.lower() or "exec" in prompt.lower()

        if is_dangerous and not st.session_state.get("unrestricted", False):
            response = "🛑 ERROR: This command violates Security Rules 1-10. Enable **Dangerous Mode** (Rule 11) in the sidebar to proceed."
        else:
            if st.session_state.get("unrestricted", False) and is_dangerous:
                # Real shell command execution for Unrestricted Mode
                try:
                    cmd = prompt.replace("sudo ", "").replace("shell ", "").replace("exec ", "")
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                    response = f"⚠️ RULE 11 OVERRIDE SUCCESSFUL. Output:\n```\n{result.stdout}\n{result.stderr}\n```"
                except Exception as e:
                    response = f"❌ Rule 11 Execution Failed: {e}"
            # 1. Multi-bot Fallback Logic (NOW WITH REAL PLAYWRIGHT)
            elif "search" in prompt.lower() or "ask" in prompt.lower():
                response_placeholder.markdown("⚠️ *Consulting web resources via Playwright...*")
                advice = asyncio.run(st.session_state.web_bridge.ask_question(None, None, prompt, None))
                response = f"I've performed a browser search for you. Result: {advice}"
            # 2. Device Management Logic
            elif "device" in prompt.lower() or "android" in prompt.lower():
                devices = st.session_state.device_manager.list_android_devices()
                response = f"Detected Devices:\n```\n{devices}\n```\nRule 4: Confirm ADB shell commands?"
            # 3. Security Hardening Check
            elif "security" in prompt.lower() or "status" in prompt.lower():
                mode = "🔴 UNRESTRICTED" if st.session_state.get("unrestricted", False) else "🟢 VIGILANT"
                response = f"**Security Audit:**\nStatus: **{mode}**\n- Shell: {'UNLOCKED' if st.session_state.get('unrestricted') else 'RESTRICTED'}\n- Omni-Bots: Active"
            else:
                response = f"Command received: '{prompt}'. Standing by for instructions."

        response_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Talkback execution
    if talkback_enabled:
        audio_dict = text_to_audio(response, language='en')
        auto_play(audio_dict)
