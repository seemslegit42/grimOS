"""
Shared configuration utilities for grimOS backend services.
This module provides a base Settings class that can be extended by each service.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseServiceSettings(BaseSettings):
    """Base settings class for all grimOS services"""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "grimOS Service"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/grimos")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_CONSUMER_GROUP: str = "grimos-service"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        case_sensitive = True
        env_file = ".env"


def get_service_settings(service_name: str, **kwargs) -> BaseServiceSettings:
    """
    Create a service-specific settings instance with custom overrides.
    
    Args:
        service_name: The name of the service
        **kwargs: Additional settings to override
        
    Returns:
        A configured BaseServiceSettings instance
    """
    class ServiceSettings(BaseServiceSettings):
        PROJECT_NAME: str = f"grimOS {service_name}"
        KAFKA_CONSUMER_GROUP: str = f"grimos-{service_name.lower().replace(' ', '-')}"
        
        # Add any additional settings
        for key, value in kwargs.items():
            locals()[key] = value
    
    return ServiceSettings()