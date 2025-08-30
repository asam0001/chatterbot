import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# --- Load API Key ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in environment variables.")
    st.stop()

# --- Model Options ---
MODEL_OPTIONS = {
    "Gemini Flash (fast & cheap)": "models/gemini-1.5-flash",
    "Gemini Pro (advanced)": "models/gemini-1.5-pro-latest",
}

# --- Sidebar: Model Selector ---
with st.sidebar:
    st.header("⚙️ Settings")
    selected_model_name = st.selectbox("Choose Model:", list(MODEL_OPTIONS.keys()))
    selected_model = MODEL_OPTIONS[selected_model_name]

# --- Configure Gemini ---
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(selected_model)

# --- Page Setup ---
st.set_page_config(page_title="💬 Gemini Chatbot", layout="wide")
st.title("🤖 Gemini Chatbot")
st.markdown(f"Using **{selected_model_name}** ⚡")

# --- Custom CSS ---
st.markdown(
    """
    <style>
    .stChatMessage {padding: 12px; border-radius: 12px; margin-bottom: 10px;}
    .user-msg {background-color: #DCF8C6; text-align: right;}
    .assistant-msg {background-color: #F1F0F0; text-align: left;}
    .chat-box {max-height: 500px; overflow-y: auto; padding: 10px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session State ---
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_logs" not in st.session_state:
    st.session_state.chat_logs = []

# --- Sidebar Chat Controls ---
with st.sidebar:
    if st.button("🆕 New Chat"):
        if st.session_state.history:
            st.session_state.chat_logs.append(st.session_state.history.copy())
        st.session_state.history = []
        st.rerun()

    if st.session_state.chat_logs:
        st.subheader("📜 Previous Chats")
        for i, chat in enumerate(st.session_state.chat_logs):
            with st.expander(f"Chat #{i+1}"):
                for msg in chat:
                    role = "👤 User" if msg["role"] == "user" else "🤖 Assistant"
                    st.markdown(f"**{role}:** {msg['content']}")

# --- Display Current Chat ---
st.markdown("### 💬 Chat Window")
chat_container = st.container()
with chat_container:
    for msg in st.session_state.history:
        role_class = "user-msg" if msg["role"] == "user" else "assistant-msg"
        st.markdown(
            f"<div class='stChatMessage {role_class}'>{msg['content']}</div>",
            unsafe_allow_html=True,
        )

# --- Input ---
prompt = st.chat_input("Type your message here...")

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with chat_container:
        st.markdown(f"<div class='stChatMessage user-msg'>{prompt}</div>", unsafe_allow_html=True)

    with st.spinner("🤔 Thinking..."):
        try:
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"❌ Error: {e}"

    st.session_state.history.append({"role": "assistant", "content": reply})
    with chat_container:
        st.markdown(f"<div class='stChatMessage assistant-msg'>{reply}</div>", unsafe_allow_html=True)
