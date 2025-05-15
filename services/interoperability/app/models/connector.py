"""
Database models for the Interoperability Engine
"""
from sqlalchemy import Column, String, Boolean, JSON, ForeignKey, DateTime, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from enum import Enum as PyEnum
from datetime import datetime

from app.core.database import Base


class ConnectorType(str, PyEnum):
    REST_API = "rest_api"
    SOAP = "soap"
    DATABASE = "database"
    FILE = "file"
    EVENT = "event"
    MESSAGE_QUEUE = "message_queue"
    CUSTOM = "custom"


class AuthType(str, PyEnum):
    NONE = "none"
    API_KEY = "api_key"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    CERTIFICATE = "certificate"
    CUSTOM = "custom"


class ConnectorStatus(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class Connector(Base):
    """Integration connector model"""
    __tablename__ = "connectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(SQLEnum(ConnectorType), nullable=False)
    system_name = Column(String(255), nullable=False)
    auth_config = Column(JSON, nullable=False)
    base_config = Column(JSON, nullable=False, default=dict)
    operations = Column(JSON, nullable=False, default=list)
    tags = Column(JSON, nullable=False, default=list)
    is_custom = Column(Boolean, default=False)
    status = Column(SQLEnum(ConnectorStatus), default=ConnectorStatus.ACTIVE, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_connection_time = Column(DateTime(timezone=True), nullable=True)


class Credential(Base):
    """Secure credential storage for connectors"""
    __tablename__ = "credentials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(SQLEnum(AuthType), nullable=False)
    data = Column(String, nullable=False)  # Encrypted credential data
    tags = Column(JSON, nullable=False, default=list)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Note: Sensitive data should be encrypted at rest


class Integration(Base):
    """Integration between systems using connectors"""
    __tablename__ = "integrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source_connector_id = Column(UUID(as_uuid=True), ForeignKey("connectors.id"), nullable=False)
    target_connector_id = Column(UUID(as_uuid=True), ForeignKey("connectors.id"), nullable=False)
    configuration = Column(JSON, nullable=False)  # Full integration configuration
    status = Column(String(50), default="enabled", nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_run_time = Column(DateTime(timezone=True), nullable=True)
    last_run_status = Column(String(50), nullable=True)


class IntegrationLog(Base):
    """Logs for integration executions"""
    __tablename__ = "integration_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    integration_id = Column(UUID(as_uuid=True), ForeignKey("integrations.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), nullable=False)
    message = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)  # Detailed execution information
    records_processed = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
