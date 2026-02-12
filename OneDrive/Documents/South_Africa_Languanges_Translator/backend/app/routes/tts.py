"""
Text-to-Speech routes using ElevenLabs API
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from pydantic import BaseModel
from app.services.elevenlabs_service import generate_speech
from app.services.auth_middleware import get_current_user

router = APIRouter()

class TTSRequest(BaseModel):
    """Request model for text-to-speech"""
    text: str
    language: str

@router.post("")
async def text_to_speech(
    request: TTSRequest,
    user: dict = Depends(get_current_user)
):
    """
    Convert translated text to speech using ElevenLabs API
    
    Args:
        request: TTS request with text and language
        user: Authenticated user from JWT token
        
    Returns:
        Audio file as MP3 bytes with base64 encoding
        
    Raises:
        HTTPException: If TTS generation fails
    """
    # Validate text
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long (max 5000 characters)")
    
    try:
        # Generate speech audio
        audio_data = await generate_speech(request.text, request.language)
        
        # Return audio as base64 encoded string for easy frontend handling
        import base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return {
            "audio": audio_base64,
            "format": "mp3",
            "text": request.text
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"TTS generation failed: {str(e)}"
        )
