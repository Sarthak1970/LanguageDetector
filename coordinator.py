import time
from typing import List, Dict
from connectors import (
    detect_language_gemini,
    detect_language_sarvam,
    detect_language_openai,
    detect_language_elevenlabs
)

async def coordinate_detection(audio_path: str) -> List[Dict]:
    providers = [
        ("Gemini", detect_language_gemini),
        ("Sarvam AI", detect_language_sarvam),
        ("OpenAI", detect_language_openai),
        ("ElevenLabs", detect_language_elevenlabs)
    ]
    results = []

    for provider_name, detect_func in providers:
        start_time = time.time()
        language, error_message = detect_func(audio_path)
        elapsed_time = time.time() - start_time


        result = {
            "provider": provider_name,
            "language": language,
            "time_taken": round(elapsed_time, 2),
            "estimated_cost": cost,
            "status": "success" if error_message is None else "failure",
            "error_message": error_message
        }
        results.append(result)

    return results