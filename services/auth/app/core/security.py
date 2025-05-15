from datetime import datetime, timedelta, timezone
import uuid
from typing import Any, Dict, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"


def create_access_token(subject: str, expires_delta: timedelta | None = None, extra_data: Dict[str, Any] = None) -> str:
    """
    Create a JWT access token
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.now(timezone.utc) + expires_delta
    
    to_encode = {
        "exp": expire, 
        "sub": str(subject),
        "type": "access",
        "jti": str(uuid.uuid4())
    }
    
    if extra_data:
        to_encode.update(extra_data)
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str, user_agent: Optional[str] = None, ip_address: Optional[str] = None) -> str:
    """
    Create a JWT refresh token with longer expiration
    """
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.now(timezone.utc) + expires_delta
    
    jti = str(uuid.uuid4())
    
    to_encode = {
        "exp": expire, 
        "sub": str(subject),
        "type": "refresh",
        "jti": jti
    }
    
    if user_agent:
        to_encode["user_agent"] = user_agent
    
    if ip_address:
        to_encode["ip_address"] = ip_address
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT token and return its payload
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Invalid token")


def create_service_token(service_name: str, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token for service-to-service authentication
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=60)  # Default 1 hour
    
    expire = datetime.now(timezone.utc) + expires_delta
    
    to_encode = {
        "exp": expire,
        "sub": service_name,
        "type": "service",
        "jti": str(uuid.uuid4())
    }
    
    return jwt.encode(to_encode, settings.SERVICE_SECRET_KEY, algorithm=ALGORITHM)


def verify_service_token(token: str) -> Dict[str, Any]:
    """
    Verify a service-to-service JWT token
    """
    try:
        payload = jwt.decode(token, settings.SERVICE_SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "service":
            raise ValueError("Not a service token")
        return payload
    except JWTError:
        raise ValueError("Invalid service token")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)


def create_service_token(service_name: str, expires_delta: timedelta | None = None) -> str:
    """
    Create a token for service-to-service communication
    """
    if expires_delta is None:
        expires_delta = timedelta(days=1)  # Default 1 day for service tokens
    
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "exp": expire,
        "service": service_name,
        "type": "service"
    }
    
    return jwt.encode(to_encode, settings.SERVICE_SECRET_KEY, algorithm=ALGORITHM)
