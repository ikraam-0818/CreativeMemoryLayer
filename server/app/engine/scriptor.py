import os
import json
import traceback
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Client
api_key = os.getenv("GOOGLE_API_KEY")
client = None
if api_key:
    client = genai.Client(api_key=api_key)

def generate_script(topic: str) -> dict:
    """
    Generates a video script (scenes, visual prompts, voiceover) from a topic using Gemini.
    """
    # Use gemini-2.0-flash
    model_id = "gemini-2.0-flash"
    
    prompt = f"""
    You are an expert video producer. Create a script for a short 30-60 second explainer video about: "{topic}".
    
    Output strictly valid JSON with the following structure:
    {{
        "title": "Video Title",
        "scenes": [
            {{
                "id": 1,
                "voiceover": "Exact text for the narrator to speak.",
                "visual_prompt": "A detailed, high-quality image generation prompt describing the visual for this scene. photorealistic, cinematic lighting.",
                "duration": 5 (estimated seconds)
            }}
        ]
    }}
    
    Do not add markdown formatting like ```json. Just return the raw JSON.
    """
    
    try:
        if not client:
             raise Exception("Google API Key not configured.")

        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        
        text_content = response.text
        
        # Cleanup potential markdown
        cleaned_text = text_content.replace("```json", "").replace("```", "").strip()
        
        # Parse JSON
        script_data = json.loads(cleaned_text)
        return script_data
        
    except Exception as e:
        print(f"CRITICAL ERROR in generate_script: {e}")
        # traceback.print_exc()
        
        # Fallback for testing/failure
        return {
            "title": "Error generating script",
            "scenes": [
                {
                    "id": 1,
                    "voiceover": "Sorry, I could not generate a script at this time. Please check the server logs.",
                    "visual_prompt": "Error message on a computer screen",
                    "duration": 5
                }
            ]
        }
