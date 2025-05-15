"""Dependencies for the API endpoints."""
from datetime import datetime, timezone
from typing import Annotated, Generator, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.crud.user import get_user_by_id
from app.db.session import get_db
from app.grpc.user_client import UserServiceClient
from app.models.user import User
from app.schemas.auth import TokenPayload

# OAuth2 password bearer for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Database session dependency
SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_user_client() -> Generator[UserServiceClient, None, None]:
    """
    Get a User service gRPC client.
    
    Yields:
        UserServiceClient: A client for the User service.
    """
    client = UserServiceClient()
    try:
        client.connect()
        yield client
    finally:
        client.close()


def get_current_user(db: SessionDep, token: TokenDep) -> User:
    """
    Dependency to get the current user from a JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        
        # Check if token is expired
        if datetime.fromtimestamp(token_data.exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise credentials_exception
        
        # Check if token type is correct
        if token_data.type != "access":
            raise credentials_exception
        
        # Get the user_id from the token
        user_id: str = token_data.sub
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get the user from the database
    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Dependency to get the current active user.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Dependency to get the current active superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


def get_client_info(request: Request) -> tuple[Optional[str], Optional[str]]:
    """
    Extract client information from the request.
    """
    user_agent = request.headers.get("user-agent")
    
    # Get client IP, considering potential proxies
    if x_forwarded_for := request.headers.get("x-forwarded-for"):
        # Get the client's IP from the X-Forwarded-For header
        ip_address = x_forwarded_for.split(",")[0].strip()
    else:
        # Get the client's IP from the request
        ip_address = request.client.host if request.client else None
    
    return user_agent, ip_address


def validate_service_token(
    token: str, 
    required_service: Optional[str] = None
) -> dict:
    """
    Validate a service-to-service token.
    
    Args:
        token: The service token to validate
        required_service: If provided, ensures the token was issued to this service
        
    Returns:
        The decoded token payload
        
    Raises:
        HTTPException: If the token is invalid or doesn't match the required service
    """
    try:
        payload = jwt.decode(token, settings.SERVICE_SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type
        if payload.get("type") != "service":
            raise ValueError("Not a service token")
        
        # Check if token is for the required service
        if required_service and payload.get("sub") != required_service:
            raise ValueError(f"Token not issued for service: {required_service}")
            
        return payload
    except (JWTError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid service token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_service_token(token: str) -> bool:
    """
    Verify a service-to-service token.
    """
    try:
        payload = jwt.decode(token, settings.SERVICE_SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type
        if payload.get("type") != "service":
            return False
        
        # Check expiration
        exp = payload.get("exp")
        if exp is None or datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            return False
        
        return True
        
    except JWTError:
        return False


# Type aliases for dependency injection
UserClientDep = Annotated[UserServiceClient, Depends(get_user_client)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
CurrentActiveSuperuserDep = Annotated[User, Depends(get_current_active_superuser)]
