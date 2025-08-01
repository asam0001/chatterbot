import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")


# Streamlit UI setup
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("💬 Gemini Pro Chatbot")
st.markdown("Ask anything. Powered by Google's Gemini Pro API.")

# Chat history state
if "history" not in st.session_state:
    st.session_state.history = []

# Display previous messages
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Type your message here...")

if prompt:
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    # Call Gemini API
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"❌ Error: {e}"

    # Show bot reply
    st.chat_message("assistant").markdown(reply)
    st.session_state.history.append({"role": "assistant", "content": reply})
