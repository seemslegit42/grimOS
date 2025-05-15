"""Profile endpoints for the Auth service."""
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.api.deps import CurrentUserDep, UserClientDep
from app.grpc.user_client import UserServiceClient
from app.models.user import User

router = APIRouter(tags=["profile"])


class UserProfileResponse(BaseModel):
    """User profile response schema."""
    user_id: str
    email: str
    full_name: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    created_at: int
    updated_at: int


class UserPreferencesResponse(BaseModel):
    """User preferences response schema."""
    user_id: str
    theme: str
    language: str
    notifications_enabled: bool
    notification_channels: List[str]
    additional_preferences: Dict[str, str]


@router.get("/me/profile", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: CurrentUserDep,
    user_client: UserClientDep,
):
    """
    Get the current user's profile from the User service.
    
    Args:
        current_user: The current user.
        user_client: The User service client.
        
    Returns:
        UserProfileResponse: The user profile.
    """
    # Get the user profile from the User service
    user_profile = user_client.get_user_profile(str(current_user.id))
    
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found",
        )
    
    # Convert the gRPC response to our Pydantic model
    return UserProfileResponse(
        user_id=user_profile.user_id,
        email=user_profile.email,
        full_name=user_profile.full_name,
        display_name=user_profile.display_name,
        avatar_url=user_profile.avatar_url,
        bio=user_profile.bio,
        location=user_profile.location,
        website=user_profile.website,
        created_at=user_profile.created_at,
        updated_at=user_profile.updated_at,
    )


@router.get("/me/preferences", response_model=UserPreferencesResponse)
async def get_my_preferences(
    current_user: CurrentUserDep,
    user_client: UserClientDep,
):
    """
    Get the current user's preferences from the User service.
    
    Args:
        current_user: The current user.
        user_client: The User service client.
        
    Returns:
        UserPreferencesResponse: The user preferences.
    """
    # Get the user preferences from the User service
    user_preferences = user_client.get_user_preferences(str(current_user.id))
    
    if not user_preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found",
        )
    
    # Convert the gRPC response to our Pydantic model
    return UserPreferencesResponse(
        user_id=user_preferences.user_id,
        theme=user_preferences.theme,
        language=user_preferences.language,
        notifications_enabled=user_preferences.notifications_enabled,
        notification_channels=list(user_preferences.notification_channels),
        additional_preferences=dict(user_preferences.additional_preferences),
    )


@router.get("/health/user-service")
async def check_user_service_health(user_client: UserClientDep):
    """
    Check the health of the User service.
    
    Args:
        user_client: The User service client.
        
    Returns:
        dict: The health check response.
    """
    health_check = user_client.health_check("auth")
    
    if not health_check or not health_check.status:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User service is not healthy",
        )
    
    return {
        "status": "ok",
        "message": health_check.message,
        "timestamp": health_check.timestamp,
    }