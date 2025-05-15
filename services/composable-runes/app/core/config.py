"""
Configuration settings for Composable Runes Service
"""
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List


class Settings(BaseSettings):
    """
    Application settings
    """
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "grimOS Composable Runes"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    SERVICE_SECRET_KEY: str = "your-service-secret-key-here"  # Change in production
      # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/grimos"
    SQL_ECHO: bool = False
    
    # Redis settings
    REDIS_URL: str = "redis://redis:6379/2"
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:29092"
    KAFKA_CONSUMER_GROUP: str = "composable-runes"
    KAFKA_TOPIC_WORKFLOW_EXECUTION: str = "workflow-execution"
    
    # Cognitive Core API
    COGNITIVE_CORE_URL: str = "http://cognitive-core:8001"
    
    # Application settings
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    MAX_WORKFLOW_EXECUTION_TIME: int = 300  # seconds
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
