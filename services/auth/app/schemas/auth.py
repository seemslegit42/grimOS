from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import AnyUrl, BaseModel, EmailStr, Field


# Token Schema
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str  # Subject (user id)
    exp: int  # Expiration time
    type: str = "access"  # Token type (access or refresh)
    jti: Optional[str] = None  # JWT ID
    user_agent: Optional[str] = None  # User agent for refresh tokens
    ip_address: Optional[str] = None  # IP address for refresh tokens


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=100)
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


# Response models
class UserResponse(BaseModel):
    user: UserRead


class UsersResponse(BaseModel):
    items: List[UserRead]
    total: int


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None


# Service authentication schemas
class ServiceToken(BaseModel):
    token: str
    service: str
    expires_at: datetime


class ServiceTokenRequest(BaseModel):
    service_name: str
    secret_key: str


# Password reset
class PasswordReset(BaseModel):
    email: EmailStr


class NewPassword(BaseModel):
    token: str
    new_password: str


# Password update
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str
