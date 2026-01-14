import requests
import time

def test_video(prompt, model="turbo"):
    print(f"\nTesting Video with model='{model}'...")
    # Pollinations usually doesn't have a simple GET for video like it does for images.
    # It often requires a POST to a feed or specific generation endpoint.
    # However, sometimes they expose it simply.
    
    # Try 1: Standard Image Endpoint with model param (Some models are video?)
    url = f"https://image.pollinations.ai/prompt/{prompt}?model={model}&width=720&height=720"
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            content_type = r.headers.get('Content-Type', '')
            print(f"Status 200. Content-Type: {content_type}")
            if 'video' in content_type:
                 with open(f"test_vid_{model}.mp4", "wb") as f:
                     for chunk in r.iter_content(chunk_size=1024):
                         f.write(chunk)
                 print("Saved video file!")
                 return True
            elif 'image' in content_type:
                 print("Returned an image, not video.")
        else:
            print(f"Status {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")
        
    # Try 2: specific feed/video endpoint if known?
    # Based on search, it might be heavily unified.
    
    return False

# Attempt to ask for Veo
# test_video("futuristic robot barista", model="veo-3.1")
# test_video("futuristic robot barista", model="veo")

# Main approach check
print("Pollinations Video check...")
# Usually video is on a diff subdomain or unavailable freely via GET.
# Let's try the 'turbo' model which is sometimes video capable in other tools? Unlikely.
pass
