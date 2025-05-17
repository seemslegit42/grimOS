"""User management endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import SessionDep, get_current_active_user, get_current_active_superuser
from app.core.security import verify_password, get_password_hash
from app.crud.user import (
    create_user,
    delete_user,
    get_user_by_id,
    get_user_by_email,
    get_users,
    update_user,
    change_user_password,
    delete_user_refresh_tokens,
)
from app.models.user import User
from app.schemas.auth import (
    MessageResponse,
    PasswordChange,
    UserCreate,
    UserRead,
    UserUpdate,
    UsersResponse,
)

router = APIRouter(tags=["users"])


@router.get("/", response_model=UsersResponse)
async def read_users(
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_superuser)],
    skip: int = 0,
    limit: int = 100,
    email: str = Query(None, description="Filter by email (partial match)"),
    is_active: bool = Query(None, description="Filter by active status"),
) -> UsersResponse:
    """
    Retrieve users with pagination and filtering. Only accessible to superusers.
    """
    users, total = get_users(
        db, 
        skip=skip, 
        limit=limit,
        email_filter=email,
        active_filter=is_active,
    )
    
    return UsersResponse(
        items=[
            UserRead(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ],
        total=total,
    )


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    db: SessionDep,
    user_in: UserCreate,
    current_user: Annotated[User, Depends(get_current_active_superuser)],
) -> UserRead:
    """
    Create a new user. Only accessible to superusers.
    """
    # Check if email is already registered
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
        
    # Create the user
    user = create_user(db=db, user_in=user_in)
    
    return UserRead(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: str,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserRead:
    """
    Get a specific user by ID.
    Users can get their own user information.
    Superusers can get any user's information.
    """
    # Check if the user is trying to access their own info or if they're a superuser
    if str(current_user.id) != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return UserRead(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.put("/{user_id}", response_model=UserRead)
async def update_user_info(
    user_id: str,
    user_in: UserUpdate,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserRead:
    """
    Update a user.
    Users can update their own information.
    Superusers can update any user's information.
    """
    # Check if the user to update is the current user or the current user is a superuser
    if str(current_user.id) != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
        
    user = get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
        
    # If the user is not a superuser, they can't update the is_superuser field
    if not current_user.is_superuser and user_in.is_superuser is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Regular users cannot modify superuser status",
        )
        
    user = update_user(db=db, db_user=user, user_in=user_in)
    
    return UserRead(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.delete("/{user_id}", response_model=Message)
async def delete_user_by_id(
    user_id: str,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_superuser)],
) -> Message:
    """
    Delete a user. Only accessible to superusers.
    """
    user = get_user(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
        
    delete_user(db=db, user_id=user_id)
    
    return Message(detail="User deleted successfully")


@router.put("/me/password", response_model=Message)
async def update_password(
    password_update: PasswordUpdate,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Message:
    """
    Update current user's password.
    """
    # Verify current password
    if not verify_password(password_update.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )
        
    # Update password
    user_in = UserUpdate(password=password_update.new_password)
    update_user(db=db, db_user=current_user, user_in=user_in)
    
    return Message(detail="Password updated successfully")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    db: SessionDep,
    user_in: UserCreate,
) -> UserRead:
    """
    Register a new user.
    """
    # Check if email is already registered
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash the password
    hashed_password = get_password_hash(user_in.password)
    user_in.password = hashed_password

    # Create the user
    user = create_user(db=db, user_in=user_in)

    return UserRead(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
