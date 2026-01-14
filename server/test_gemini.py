import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load env from current directory
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"DEBUG: Loaded API Key: {api_key[:5]}...{api_key[-4:] if api_key else 'None'}")

if not api_key:
    print("ERROR: No API Key found. Please check .env file.")
    exit(1)

genai.configure(api_key=api_key)

print("Attempting to list models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"ERROR listing models: {e}")

print("\nAttempting generation with 'gemini-pro'...")
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'Hello Configured User'")
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"ERROR generating content: {e}")

print("\nAttempting generation with 'gemini-2.0-flash' (Recommended)...")
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say 'Hello Configured User'")
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"ERROR generating content with flash: {e}")
