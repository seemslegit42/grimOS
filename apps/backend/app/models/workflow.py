from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class WorkflowDefinition(BaseModel):
    __tablename__ = "workflow_definitions"

    # Basic workflow info
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    
    # The creator of this workflow
    created_by = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Relationships
    runes = relationship("Rune", back_populates="workflow_definition", cascade="all, delete-orphan")
    instances = relationship("WorkflowInstance", back_populates="definition", cascade="all, delete-orphan")


class Rune(BaseModel):
    __tablename__ = "runes"

    # Rune identification within workflow
    workflow_definition_id = Column(UUID(as_uuid=True), ForeignKey("workflow_definitions.id"), nullable=False)
    type = Column(String, nullable=False)  # START, END, MANUAL_TASK, SIMPLE_CONDITION, BASIC_API_CALL, AGENT_TASK_STUB
    name = Column(String, nullable=False)
    
    # Configuration for the rune
    config = Column(JSONB, nullable=True)
    
    # Flow control (for MVP - simple linear and conditional flows)
    next_step_id = Column(String, nullable=True)
    condition_true_next_step_id = Column(String, nullable=True)
    condition_false_next_step_id = Column(String, nullable=True)
    
    # Relationship to workflow definition
    workflow_definition = relationship("WorkflowDefinition", back_populates="runes")


class WorkflowInstance(BaseModel):
    __tablename__ = "workflow_instances"

    # Instance identification
    definition_id = Column(UUID(as_uuid=True), ForeignKey("workflow_definitions.id"), nullable=False, index=True)
    name = Column(String, nullable=True)
    
    # Instance status
    status = Column(String, nullable=False, index=True, default="pending")  # pending, running, completed, failed, paused
    current_step_id = Column(String, nullable=True)
    
    # Instance data
    payload = Column(JSONB, nullable=True)
    result = Column(JSONB, nullable=True)
    error = Column(String, nullable=True)
    
    # Execution timestamps
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    
    # Execution log (simple for MVP)
    execution_log = Column(JSONB, nullable=True, default=list)
    
    # Relationship to workflow definition
    definition = relationship("WorkflowDefinition", back_populates="instances")
