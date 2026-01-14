import os
import requests
import json
import base64
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("--- Testing Image Generation (REST API) ---")

def test_rest_endpoint(model_name):
    print(f"\nTesting model: {model_name}")
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateImages?key={api_key}"
    
    payload = {
        "prompt": {
            "text": "A cute futuristic robot barista serving coffee, cinematic lighting"
        },
        "number_of_images": 1
    }
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print("SUCCESS: 200 OK")
            data = response.json()
            if 'images' in data:
                img_data = data['images'][0]['image64']
                # Save just to be sure
                with open(f"test_{model_name.replace('/', '_')}.png", "wb") as f:
                     f.write(base64.b64decode(img_data))
                print("Image saved successfully.")
                return True
            else:
                print(f"Unexpected JSON structure: {list(data.keys())}")
        else:
            print(f"FAILED {response.status_code}: {response.text}")
    except Exception as e:
        print(f"EXCEPTION: {e}")
    return False

# Test 1: Content generation model (Likely to fail on generateImages endpoint but worth a shot)
# test_rest_endpoint("models/gemini-2.0-flash-exp-image-generation")

# Test 2: Standard Imagen 3 endpoint (Hidden but often available)
test_rest_endpoint("models/imagen-3.0-generate-001")

# Test 3: Legacy Imagen 2
test_rest_endpoint("models/image-generation-002")
