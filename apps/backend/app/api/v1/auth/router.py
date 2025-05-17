from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.api.v1.auth.schemas import (
    UserCreateRequest, UserResponse, TokenResponse, 
    UserProfileResponse, UserProfileUpdateRequest, UserLoginRequest
)
from app.db.session import get_db
from app.db.models import User, Role
from app.core.security import hash_password, verify_token, create_access_token, create_refresh_token, verify_password
from app.api.v1.security.auth import get_current_user
from sqlalchemy.orm import Session
from app.api.v1.auth.oauth import router as oauth_router
from app.api.v1.auth.frontend_integration import router as frontend_router
from app.api.v1.security.rbac import router as rbac_router
from app.core.metrics_manager import get_metrics_manager

router = APIRouter()

# Get metrics manager
metrics = get_metrics_manager()

# Include OAuth, frontend integration, and RBAC routers
router.include_router(oauth_router)
router.include_router(frontend_router)
router.include_router(rbac_router)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create new user
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(new_user)
    db.flush()
    
    # Assign default 'user' role to new user
    default_role = db.query(Role).filter(Role.name == "user").first()
    if default_role:
        new_user.roles.append(default_role)
    
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=TokenResponse)
async def login_user(user_login: UserLoginRequest, db: Session = Depends(get_db)):
    """Login a user and return JWT tokens."""
    # Find user by email
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(user_login.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: Request):
    """Refresh the access token using a valid refresh token."""
    refresh_token = request.headers.get("Authorization")
    if not refresh_token or not refresh_token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing refresh token."
        )

    token = refresh_token.split(" ")[1]
    try:
        payload = verify_token(token)
        new_access_token = create_access_token({"sub": payload["sub"]})
        return {"access_token": new_access_token, "refresh_token": token}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get("/me", response_model=UserProfileResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile."""
    return current_user

@router.put("/me", response_model=UserProfileResponse)
async def update_user_profile(
    profile_update: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the current user's profile."""
    # Get a fresh copy from the database to avoid SQLAlchemy column assignment issues
    user = db.query(User).filter(User.id == current_user.id).first()
    
    # Update user fields
    if profile_update.first_name:
        setattr(user, "first_name", profile_update.first_name)
        
    if profile_update.last_name:
        setattr(user, "last_name", profile_update.last_name)
    
    # Update password if provided
    if profile_update.password:
        setattr(user, "hashed_password", hash_password(profile_update.password))
    
    # Update avatar URL if provided
    if profile_update.avatar_url:
        setattr(user, "avatar_url", profile_update.avatar_url)
    
    db.commit()
    db.refresh(user)
    
    # Record metric for profile update
    metrics.record_user_activity("profile_update", str(user.id))
    
    return user
