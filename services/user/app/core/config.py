"""Configuration settings for the User service."""
import secrets
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "user_db"
    
    # CORS
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_USER_EVENTS_TOPIC: str = "user-events"
    KAFKA_ENABLED: bool = True
    
    # gRPC settings
    AUTH_SERVICE_HOST: str = "auth"
    AUTH_SERVICE_PORT: int = 50051
    GRPC_SERVER_HOST: str = "0.0.0.0"
    GRPC_SERVER_PORT: int = 50052
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            path=f"{self.POSTGRES_DB}",
        )
    
    @computed_field
    @property
    def AUTH_SERVICE_ADDRESS(self) -> str:
        return f"{self.AUTH_SERVICE_HOST}:{self.AUTH_SERVICE_PORT}"


settings = Settings()