from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List


class Settings(BaseSettings):
    """
    Application settings
    """
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "grimOS Cognitive Core"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    SERVICE_SECRET_KEY: str = "your-service-secret-key-here"  # Change in production
    
    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/grimos"
    SQL_ECHO: bool = False
    
    # Redis settings
    REDIS_URL: str = "redis://redis:6379/1"
    
    # Vector DB settings (ChromaDB)
    VECTOR_DB_HOST: str = "chroma"
    VECTOR_DB_PORT: int = 8000
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:29092"
    KAFKA_CONSUMER_GROUP: str = "cognitive-core"
    
    # AI Provider API Keys
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    # Vercel AI SDK settings
    VERCEL_RUNTIME_TIMEOUT: int = 60  # seconds
    
    # Model configurations
    DEFAULT_OPENAI_MODEL: str = "gpt-4o"
    DEFAULT_GEMINI_MODEL: str = "gemini-1.5-pro"
    DEFAULT_GROQ_MODEL: str = "llama3-70b-8192"
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()