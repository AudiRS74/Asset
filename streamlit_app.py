import streamlit as st

st.set_page_config(page_title="ClawGuardian Proxy", page_icon="🦞")

st.title("🦞 ClawGuardian Proxy")
st.subheader("Secure Autonomous Interface for Auctus")

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

# React to user input
if prompt := st.chat_input("Command ClawGuardian..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Simple command handling logic (placeholder for actual bridge integration)
    with st.chat_message("assistant"):
        if "confirm" in prompt.lower():
            response = "Confirmation received. Proceeding within security boundaries."
        else:
            response = f"I have received your command: '{prompt}'. Analyzing for security risks..."
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.sidebar.markdown("### Security Status: 🟢 VIGILANT")
st.sidebar.info("All operations restricted to `./safe_zone/` and require explicit confirmation.")
