import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("--- Testing Veo 3 Video Generation ---")

def test_veo_rest(model_name):
    print(f"\nTesting model: {model_name}")
    # Veo usually uses the predict endpoint in Vertex AI, but in Gemini API (Generative Language) 
    # it might be under models:predict or similar.
    # Let's try the standard generateContent pattern for experimental models first, 
    # or the specific video generation method if documented.
    
    # URL pattern checking
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:predict?key={api_key}"
    
    # Veo Payload Structure (Hypothetical based on common Vertex patterns if not standard Gemini)
    payload = {
        "instances": [
             { "prompt": "Cinematic shot of a futuristic coffee robot, 4k, slow motion" }
        ],
        "parameters": {
            "sampleCount": 1,
            "videoLengthSeconds": 5
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
             print("SUCCESS (Predict Endpoint): 200 OK")
             print(str(response.json())[:500])
             return True
        else:
             print(f"Predict Endpoint Failed {response.status_code}: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

    # Try standard generateContent which is the Gemini Universal Endpoint
    url_gen = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    payload_gen = {
        "contents": [{
            "parts": [{"text": "Generate a video of a futuristic coffee robot"}]
        }]
    }
    try:
        response = requests.post(url_gen, json=payload_gen, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
             print("SUCCESS (GenerateContent): 200 OK")
             print(str(response.json())[:500])
             return True
        else:
             print(f"GenerateContent Endpoint Failed {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
        
    return False

# List of potential Veo model names in the public API
# Note: Veo might still be in Vertex AI only (GCP specific) rather than AI Studio (Generative Language API).
# If so, we can't access it easily with just an API Key, we need `gcloud auth`.
# But let's check the user's enabled API specifically.

test_veo_rest("models/veo-2.0-generate-001") # Guess at public name
test_veo_rest("models/veo-3.0-generate-001") # Guess at public name
test_veo_rest("models/gemini-2.0-flash-exp") # Just to see if it accepts video prompts now
