import os
from typing import Optional, Tuple
import google.generativeai as genai
from sarvamai import SarvamAI
from dotenv import load_dotenv

load_dotenv()

def detect_language_gemini(audio_path: str) -> Tuple[str, Optional[str]]:
    try:
        if not os.path.exists(audio_path):
            return "unknown", "Audio file not found"
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        audio_file = genai.upload_file(path=audio_path)
        prompt = "Identify the spoken language in this audio file. Return only the ISO 639-1 language code (e.g., 'en', 'hi')."
        response = model.generate_content([audio_file, prompt])
        
        language = response.text.strip()
        return language, None
    except Exception as e:
        return "unknown", f"Gemini error: {str(e)}"
    
def detect_language_sarvam(audio_path: str) -> Tuple[str, Optional[str]]:
    try:
        if not os.path.exists(audio_path):
            return "unknown", "Audio file not found"
        client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))
        with open(audio_path, "rb") as audio_file:
            response = client.speech_to_text.transcribe(
                file=audio_file,
                model="saarika:v2.5",
                language_code="unknown" 
            )
        language = response.get("language_code", "unknown").split("-")[0]
        return language, None
    except Exception as e:
        return "unknown", f"Sarvam error: {str(e)}"

def detect_language_openai(audio_path: str) -> Tuple[str, Optional[str]]:
    """Mock for OpenAI."""
    try:
        if not os.path.exists(audio_path):
            return "unknown", "Audio file not found"
        return "en", None
    except Exception as e:
        return "unknown", f"OpenAI mock error: {str(e)}"

def detect_language_elevenlabs(audio_path: str) -> Tuple[str, Optional[str]]:
    """Mock for ElevenLabs."""
    try:
        if not os.path.exists(audio_path):
            return "unknown", "Audio file not found"
        return "es", None
    except Exception as e:
        return "unknown", f"ElevenLabs mock error: {str(e)}"