import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def test_flow():
    print("1. Creating Project...")
    res = requests.post(f"{BASE_URL}/api/projects", json={
        "name": "Test Project",
        "topic": "A short history of coffee",
        "mode": "text_to_video"
    })
    if res.status_code != 200:
        print(f"Failed to create project: {res.text}")
        sys.exit(1)
    
    project = res.json()
    p_id = project['id']
    print(f"   Project Created: {p_id}")
    
    print("2. Triggering Script Generation...")
    # Trigger generation (first step is scripting if script is missing)
    res = requests.post(f"{BASE_URL}/api/projects/{p_id}/generate")
    if res.status_code != 200:
        print(f"Failed to trigger generation: {res.text}")
        sys.exit(1)
        
    print("   Generation Queued. Waiting for script...")
    
    # Poll for script
    for _ in range(30): # Wait up to 30s for script
        res = requests.get(f"{BASE_URL}/api/projects/{p_id}")
        data = res.json()
        if data.get('script'):
            print("   Script Generated!")
            print(f"   Title: {data['script']['title']}")
            break
        if data['status'] == 'failed':
            print(f"   Generation Failed: {data.get('error')}")
            sys.exit(1)
        time.sleep(1)
    
    if not data.get('script'):
        print("   Timeout waiting for script.")
        sys.exit(1)

    print("3. Modifying Script (Persistence Test)...")
    script = data['script']
    script['title'] = "The EDITED History of Coffee"
    
    res = requests.put(f"{BASE_URL}/api/projects/{p_id}/script", json={"script": script})
    if res.status_code != 200:
        print(f"Failed to update script: {res.text}")
        sys.exit(1)
        
    print("   Script Updated.")
    
    # Verify persistence by fetching again
    res = requests.get(f"{BASE_URL}/api/projects/{p_id}")
    new_data = res.json()
    if new_data['script']['title'] != "The EDITED History of Coffee":
        print("   Persistence Check FAILED: Title did not update.")
        sys.exit(1)
    else:
        print("   Persistence Check PASSED.")

    print("\n✅ Verification Complete: Project Flow & Persistence Working.")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"Test failed: {e}")
