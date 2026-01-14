from gtts import gTTS
import os

def generate_audio(text: str, output_path: str):
    """
    Generates MP3 audio from text using Google Text-to-Speech (gTTS).
    """
    try:
        tts = gTTS(text, lang='en')
        tts.save(output_path)
        return True
    except Exception as e:
        print(f"Error generating audio: {e}")
        return False
