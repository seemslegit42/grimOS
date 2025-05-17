"""
OAuth 2.0 endpoints for authentication
"""
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from typing import Optional

from app.db.session import get_db
from app.db.models import User, Role
from app.core.security import create_access_token, create_refresh_token, hash_password
from app.core.oauth import oauth, get_oauth_user_info, OAUTH_PROVIDERS
from app.core.config import settings

router = APIRouter(
    prefix="/oauth",
    tags=["oauth"]
)

@router.get("/authorize/{provider}")
async def authorize(provider: str, request: Request):
    """
    Start the OAuth authorization flow by redirecting to the provider.
    
    Args:
        provider: The OAuth provider name (google, github, microsoft)
        request: The request object
    """
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {provider}"
        )
    
    client = oauth.create_client(provider)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth provider not configured: {provider}"
        )
    
    # Store the request URL so we can return to it after auth
    redirect_uri = settings.OAUTH_REDIRECT_URL
    return await client.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def oauth_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle the OAuth callback after successful authorization.
    
    Args:
        request: The request object containing the OAuth code
        db: Database session
    """
    from app.core.metrics_manager import get_metrics_manager
    metrics = get_metrics_manager()
    
    # Get the provider from query parameters
    provider = request.query_params.get("provider")
    if not provider or provider not in OAUTH_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or missing OAuth provider"
        )
    
    client = oauth.create_client(provider)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth provider not configured: {provider}"
        )
    
    # Exchange code for access token
    try:
        token = await client.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not authorize with {provider}: {str(e)}"
        )
    
    # Get user info from provider
    try:
        user_info = await get_oauth_user_info(provider, token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not get user info from {provider}: {str(e)}"
        )
    
    # Check if user exists in the database
    email = user_info.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not provided by OAuth provider"
        )
    
    existing_user = db.query(User).filter(User.email == email).first()
    
    if existing_user:
        # Update user information
        name_parts = user_info.get("name", "").split(" ", 1)
        if len(name_parts) > 0 and name_parts[0]:
            existing_user.first_name = name_parts[0]
        if len(name_parts) > 1 and name_parts[1]:
            existing_user.last_name = name_parts[1]
        
        db.commit()
        db.refresh(existing_user)
        user = existing_user
    else:
        # Create new user
        name_parts = user_info.get("name", "").split(" ", 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        # Generate a random secure password
        import secrets
        import string
        random_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        hashed_password = hash_password(random_password)
        
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            oauth_provider=provider,
            oauth_provider_id=user_info.get("provider_id")
        )
        
        db.add(new_user)
        db.flush()
        
        # Assign default 'user' role
        default_role = db.query(Role).filter(Role.name == "user").first()
        if default_role:
            new_user.roles.append(default_role)
        
        db.commit()
        db.refresh(new_user)
        user = new_user
    
    # Generate tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    # Record the successful OAuth login
    from app.core.metrics_manager import get_metrics_manager
    metrics = get_metrics_manager()
    metrics.record_oauth_login(provider)
    
    # Set tokens in cookies
    frontend_url = settings.ALLOWED_ORIGINS[0]
    redirect_url = f"{frontend_url}/auth/oauth/success?access_token={access_token}&refresh_token={refresh_token}"
    
    response = RedirectResponse(url=redirect_url)
    return response
