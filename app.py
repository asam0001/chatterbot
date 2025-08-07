import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime

# --- Load API Key ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in environment variables.")
    st.stop()

# --- Configure Gemini ---
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# --- Page Setup ---
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("💬 Gemini Pro Chatbot")
st.markdown("Ask anything. Powered by Google's Gemini Pro API.")

# --- Initialize Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

if "chat_logs" not in st.session_state:
    st.session_state.chat_logs = []

# --- Action Buttons ---
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🆕 New Chat"):
        if st.session_state.history:
            st.session_state.chat_logs.append(st.session_state.history.copy())
        st.session_state.history = []
        st.rerun()

with col2:
    if st.button("🧹 Clear All Chats"):
        st.session_state.history = []
        st.session_state.chat_logs = []
        st.rerun()

with col3:
    if st.session_state.chat_logs:
        logs_text = ""
        for i, chat in enumerate(st.session_state.chat_logs):
            logs_text += f"\n--- Chat #{i+1} ---\n"
            for msg in chat:
                logs_text += f"{msg['role'].capitalize()}: {msg['content']}\n"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button("📥 Download All Chats", logs_text, f"gemini_chat_logs_{timestamp}.txt")

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

# --- Input Prompt ---
prompt = st.chat_input("Type your message here...")

if prompt:
    # Add user message
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    # Gemini Response
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"❌ Error: {e}"

    # Add assistant reply
    st.chat_message("assistant").markdown(reply)
    st.session_state.history.append({"role": "assistant", "content": reply})
