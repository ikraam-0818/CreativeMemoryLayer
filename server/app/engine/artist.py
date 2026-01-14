import os
from google import genai
from google.genai import types
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = None
if api_key:
    client = genai.Client(api_key=api_key)

def generate_image(prompt: str, output_path: str):
    """
    Generates an image using Google Imagen 3 (via google-genai SDK).
    """
    if not client:
        print("Error: No API Key")
        return False
        
    try:
        print(f"🎨 Generating Image: {prompt[:30]}...")
        # Try Imagen 3 model ID
        model_id = "imagen-4.0-generate-001"
        
        response = client.models.generate_images(
            model=model_id,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        
        # Check generated_images
        if response.generated_images:
            img_bytes = response.generated_images[0].image.image_bytes
            image = Image.open(io.BytesIO(img_bytes))
            image.save(output_path)
            print("✅ Image Generated")
            return True
        else:
            print("No images returned.")
            return False

    except Exception as e:
        print(f"Error generating image: {e}")
        return False
