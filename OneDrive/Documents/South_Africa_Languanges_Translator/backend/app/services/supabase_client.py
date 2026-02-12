"""
Supabase client for authentication and database operations
"""
import httpx
from app.config import settings
import jwt
from typing import Optional

# Supabase REST API endpoints
SUPABASE_REST_URL = f"{settings.SUPABASE_URL}/rest/v1"
SUPABASE_AUTH_URL = f"{settings.SUPABASE_URL}/auth/v1"

# Headers for Supabase requests
def get_supabase_headers(user_token: Optional[str] = None) -> dict:
    """Get headers for Supabase API requests"""
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
    }
    if user_token:
        headers["Authorization"] = f"Bearer {user_token}"
    return headers

async def verify_token(token: str) -> Optional[dict]:
    """
    Verify a Supabase JWT token and return user information
    
    Args:
        token: JWT token string from Authorization header
        
    Returns:
        User information dict if valid, None if invalid
    """
    try:
        # Decode JWT to get user info
        decoded = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        
        # Check if token has required fields
        if not decoded.get("sub") or not decoded.get("email"):
            print("❌ Token missing required fields")
            return None
        
        print(f"✅ Token decoded successfully for user: {decoded.get('email')}")
        return decoded
    
    except jwt.ExpiredSignatureError:
        print("❌ Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print("❌ Invalid token: {e}")
        return None
    except Exception as e:
        print(f"❌ Token verification error: {e}")
        return None

# Database operations using REST API
async def insert_translation_history(
    user_id: str,
    original_text: str,
    translated_text: str,
    target_language: str,
    user_token: str,
    audio_url: Optional[str] = None
) -> dict:
    """Insert a translation into history using Supabase REST API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_REST_URL}/translation_history",
                headers=get_supabase_headers(user_token),
                json={
                    "user_id": user_id,
                    "original_text": original_text,
                    "translated_text": translated_text,
                    "target_language": target_language,
                    "audio_url": audio_url
                }
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise Exception(f"Failed to insert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Insert error: {e}")
        raise

async def get_translation_history(
    user_id: str,
    user_token: str,
    limit: int = 20,
    offset: int = 0
) -> list:
    """Get translation history using Supabase REST API"""
    try:
        async with httpx.AsyncClient() as client:
            # Supabase REST API query
            url = f"{SUPABASE_REST_URL}/translation_history"
            headers = get_supabase_headers(user_token)
            params = {
                "user_id": f"eq.{user_id}",
                "order": "created_at.desc",
                "limit": limit,
                "offset": offset,
                "select": "*"
            }
            
            print(f"📋 Fetching history: {url}")
            print(f"📋 Params: {params}")
            
            response = await client.get(url, headers=headers, params=params)
            
            print(f"📋 Response status: {response.status_code}")
            print(f"📋 Response body: {response.text[:200]}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to fetch: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Fetch error: {e}")
        raise

async def delete_translation_history(
    history_id: str,
    user_id: str,
    user_token: str
) -> bool:
    """Delete a translation from history using Supabase REST API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{SUPABASE_REST_URL}/translation_history",
                headers=get_supabase_headers(user_token),
                params={
                    "id": f"eq.{history_id}",
                    "user_id": f"eq.{user_id}"
                }
            )
            
            if response.status_code in [200, 204]:
                return True
            else:
                raise Exception(f"Failed to delete: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Delete error: {e}")
        raise

print("✅ Supabase REST client initialized")
