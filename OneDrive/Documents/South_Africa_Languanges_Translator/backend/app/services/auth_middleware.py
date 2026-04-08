"""
Authentication middleware for protecting routes
"""
from fastapi import Header, HTTPException
from typing import Optional
from app.services.supabase_client import verify_token

async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    Dependency function to extract and verify user from JWT token
    
    Args:
        authorization: Bearer token from Authorization header
        
    Returns:
        User information dict
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    print(f"🔍 Authorization header: {authorization[:50] if authorization else 'None'}...")
    
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format"
        )
    
    print(f"🔑 Token extracted: {token[:50]}...")
    
    # Verify token
    user = await verify_token(token)
    
    if not user:
        print("❌ Token verification failed")
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    print(f"✅ User authenticated: {user.get('email')}")
    
    return {
        "user_id": user.get("sub"),
        "email": user.get("email"),
        "token": token
    }
