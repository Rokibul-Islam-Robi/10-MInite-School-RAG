import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

print("Available Gemini Models for generateContent:")
found_model = False
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(f"- {m.name}")
        if "gemini-1.0-pro" in m.name or "gemini-pro" in m.name:
            found_model = True
if not found_model:
    print("\nCould not find a 'gemini-1.0-pro' or 'gemini-pro' model supporting generateContent.")
    print("This might indicate an API key issue or regional availability.")

print("\nAvailable Gemini Models for embedding (embedContent):")
found_embedding_model = False
for m in genai.list_models():
    if "embedContent" in m.supported_generation_methods:
        print(f"- {m.name}")
        if "embedding-001" in m.name:
            found_embedding_model = True
if not found_embedding_model:
    print("\nCould not find 'embedding-001' model supporting embedContent.")
    print("This might indicate an API key issue or regional availability.")