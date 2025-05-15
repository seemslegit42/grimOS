"""User profile endpoints."""
from typing import Annotated, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.api.deps import get_current_active_user, get_auth_client
from app.grpc.auth_client import AuthServiceClient

router = APIRouter(tags=["profile"])


class UserProfileUpdate(BaseModel):
    """User profile update schema."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserProfileResponse(BaseModel):
    """User profile response schema."""
    id: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: Annotated[Dict, Depends(get_current_active_user)],
):
    """
    Get the current user's profile.
    
    Args:
        current_user: The current user.
        
    Returns:
        UserProfileResponse: The user profile.
    """
    return UserProfileResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        is_active=current_user["is_active"],
        is_superuser=current_user["is_superuser"],
    )


@router.put("/me", response_model=UserProfileResponse)
async def update_my_profile(
    profile_update: UserProfileUpdate,
    current_user: Annotated[Dict, Depends(get_current_active_user)],
    auth_client: Annotated[AuthServiceClient, Depends(get_auth_client)],
):
    """
    Update the current user's profile.
    
    Args:
        profile_update: The profile update data.
        current_user: The current user.
        auth_client: The Auth service client.
        
    Returns:
        UserProfileResponse: The updated user profile.
        
    Raises:
        HTTPException: If the update fails.
    """
    # Update the user in the Auth service
    updated_user = auth_client.update_user(
        user_id=current_user["id"],
        email=profile_update.email,
        password=profile_update.password,
        full_name=profile_update.full_name,
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile",
        )
    
    return UserProfileResponse(
        id=updated_user.id,
        email=updated_user.email,
        full_name=updated_user.full_name,
        is_active=updated_user.is_active,
        is_superuser=updated_user.is_superuser,
    )