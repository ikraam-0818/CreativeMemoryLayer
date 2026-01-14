import requests
import shutil

url = "https://image.pollinations.ai/prompt/futuristic%20robot%20making%20coffee"
print(f"Testing URL: {url}")

try:
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open("test_pollinations.jpg", "wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        print("SUCCESS: test_pollinations.jpg created")
    else:
        print(f"FAILED: {response.status_code}")
except Exception as e:
    print(f"FAILED: {e}")
