from fastapi import APIRouter, HTTPException, status, Depends
from app.api.v1.auth.schemas import UserLoginRequest, TokenResponse
from app.db.session import SessionLocal
from app.db.models import User
from app.core.security import verify_password, create_access_token, create_refresh_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login_user(user: UserLoginRequest):
    """Authenticate user and issue JWTs."""
    with SessionLocal() as db:
        # Check if user exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        # Generate tokens
        access_token = create_access_token(data={"sub": db_user.email})
        refresh_token = create_refresh_token(data={"sub": db_user.email})

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
