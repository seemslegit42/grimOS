from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class RoleInfo(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    active: bool
    oauth_provider: Optional[str] = None
    avatar_url: Optional[str] = None
    roles: List[RoleInfo] = []
    
    class Config:
        orm_mode = True

class UserProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
