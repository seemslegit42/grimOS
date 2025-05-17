from pydantic_settings import BaseSettings
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GrimOS API"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/grimos")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Frontend URL for redirects
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # OAuth
    OAUTH_PROVIDERS: Dict[str, Dict[str, Any]] = {
        "google": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
            "client_kwargs": {"scope": "openid email profile"}
        },
        "github": {
            "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
            "client_secret": os.getenv("GITHUB_CLIENT_SECRET", ""),
            "access_token_url": "https://github.com/login/oauth/access_token",
            "authorize_url": "https://github.com/login/oauth/authorize",
            "api_base_url": "https://api.github.com/",
            "client_kwargs": {"scope": "user:email"}
        },
        "microsoft": {
            "client_id": os.getenv("MICROSOFT_CLIENT_ID", ""),
            "client_secret": os.getenv("MICROSOFT_CLIENT_SECRET", ""),
            "server_metadata_url": "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration",
            "client_kwargs": {"scope": "openid email profile"}
        }
    }

    class Config:
        case_sensitive = True


settings = Settings()