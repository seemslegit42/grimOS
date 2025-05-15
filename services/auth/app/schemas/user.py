from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """Base User schema"""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """User update schema with all optional fields"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=100)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserInDBBase(UserBase):
    """Schema for User model as stored in DB"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserPublic(UserInDBBase):
    """Schema for public user data (returned via API)"""
    # Exclude sensitive fields from the response
    pass


class UserWithRefreshTokens(UserInDBBase):
    """Schema for user with refresh tokens"""
    refresh_tokens: List["RefreshTokenRead"] = []


class RefreshTokenBase(BaseModel):
    """Base Refresh Token schema"""
    token: str
    expires_at: datetime
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None


class RefreshTokenCreate(RefreshTokenBase):
    """Schema for creating a new refresh token"""
    user_id: uuid.UUID


class RefreshTokenRead(RefreshTokenBase):
    """Schema for reading refresh token data"""
    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID

    class Config:
        orm_mode = True


# Update forward references
UserWithRefreshTokens.update_forward_refs()
