import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env for API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check API key
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in environment variables.")
    st.stop()

# Configure Gemini model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# Page setup
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("💬 Gemini Pro Chatbot")
st.markdown("Ask anything. Powered by Google's Gemini Pro API.")

# --- Session State Setup ---
if "history" not in st.session_state:
    st.session_state.history = []

if "chat_logs" not in st.session_state:
    st.session_state.chat_logs = []

# --- New Chat Button ---
if st.button("🆕 New Chat"):
    if st.session_state.history:
        # Save current chat to logs
        st.session_state.chat_logs.append(st.session_state.history.copy())
    st.session_state.history = []  # Reset current chat
    st.experimental_rerun()

# --- View Old Chats ---
if st.session_state.chat_logs:
    with st.expander("📜 View Previous Chats"):
        for i, chat in enumerate(st.session_state.chat_logs):
            st.markdown(f"**Chat #{i+1}:**")
            for msg in chat:
                st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")
            st.markdown("---")

# --- Display Current Chat ---
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input ---
prompt = st.chat_input("Type your message here...")

if prompt:
    # User message
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    # Gemini Response
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"❌ Error: {e}"

    # Assistant reply
    st.chat_message("assistant").markdown(reply)
    st.session_state.history.append({"role": "assistant", "content": reply})
