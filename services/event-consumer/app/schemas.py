"""Pydantic schemas for event consumer service."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Literal, Optional, Union, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator, field_validator


class UserRole(str, Enum):
    """User role enum."""
    
    USER = "user"
    ADMIN = "admin"
    SYSTEM = "system"


class UserData(BaseModel):
    """User data schema."""
    
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    roles: List[UserRole] = Field(default_factory=lambda: [UserRole.USER])
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate user ID format."""
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError("User ID must be a valid UUID")


class EventType(str, Enum):
    """Event type enum."""
    
    USER_REGISTERED = "user_registered"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_PASSWORD_CHANGED = "user_password_changed"
    USER_EMAIL_VERIFIED = "user_email_verified"


class UserEvent(BaseModel):
    """User event schema."""
    
    event_type: EventType
    user_id: str
    data: UserData
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate user ID format."""
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError("User ID must be a valid UUID")


class EventProcessingResult(BaseModel):
    """Event processing result schema."""
    
    success: bool
    message: str
    event_id: Optional[str] = None
    error: Optional[str] = None
    retry_recommended: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class EventProcessingStatistics(BaseModel):
    """Statistics for event processing."""
    
    total_processed: int = 0
    successful: int = 0
    failed: int = 0
    retried: int = 0
    event_types: Dict[str, int] = Field(default_factory=dict)
    last_event_timestamp: Optional[datetime] = None
    processing_time_ms_avg: float = 0