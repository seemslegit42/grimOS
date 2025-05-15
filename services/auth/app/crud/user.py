"""CRUD operations for user management."""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import RefreshToken, User
from app.schemas.auth import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()


def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    email_filter: Optional[str] = None,
    active_filter: Optional[bool] = None,
) -> Tuple[List[User], int]:
    """
    Get a list of users with optional filtering.
    
    Returns:
        Tuple of (list of users, total count)
    """
    query = db.query(User)
    
    # Apply filters if provided
    if email_filter:
        query = query.filter(User.email.ilike(f"%{email_filter}%"))
    
    if active_filter is not None:
        query = query.filter(User.is_active == active_filter)
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    users = query.offset(skip).limit(limit).all()
    
    return users, total


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user.
    
    Raises:
        HTTPException: If a user with the given email already exists
    """
    # Check if user with this email already exists
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    """Update a user."""
    update_data = user_in.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        update_data["hashed_password"] = hashed_password
        del update_data["password"]
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str) -> None:
    """Delete a user."""
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_refresh_token(
    db: Session, 
    user_id: str, 
    token: str, 
    expires_in_days: int = 7,
    user_agent: Optional[str] = None,
    ip_address: Optional[str] = None
) -> RefreshToken:
    """Create a new refresh token."""
    expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
    db_token = RefreshToken(
        token=token,
        expires_at=expires_at,
        user_id=user_id,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_refresh_token(db: Session, token: str) -> Optional[RefreshToken]:
    """Get a refresh token by value."""
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def delete_refresh_token(db: Session, token: str) -> None:
    """Delete a refresh token."""
    db_token = get_refresh_token(db, token)
    if db_token:
        db.delete(db_token)
        db.commit()
