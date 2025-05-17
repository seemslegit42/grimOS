"""
Frontend integration utilities for OAuth authentication
"""
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from app.db.session import get_db
from app.core.oauth import OAUTH_PROVIDERS
from app.core.config import settings

router = APIRouter(
    prefix="/frontend",
    tags=["oauth-frontend"]
)

@router.get("/providers")
async def get_oauth_providers():
    """
    Get the list of available and configured OAuth providers.
    This endpoint is used by the frontend to show available login options.
    
    Returns:
        List of provider information with configured status
    """
    providers = []
    
    for provider in OAUTH_PROVIDERS:
        # Check if provider is properly configured
        client_id = settings.OAUTH_PROVIDERS.get(provider, {}).get("client_id", "")
        client_secret = settings.OAUTH_PROVIDERS.get(provider, {}).get("client_secret", "")
        
        is_configured = bool(client_id and client_secret)
        
        providers.append({
            "name": provider,
            "displayName": provider.capitalize(),
            "isConfigured": is_configured,
            "authUrl": f"/api/v1/auth/oauth/authorize/{provider}" if is_configured else None,
        })
    
    return {"providers": providers}

@router.get("/user-data")
async def get_frontend_user_data(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Get user data after successful OAuth login.
    This endpoint is called by the frontend after receiving the access token.
    
    Args:
        request: The request object with Authorization header
        db: Database session
        
    Returns:
        User data for frontend display
    """
    # Get the token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    
    # Use existing token verification logic
    from app.core.security import verify_token
    
    try:
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        
        # Get user from database
        from app.db.models import User
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Return user data for frontend
        return {
            "id": user.id,
            "email": user.email,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "profilePicture": None,  # Add profile picture if available
            "oauthProvider": user.oauth_provider
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error verifying token: {str(e)}"
        )
