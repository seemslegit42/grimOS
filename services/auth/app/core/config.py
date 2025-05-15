import secrets
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
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
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 days
    SERVICE_SECRET_KEY: str = secrets.token_urlsafe(32)  # For service-to-service communication
    
    # Environment
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "auth_db"
    
    # CORS
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_USER_EVENTS_TOPIC: str = "user-events"
    KAFKA_ENABLED: bool = True
    
    # gRPC settings
    GRPC_SERVER_HOST: str = "0.0.0.0"
    GRPC_SERVER_PORT: int = 50051
    
    # User service settings
    USER_SERVICE_HOST: str = "user"
    USER_SERVICE_PORT: int = 50052
    
    # gRPC client settings
    GRPC_CLIENT_TIMEOUT: float = 5.0  # seconds
    GRPC_CLIENT_MAX_RETRIES: int = 3
    GRPC_CLIENT_RETRY_DELAY: float = 0.5  # seconds
    
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
    def USER_SERVICE_ADDRESS(self) -> str:
        return f"{self.USER_SERVICE_HOST}:{self.USER_SERVICE_PORT}"


settings = Settings()
