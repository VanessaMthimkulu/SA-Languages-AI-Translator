"""
Configuration module for loading environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    # Supabase configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    
    # CORS settings
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # Add your production frontend URL here
    ]
    
    # Supported SA languages
    SUPPORTED_LANGUAGES: dict[str, str] = {
        "isizulu": "isiZulu",
        "isixhosa": "isiXhosa",
        "sesotho": "Sesotho",
        "setswana": "Setswana",
        "sepedi": "Sepedi",
        "siswati": "siSwati",
        "tshivenda": "Tshivenda",
        "xitsonga": "Xitsonga",
        "afrikaans": "Afrikaans"
    }

# Create settings instance
settings = Settings()
