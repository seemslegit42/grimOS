"""
Agent models for the database
"""
from sqlalchemy import Column, String, Boolean, JSON, ForeignKey, Enum, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from enum import Enum as PyEnum

from app.core.database import Base


class AgentType(str, PyEnum):
    ASSISTANT = "assistant"
    AUTONOMOUS = "autonomous"
    COLLABORATIVE = "collaborative"


class AgentProvider(str, PyEnum):
    OPENAI = "openai"
    GEMINI = "gemini"
    GROQ = "groq"
    LOCAL = "local"


class Agent(Base):
    """Agent model for database"""
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(Enum(AgentType), nullable=False)
    capabilities = Column(JSON, nullable=False, default=list)
    parameters = Column(JSON, nullable=False, default=dict)
    goals = Column(JSON, nullable=True)
    model_id = Column(String(255), nullable=False)
    provider = Column(Enum(AgentProvider), nullable=False)
    is_active = Column(Boolean, default=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AgentMemoryEntry(Base):
    """Agent memory entry in database"""
    __tablename__ = "agent_memory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    memory_type = Column(String(50), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(JSON, nullable=False)
    vector_id = Column(String(255), nullable=True)  # ID in the vector database if applicable
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)  # For TTL-based memories

    __table_args__ = (
        # Composite index for faster lookups
        {'postgresql_partition_by': 'LIST (memory_type)'}
    )


class AgentConversation(Base):
    """Agent conversation history"""
    __tablename__ = "agent_conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    messages = Column(JSON, nullable=False, default=list)
    metadata = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
