"""
Authentication and authorization for Composable Runes
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid

from app.core.config import settings

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User:
    """Simple user model for authentication purposes"""
    def __init__(self, id: uuid.UUID, username: str, email: str, role: str):
        self.id = id
        self.username = username
        self.email = email
        self.role = role


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Validate the access token and return the current user
    
    Note: In a production environment, this would verify with your auth service
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        
        # Extract user information from token
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        email: str = payload.get("email")
        role: str = payload.get("role", "user")
        
        if user_id is None:
            raise credentials_exception
            
        # Convert user_id to UUID
        try:
            user_id_uuid = uuid.UUID(user_id)
        except ValueError:
            raise credentials_exception
            
        # Create and return a user object
        return User(
            id=user_id_uuid,
            username=username,
            email=email,
            role=role
        )
        
    except jwt.JWTError:
        raise credentials_exception
