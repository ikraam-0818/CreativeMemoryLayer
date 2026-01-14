import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("--- Testing Veo 3 with google-genai SDK ---")

client = genai.Client(api_key=api_key)

try:
    # Based on the new SDK patterns (which match the React example logic but in Python)
    # The React example used 'generateVideo' via a service.
    # In Python, it's typically client.models.generate_videos
    
    print("Attempting to generate video with 'veo-2.0-generate-001'...")
    response = client.models.generate_videos(
        model="veo-2.0-generate-001", 
        prompt="A cinematic drone shot of a futuristic city at sunset, 4k, hyper-realistic",
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            # aspect_ratio="16:9" # Optional config
        )
    )
    
    # Check response (It might be an Operation or direct Video object)
    print("Response received!")
    # In the new SDK, response usually contains 'generated_videos' or we need to wait for operation
    
    print("Response received! Operation started.")
    print(f"Operation Name: {response.name}")
    
    # Poll for result
    import time
    operation_name = response.name
    
    print("Waiting for video generation (this takes time)...")
    while True:
        # Check operation status - Passing the object itself as the error suggested 'str' has no 'name'
        # Check if the method accepts the name string positionally?
        try:
            op = client.operations.get(name=operation_name)
        except TypeError:
            try:
                op = client.operations.get(operation_name)
            except Exception:
                op = client.operations.get(response)

        if op.done:
            if op.error:
                print(f"Operation Failed: {op.error}")
            else:
                print("Operation Completed!")
                # processing result
                # The result is typically in op.response or we need to look at document
                # For Veo, the result usually contains the generated video
                
                # In the new SDK, the operation might convert to the result type automatically if we use a helper,
                # but 'client.operations.get' returns the raw operation.
                # Let's inspect the 'result' or 'response' field.
                
                if op.result:
                     print(f"Result: {op.result}")
                     # Try to access video uri from result if structured
                else:
                     print(f"Raw Done Response: {op}")
            break
        
        print(".", end="", flush=True)
        time.sleep(2)

except Exception as e:
    print(f"Veo 2.0 Failed: {e}")


try:
    print("\nAttempting to generate video with 'veo-3.0-generate-001' (Speculative)...")
    # Trying various model names just in case
    response = client.models.generate_videos(
        model="veo-3.0-generate-001",
        prompt="A cute robot barista",
    )
    print(f"Veo 3.0 Response: {response}")
except Exception as e:
    print(f"Veo 3.0 Failed: {e}")

