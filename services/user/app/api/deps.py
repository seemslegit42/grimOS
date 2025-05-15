"""Dependency injection utilities."""
from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.grpc.auth_client import AuthServiceClient

# OAuth2 password bearer scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Type alias for database session dependency
SessionDep = Annotated[Session, Depends(lambda: get_db())]


def get_db() -> Generator[Session, None, None]:
    """
    Get a database session.
    
    Yields:
        Session: A SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_client() -> Generator[AuthServiceClient, None, None]:
    """
    Get an Auth service gRPC client.
    
    Yields:
        AuthServiceClient: A client for the Auth service.
    """
    client = AuthServiceClient()
    try:
        client.connect()
        yield client
    finally:
        client.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_client: Annotated[AuthServiceClient, Depends(get_auth_client)],
):
    """
    Get the current user from the token.
    
    Args:
        token: The JWT token.
        auth_client: The Auth service client.
        
    Returns:
        dict: The user information.
        
    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    # Validate the token with the Auth service
    token_validation = auth_client.validate_token(token)
    
    if not token_validation or not token_validation.is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get the user from the Auth service
    user = auth_client.get_user(token_validation.user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Convert the gRPC user response to a dictionary
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
    }


async def get_current_active_user(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Get the current active user.
    
    Args:
        current_user: The current user.
        
    Returns:
        dict: The current active user.
        
    Raises:
        HTTPException: If the user is inactive.
    """
    if not current_user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    return current_user