import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("No API key found in .env file!")

# Configure Gemini API
genai.configure(api_key=api_key)

# List models available to this API key
try:
    print("🔍 Listing available models for your key:\n")
    models = genai.list_models()
    for model in models:
        print(f"✅ {model.name} → Supported methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"❌ Error while listing models: {e}")
