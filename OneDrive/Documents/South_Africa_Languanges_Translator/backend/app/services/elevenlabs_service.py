"""
ElevenLabs API service for text-to-speech generation
"""
import httpx
from app.config import settings
from typing import Optional

# ElevenLabs API configuration
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice (default)

async def generate_speech(text: str, language: str) -> bytes:
    """
    Generate speech audio from text using ElevenLabs API
    
    Args:
        text: Text to convert to speech
        language: Language of the text (for voice selection)
        
    Returns:
        Audio data as bytes (MP3 format)
        
    Raises:
        Exception: If TTS generation fails
    """
    try:
        # Select appropriate voice based on language
        voice_id = get_voice_for_language(language)
        
        # Prepare API request
        url = f"{ELEVENLABS_API_URL}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": settings.ELEVENLABS_API_KEY
        }
        
        # Use the newer free tier model
        data = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",  # Updated to free tier model
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        # Make async HTTP request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                return response.content
            else:
                error_msg = f"ElevenLabs API error: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail}"
                except:
                    pass
                raise Exception(error_msg)
    
    except httpx.TimeoutException:
        raise Exception("TTS request timed out")
    except Exception as e:
        print(f"ElevenLabs TTS error: {e}")
        raise Exception(f"TTS generation failed: {str(e)}")

def get_voice_for_language(language: str) -> str:
    """
    Select appropriate ElevenLabs voice ID based on language
    
    Args:
        language: Target language name
        
    Returns:
        Voice ID string for ElevenLabs API
    """
    # Voice mapping for different languages
    # Using default multilingual voices from ElevenLabs
    voice_map = {
        "isizulu": "21m00Tcm4TlvDq8ikWAM",      # Rachel
        "isixhosa": "AZnzlk1XvdvUeBnXmlld",     # Domi
        "sesotho": "EXAVITQu4vr4xnSDxMaL",      # Bella
        "setswana": "ErXwobaYiN019PkySvjV",     # Antoni
        "sepedi": "MF3mGyEYCl7XYWbV9V6O",       # Elli
        "siswati": "TxGEqnHWrfWFTfGW9XjX",      # Josh
        "tshivenda": "VR6AewLTigWG4xSOukaG",    # Arnold
        "xitsonga": "pNInz6obpgDQGcFmaJgB",     # Adam
        "afrikaans": "yoZ06aMxZJJ28mfd3POQ",    # Sam
    }
    
    # Return voice for language or default
    return voice_map.get(language.lower(), DEFAULT_VOICE_ID)

async def get_available_voices() -> list[dict]:
    """
    Fetch list of available voices from ElevenLabs
    
    Returns:
        List of voice information dicts
    """
    try:
        url = f"{ELEVENLABS_API_URL}/voices"
        
        headers = {
            "Accept": "application/json",
            "xi-api-key": settings.ELEVENLABS_API_KEY
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("voices", [])
            else:
                return []
    
    except Exception as e:
        print(f"Error fetching voices: {e}")
        return []
