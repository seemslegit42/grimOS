"""Authentication endpoints."""
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep, get_client_info, get_current_active_user
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token as create_refresh_token_jwt,
    decode_token,
)
from app.crud.user import (
    authenticate_user,
    create_refresh_token,
    delete_refresh_token,
    get_refresh_token,
    get_user_by_id,
)
from app.models.user import User
from app.schemas.auth import (
    LogoutRequest,
    MessageResponse,
    RefreshRequest,
    TokenResponse,
    UserLogin,
    UserRead,
)

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(
    request: Request,
    db: SessionDep,
    user_login: UserLogin,
) -> TokenResponse:
    """
    User login endpoint to get access and refresh tokens.
    """
    user = authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Get client info for the refresh token
    user_agent, ip_address = get_client_info(request)
    
    # Create the tokens
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires,
    )
    
    refresh_token_jwt = create_refresh_token_jwt(
        subject=str(user.id),
        user_agent=user_agent,
        ip_address=ip_address,
    )
    
    # Store refresh token in the database
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    create_refresh_token(
        db,
        user_id=user.id,
        token=refresh_token_jwt,
        expires_at=expires_at,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    
    # Create user object for response
    user_data = UserRead(
        id=str(user.id),
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        full_name=user.full_name,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_jwt,
        token_type="bearer",
        user=user_data,
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    db: SessionDep,
    refresh_token: RefreshRequest,
) -> Token:
    """
    Refresh access token using a refresh token.
    """
    # Get the refresh token from the database
    db_token = get_refresh_token(db, refresh_token.refresh_token)
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if the token is expired
    if db_token.expires_at < datetime.now(timezone.utc):
        delete_refresh_token(db, refresh_token.refresh_token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(db_token.user_id),
        expires_delta=access_token_expires,
    )
    
    # Create new refresh token
    new_refresh_token_jwt = create_refresh_token_jwt(str(db_token.user_id))
    
    # Get client info for tracking
    user_agent, ip_address = get_client_info(request)
    
    # Store new refresh token in database
    create_refresh_token(
        db=db,
        user_id=str(db_token.user_id),
        token=new_refresh_token_jwt,
        expires_in_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    
    # Delete old refresh token
    delete_refresh_token(db, refresh_token.refresh_token)
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token_jwt,
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    db: SessionDep,
    refresh_token: RefreshRequest,
) -> MessageResponse:
    """
    Logout by invalidating the refresh token.
    """
    # Delete the refresh token from the database
    delete_refresh_token(db, refresh_token.refresh_token)
    
    return MessageResponse(message="Successfully logged out")


@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserRead:
    """
    Get current user information.
    """
    return UserRead(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
    )
