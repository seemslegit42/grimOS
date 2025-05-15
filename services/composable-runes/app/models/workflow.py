"""
Database models for the Composable Runes workflows
"""
from sqlalchemy import Column, String, Boolean, JSON, ForeignKey, Integer, DateTime, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from enum import Enum as PyEnum
from datetime import datetime

from app.core.database import Base


class WorkflowStatus(str, PyEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class ExecutionStatus(str, PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    TIMEOUT = "timeout"


class Workflow(Base):
    """Workflow (Spell) model for database"""
    __tablename__ = "workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category = Column(String(100), nullable=True)
    tags = Column(JSON, nullable=False, default=list)
    status = Column(SQLEnum(WorkflowStatus), default=WorkflowStatus.DRAFT, nullable=False)
    is_public = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WorkflowVersion(Base):
    """Version control for workflow definitions"""
    __tablename__ = "workflow_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False)
    version = Column(Integer, nullable=False)
    definition = Column(JSONB, nullable=False)  # The actual workflow definition (nodes, connections, etc.)
    comment = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        # Composite unique constraint on workflow_id and version
        {'unique_together': ('workflow_id', 'version')}
    )


class WorkflowExecution(Base):
    """Record of workflow executions"""
    __tablename__ = "workflow_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"), nullable=False)
    version = Column(Integer, nullable=False)  # Which version was executed
    inputs = Column(JSONB, nullable=False)
    outputs = Column(JSONB, nullable=True)
    error = Column(Text, nullable=True)
    status = Column(SQLEnum(ExecutionStatus), nullable=False)
    initiated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    

class WorkflowStep(Base):
    """Individual step/node in a workflow execution (for detailed execution logs)"""
    __tablename__ = "workflow_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("workflow_executions.id", ondelete="CASCADE"), nullable=False)
    step_id = Column(String(255), nullable=False)  # ID of the step in the workflow definition
    step_type = Column(String(100), nullable=False)  # Type of step (e.g., 'api', 'transformation', 'condition')
    inputs = Column(JSONB, nullable=True)
    outputs = Column(JSONB, nullable=True)
    error = Column(Text, nullable=True)
    status = Column(SQLEnum(ExecutionStatus), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)  # Duration in milliseconds


class RuneDefinition(Base):
    """Reusable component (Rune) that can be used in workflows"""
    __tablename__ = "rune_definitions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    definition = Column(JSONB, nullable=False)  # The rune definition (inputs, outputs, logic)
    is_public = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    version = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
