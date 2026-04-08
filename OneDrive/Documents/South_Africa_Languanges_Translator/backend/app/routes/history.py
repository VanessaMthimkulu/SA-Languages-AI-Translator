"""
Translation history routes for saving and retrieving user translations
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.services.supabase_client import (
    insert_translation_history,
    get_translation_history,
    delete_translation_history
)
from app.services.auth_middleware import get_current_user

router = APIRouter()

class SaveHistoryRequest(BaseModel):
    """Request model for saving translation history"""
    original_text: str
    translated_text: str
    target_language: str
    audio_url: Optional[str] = None

class HistoryItem(BaseModel):
    """Model for a single history item"""
    id: str
    original_text: str
    translated_text: str
    target_language: str
    audio_url: Optional[str]
    created_at: str

@router.post("/save")
async def save_history(
    request: SaveHistoryRequest,
    user: dict = Depends(get_current_user)
):
    """
    Save a translation to user's history in Supabase
    
    Args:
        request: Translation data to save
        user: Authenticated user from JWT token
        
    Returns:
        Saved history item with ID
        
    Raises:
        HTTPException: If save operation fails
    """
    try:
        # Insert using REST API
        result = await insert_translation_history(
            user_id=user["user_id"],
            original_text=request.original_text,
            translated_text=request.translated_text,
            target_language=request.target_language,
            user_token=user["token"],
            audio_url=request.audio_url
        )
        
        return {
            "success": True,
            "id": result[0]["id"] if isinstance(result, list) and result else None,
            "message": "Translation saved to history"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save history: {str(e)}"
        )

@router.get("/get")
async def get_history(
    user: dict = Depends(get_current_user),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0)
):
    """
    Retrieve user's translation history with pagination
    
    Args:
        user: Authenticated user from JWT token
        limit: Maximum number of items to return (max 100)
        offset: Number of items to skip for pagination
        
    Returns:
        List of translation history items
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        print(f"📋 Fetching history for user: {user['user_id']}")
        
        # Query using REST API
        result = await get_translation_history(
            user_id=user["user_id"],
            user_token=user["token"],
            limit=limit,
            offset=offset
        )
        
        print(f"✅ Retrieved {len(result)} history items")
        
        return {
            "history": result,
            "count": len(result),
            "limit": limit,
            "offset": offset
        }
    
    except Exception as e:
        print(f"❌ History retrieval error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve history: {str(e)}"
        )

@router.delete("/delete/{history_id}")
async def delete_history(
    history_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Delete a specific translation from user's history
    
    Args:
        history_id: UUID of the history item to delete
        user: Authenticated user from JWT token
        
    Returns:
        Success confirmation
        
    Raises:
        HTTPException: If deletion fails
    """
    try:
        # Delete using REST API
        await delete_translation_history(
            history_id=history_id,
            user_id=user["user_id"],
            user_token=user["token"]
        )
        
        return {
            "success": True,
            "message": "History item deleted"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete history: {str(e)}"
        )
