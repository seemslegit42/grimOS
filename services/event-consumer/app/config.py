"""Configuration settings for the event consumer service."""
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_USER_EVENTS_TOPIC: str = "user-events"
    KAFKA_GROUP_ID: str = "user-events-consumer"
    KAFKA_AUTO_OFFSET_RESET: str = "earliest"
    
    # Service settings
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"


settings = Settings()