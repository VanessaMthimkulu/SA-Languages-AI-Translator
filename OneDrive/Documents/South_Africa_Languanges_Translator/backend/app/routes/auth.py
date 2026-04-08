"""
Authentication routes for verifying Supabase JWT tokens
"""
from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.services.supabase_client import verify_token

router = APIRouter()

@router.post("/verify")
async def verify_auth(authorization: Optional[str] = Header(None)):
    """
    Verify Supabase JWT token from Authorization header
    
    Args:
        authorization: Bearer token from request header
        
    Returns:
        User information if token is valid
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    # Extract token from "Bearer <token>" format
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    # Verify token with Supabase
    user = await verify_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {
        "user_id": user.get("sub"),
        "email": user.get("email"),
        "verified": True
    }
