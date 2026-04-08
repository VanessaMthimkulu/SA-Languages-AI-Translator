"""
Translation routes using Google Gemini API
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.gemini_service import translate_text
from app.services.auth_middleware import get_current_user
from app.config import settings

router = APIRouter()

class TranslateRequest(BaseModel):
    """Request model for translation"""
    text: str
    target_language: str

class TranslateResponse(BaseModel):
    """Response model for translation"""
    original_text: str
    translated_text: str
    target_language: str

@router.post("", response_model=TranslateResponse)
async def translate(
    request: TranslateRequest,
    user: dict = Depends(get_current_user)
):
    """
    Translate English text to a South African language using Gemini API
    
    Args:
        request: Translation request with text and target language
        user: Authenticated user from JWT token
        
    Returns:
        Translated text with metadata
        
    Raises:
        HTTPException: If translation fails or language is unsupported
    """
    # Validate target language
    if request.target_language.lower() not in settings.SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported: {list(settings.SUPPORTED_LANGUAGES.values())}"
        )
    
    # Validate text length
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long (max 5000 characters)")
    
    try:
        # Get full language name
        language_name = settings.SUPPORTED_LANGUAGES[request.target_language.lower()]
        
        # Translate using Gemini
        translated = await translate_text(request.text, language_name)
        
        return TranslateResponse(
            original_text=request.text,
            translated_text=translated,
            target_language=language_name
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )
