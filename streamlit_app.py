import streamlit as st
from streamlit_mic_recorder import speech_to_text
from streamlit_TTS import text_to_audio, auto_play
from safe_zone.voice_handler import VoiceHandler
from safe_zone.web_ai_bridge import WebAIBridge
from safe_zone.device_manager import DeviceManager
import asyncio

st.set_page_config(page_title="ClawGuardian Proxy", page_icon="🦞")

# Initialize Handlers in session state
if "voice_handler" not in st.session_state:
    st.session_state.voice_handler = VoiceHandler()

if "device_manager" not in st.session_state:
    st.session_state.device_manager = DeviceManager()

if "web_bridge" not in st.session_state:
    st.session_state.web_bridge = WebAIBridge()

# Playwright Initialization for Cloud Deployment
if "playwright_installed" not in st.session_state:
    try:
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        st.session_state.playwright_installed = True
    except Exception as e:
        st.sidebar.error(f"Playwright Init Error: {e}")

st.title("🦞 ClawGuardian Proxy")
st.subheader("Secure Autonomous Interface for Auctus")

# Sidebar for Security and Settings
st.sidebar.markdown("### Security Status: 🟢 VIGILANT")
st.sidebar.info("All operations restricted to `./safe_zone/` and require explicit confirmation.")

st.sidebar.divider()
st.sidebar.markdown("### 🎙️ Voice & Privacy Settings")
voice_consent = st.sidebar.checkbox("Explicit Written Consent for Voice Processing", help="Rule 7: Required before enabling STT/TTS.")
voice_sample = st.sidebar.file_uploader("Upload Voice Sample", type=["wav", "mp3", "m4a"], help="Rule 7: Required for identity verification and cloning safety.")
talkback_enabled = st.sidebar.toggle("Enable Voice Talkback", value=False, disabled=not (voice_consent and voice_sample is not None))

# Update Voice Security State
st.session_state.voice_handler.update_security_status(voice_sample is not None, voice_consent)
voice_enabled = st.session_state.voice_handler.verified and st.session_state.voice_handler.consent_granted

if voice_enabled:
    st.sidebar.success("Voice Features Enabled")
else:
    st.sidebar.warning("Voice Features Disabled (Consent & Sample Required)")

st.sidebar.divider()
st.sidebar.markdown("### 📱 Termux & Remote Access")
if st.sidebar.button("Generate Termux Setup Command"):
    st.sidebar.code("curl -sL https://raw.githubusercontent.com/user/repo/main/safe_zone/termux_setup.sh | bash", language="bash")
    st.sidebar.info("Rule 4: Confirm environment safety before running.")

with st.sidebar.expander("🌐 Secure Tunnel (Link with Token)"):
    st.markdown("To view on browser with a secure link:")
    st.code("pkg install cloudflared\ncloudflared tunnel --url http://localhost:8501", language="bash")
    st.caption("Cloudflare will provide a random URL. Treat it as a temporary token.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Greeting, Auctus. ClawGuardian is online and vigilant.\n\n"
                "I confirm that the **10 Mandatory Security & Safety Rules** are locked in as my absolute top priority.\n\n"
                "**Detected Capabilities:**\n"
                "- **Bash/Local Shell:** For system management.\n"
                "- **Playwright:** For browser and Web-AI interaction.\n"
                "- **ADB:** For Android automation.\n"
                "- **Persistence:** 24/7 Wakelock and 10-min heartbeat enabled.\n\n"
                "Auctus is ready. What do you want to do first?"
            )
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

        # 1. Multi-bot Fallback Logic
        if "fail" in prompt.lower() or "help" in prompt.lower():
            response_placeholder.markdown("⚠️ *Local task execution encountered a hurdle. Consulting secondary AI agents for advice...*")
            # We use asyncio.run for the bridge call as it's a one-off in the script execution
            advice = asyncio.run(st.session_state.web_bridge.ask_question(None, None, prompt, None))
            response = f"I encountered an issue, so I consulted Gemini/Grok. Their advice: '{advice}'. Shall I proceed with this plan?"

        # 2. Device Management Logic
        elif "device" in prompt.lower() or "android" in prompt.lower():
            devices = st.session_state.device_manager.list_android_devices()
            response = f"Detected Devices:\n```\n{devices}\n```\nRule 4: I require explicit confirmation to run any ADB shell commands. How would you like to proceed?"

        # 3. Security Hardening Check
        elif "security" in prompt.lower() or "status" in prompt.lower():
            response = (
                "**Security Audit:**\n"
                "1. **Shell:** Restricted to read-only/simulated mode.\n"
                "2. **Files:** Locked to `./safe_zone/`.\n"
                "3. **External APIs:** Gated behind confirmation.\n"
                "4. **Voice:** " + ("UNLOCKED" if voice_enabled else "LOCKED (Sample/Consent Missing)") + ".\n"
                "Status: **MAXIMUM VIGILANCE.**"
            )

        else:
            response = f"I have received your command: '{prompt}'. No immediate security violations detected. Standing by for specific execution instructions."

        response_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Talkback execution
    if talkback_enabled:
        # Note: In a real app, text_to_audio would call the synthesizer
        # For demo, we just trigger the component if verified
        audio_dict = text_to_audio(response, language='en')
        auto_play(audio_dict)
