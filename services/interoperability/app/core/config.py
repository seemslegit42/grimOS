"""
Configuration settings for Interoperability Engine
"""
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List


class Settings(BaseSettings):
    """
    Application settings
    """
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "grimOS Interoperability Engine"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    SERVICE_SECRET_KEY: str = "your-service-secret-key-here"  # Change in production
    
    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/grimos"
    SQL_ECHO: bool = False
    
    # Redis settings
    REDIS_URL: str = "redis://redis:6379/3"
    
    # MongoDB settings for connector configs
    MONGO_CONNECTION_STRING: str = "mongodb://mongo:27017"
    MONGO_DB_NAME: str = "grimos_integration"
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:29092"
    KAFKA_CONSUMER_GROUP: str = "interoperability"
    
    # Credentials vault settings
    # In production, use a proper secrets manager
    CREDENTIAL_ENCRYPTION_KEY: str = "your-encryption-key-here"  # 32-byte key for AES-256
    
    # Connection pool settings
    MAX_CONNECTIONS: int = 100
    CONNECTION_TIMEOUT: int = 30  # seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
