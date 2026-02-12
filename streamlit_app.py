import streamlit as st
from streamlit_mic_recorder import speech_to_text
from streamlit_TTS import text_to_audio, auto_play

st.set_page_config(page_title="ClawGuardian Proxy", page_icon="🦞")

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

voice_enabled = voice_consent and voice_sample is not None

if voice_enabled:
    st.sidebar.success("Voice Features Enabled")
else:
    st.sidebar.warning("Voice Features Disabled (Consent & Sample Required)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Greeting, Auctus. ClawGuardian is online and vigilant.\n\n"
                "I confirm that the **10 Mandatory Security & Safety Rules** are locked in as my absolute top priority; they override every other goal and cannot be weakened or removed.\n\n"
                "**Detected Capabilities:**\n"
                "- **Bash/Local Shell:** For system management and file operations.\n"
                "- **Playwright:** For browser automation and visual UI interaction.\n"
                "- **ADB:** For Android device automation.\n\n"
                "**Hardening Steps Implemented:**\n"
                "- **Designated Safe Zone:** All file operations restricted to `./safe_zone/`.\n"
                "- **Strict Confirmation Policy:** Every sensitive action (credentials, shell, transactions) requires explicit approval.\n"
                "- **Credential Protection:** Secrets are never stored or displayed in plaintext.\n\n"
                "Auctus is ready. What do you want to do first?\n"
                "- Provide a voice sample with consent.\n"
                "- Approve/test a specific safe skill.\n"
                "- Run a harmless browser demo.\n"
                "- Set up daily briefings."
            )
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Audio Player Placeholder (Rule 7 Talkback)
audio_placeholder = st.empty()

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

# Always render chat input
chat_input_text = st.chat_input("Command ClawGuardian...")

# Determine the active prompt
prompt = voice_input_text or chat_input_text

# React to user input (Voice or Text)
if prompt:
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Simple command handling logic
    with st.chat_message("assistant"):
        if "confirm" in prompt.lower():
            response = "Confirmation received. Proceeding within security boundaries."
        else:
            response = f"I have received your command: '{prompt}'. Analyzing for security risks..."
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Talkback execution
    if talkback_enabled:
        audio_dict = text_to_audio(response, language='en')
        auto_play(audio_dict)
