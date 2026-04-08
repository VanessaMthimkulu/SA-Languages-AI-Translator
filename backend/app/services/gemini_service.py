"""
Google Gemini API service for text translation
"""
import google.generativeai as genai
from app.config import settings
from typing import Optional

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

# List available models and use the first one that supports generateContent
available_models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            print(f"📋 Available model: {m.name}")
except Exception as e:
    print(f"⚠️ Could not list models: {e}")

# Use the first available model or fallback
if available_models:
    model_name = available_models[0]
    print(f"✅ Using model: {model_name}")
else:
    model_name = "gemini-pro"
    print(f"⚠️ Using fallback model: {model_name}")

model = genai.GenerativeModel(model_name)

async def translate_text(text: str, target_language: str) -> str:
    """
    Translate English text to a South African language using Gemini
    
    Args:
        text: English text to translate
        target_language: Target SA language name (e.g., "isiZulu")
        
    Returns:
        Translated text string
        
    Raises:
        Exception: If translation fails
    """
    try:
        # Create translation prompt
        prompt = f"""Translate the following English text to {target_language}.
Only provide the translation, no explanations or additional text.

English text: {text}

{target_language} translation:"""
        
        # Generate translation using Gemini
        response = model.generate_content(prompt)
        
        # Extract translated text
        if response and response.text:
            translated = response.text.strip()
            return translated
        else:
            raise Exception("No translation received from Gemini")
    
    except Exception as e:
        print(f"Gemini translation error: {e}")
        raise Exception(f"Translation failed: {str(e)}")

async def translate_with_context(
    text: str,
    target_language: str,
    context: Optional[str] = None
) -> str:
    """
    Translate with additional context for better accuracy
    
    Args:
        text: English text to translate
        target_language: Target SA language name
        context: Optional context about the text (e.g., "formal", "casual")
        
    Returns:
        Translated text string
    """
    try:
        # Enhanced prompt with context
        prompt = f"""Translate the following English text to {target_language}.
{f'Context: {context}' if context else ''}
Provide only the translation, maintaining the tone and meaning.

English: {text}

{target_language}:"""
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            raise Exception("No translation received")
    
    except Exception as e:
        print(f"Context translation error: {e}")
        raise Exception(f"Translation failed: {str(e)}")
