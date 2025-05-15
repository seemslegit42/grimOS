from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

# Workflow models
class RuneConfigBase(BaseModel):
    # This will have type-specific fields based on Rune type
    pass

class RuneBase(BaseModel):
    id: str  # Unique within the workflow definition
    type: str  # START, END, MANUAL_TASK, SIMPLE_CONDITION, BASIC_API_CALL, AGENT_TASK_STUB
    name: str
    config: Optional[Dict[str, Any]] = None
    next_step_id: Optional[str] = None  # For linear MVP workflows
    condition_true_next_step_id: Optional[str] = None  # For SIMPLE_CONDITION
    condition_false_next_step_id: Optional[str] = None  # For SIMPLE_CONDITION

class WorkflowDefinitionBase(BaseModel):
    name: str
    description: Optional[str] = None
    runes: List[RuneBase]

class WorkflowDefinitionCreate(WorkflowDefinitionBase):
    pass

class WorkflowDefinitionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    runes: Optional[List[RuneBase]] = None

class WorkflowDefinition(WorkflowDefinitionBase):
    id: UUID
    version: int
    created_at: datetime
    updated_at: datetime
    created_by: UUID

    class Config:
        from_attributes = True

class WorkflowInstanceCreate(BaseModel):
    definition_id: UUID
    name: Optional[str] = None
    initial_payload: Optional[Dict[str, Any]] = None

class ExecutionLogEntry(BaseModel):
    step_id: str
    status: str
    message: str
    timestamp: datetime

class WorkflowInstance(BaseModel):
    id: UUID
    definition_id: UUID
    definition_name: str
    name: Optional[str] = None
    status: str  # pending, running, completed, failed, paused
    current_step_id: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_at: datetime
    execution_log: List[ExecutionLogEntry]

    class Config:
        from_attributes = True

class TaskCompletion(BaseModel):
    outcome: str  # e.g., approved, rejected
    notes: Optional[str] = None
