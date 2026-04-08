"""
Text-to-Speech service using Google Translate TTS (free, no API key needed)
Falls back gracefully if unavailable.
"""
import httpx
from typing import Optional

# Google Translate TTS endpoint (free, no API key required)
GTTS_URL = "https://translate.google.com/translate_tts"

# Language code mapping for Google TTS
LANGUAGE_CODES = {
    "isizulu": "zu",
    "isixhosa": "xh",
    "sesotho": "st",
    "setswana": "tn",
    "sepedi": "nso",
    "siswati": "ss",
    "tshivenda": "ve",
    "xitsonga": "ts",
    "afrikaans": "af",
}

async def generate_speech(text: str, language: str) -> bytes:
    """
    Generate speech audio from text using Google Translate TTS (free)
    
    Args:
        text: Text to convert to speech
        language: Language code (e.g., "isizulu")
        
    Returns:
        Audio data as bytes (MP3 format)
        
    Raises:
        Exception: If TTS generation fails
    """
    try:
        # Get language code
        lang_code = LANGUAGE_CODES.get(language.lower(), "af")
        
        # Truncate text if too long (Google TTS limit ~200 chars per request)
        tts_text = text[:200] if len(text) > 200 else text
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        params = {
            "ie": "UTF-8",
            "q": tts_text,
            "tl": lang_code,
            "client": "tw-ob",
            "ttsspeed": "0.8"
        }
        
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(GTTS_URL, params=params, headers=headers)
            
            if response.status_code == 200 and len(response.content) > 0:
                print(f"✅ TTS generated: {len(response.content)} bytes for lang={lang_code}")
                return response.content
            else:
                raise Exception(f"TTS request failed: {response.status_code}")
    
    except httpx.TimeoutException:
        raise Exception("TTS request timed out")
    except Exception as e:
        print(f"❌ TTS error: {e}")
        raise Exception(f"TTS generation failed: {str(e)}")

def get_voice_for_language(language: str) -> str:
    """Get language code for TTS"""
    return LANGUAGE_CODES.get(language.lower(), "af")
