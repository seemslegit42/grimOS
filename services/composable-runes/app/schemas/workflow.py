"""
Schemas for Composable Runes workflows
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime
from enum import Enum


class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    TIMEOUT = "timeout"


class WorkflowBase(BaseModel):
    """Base schema for workflow data"""
    name: str = Field(..., description="Name of the workflow")
    description: Optional[str] = Field(None, description="Description of what the workflow does")
    category: Optional[str] = Field(None, description="Category for organization")
    tags: List[str] = Field(default_factory=list, description="Tags for classification and search")
    is_public: bool = Field(default=False, description="Whether the workflow is visible to other users")
    is_template: bool = Field(default=False, description="Whether this is a template workflow")


class WorkflowCreate(WorkflowBase):
    """Schema for creating a new workflow"""
    definition: Optional[Dict[str, Any]] = Field(
        None,
        description="The workflow definition in n8n workflow JSON format"
    )


class WorkflowUpdate(BaseModel):
    """Schema for updating an existing workflow"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[WorkflowStatus] = None
    is_public: Optional[bool] = None
    is_template: Optional[bool] = None


class WorkflowVersionCreate(BaseModel):
    """Schema for creating a new version of a workflow"""
    definition: Dict[str, Any] = Field(..., description="The workflow definition")
    comment: Optional[str] = Field(None, description="Comment about changes in this version.")


class WorkflowVersionResponse(BaseModel):
    """Schema for workflow version response"""
    id: uuid.UUID
    workflow_id: uuid.UUID
    version: int
    definition: Dict[str, Any]
    comment: Optional[str] = None
    created_by: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True


class WorkflowResponse(WorkflowBase):
    """Schema for workflow response"""
    id: uuid.UUID
    owner_id: uuid.UUID
    status: WorkflowStatus
    created_at: datetime
    updated_at: datetime
    latest_version: Optional[int] = None

    class Config:
        orm_mode = True


class WorkflowWithDefinition(WorkflowResponse):
    """Schema for workflow with its definition included"""
    definition: Optional[Dict[str, Any]] = None
    version: Optional[int] = None


class WorkflowExecutionCreate(BaseModel):
    """Schema for triggering workflow execution"""
    inputs: Dict[str, Any] = Field(..., description="Input parameters for the workflow")
    version: Optional[int] = Field(None, description="Specific version to execute, or latest if not provided")
    is_async: bool = Field(default=False, description="Whether to run asynchronously")


class WorkflowExecutionResponse(BaseModel):
    """Schema for workflow execution response"""
    id: uuid.UUID
    workflow_id: uuid.UUID
    version: int
    inputs: Dict[str, Any]
    outputs: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status: ExecutionStatus
    initiated_by: uuid.UUID
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class RuneDefinitionBase(BaseModel):
    """Base schema for rune component definition"""
    name: str
    description: Optional[str] = None
    category: str
 definition: Optional[Dict[str, Any]] = Field(
 None,
 description="The rune definition (inputs, outputs, logic), possibly including n8n node configuration"
 )

    is_public: bool = False
    version: str


class RuneDefinitionCreate(RuneDefinitionBase):
    """Schema for creating a new rune component"""
    pass


class RuneDefinitionResponse(RuneDefinitionBase):
    """Schema for rune component response"""
    id: uuid.UUID
    creator_id: uuid.UUID
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    # Fields for n8n integration
 n8n_node_type: Optional[str] = Field(
 None, description="The type of n8n node corresponding to this rune"
 )
 n8n_node_config: Optional[Dict[str, Any]] = Field(
 None, description="The JSON configuration for the n8n node"
 )
 input_mapping: Optional[Dict[str, str]] = Field(
 None, description="Mapping from workflow inputs to n8n node parameters"
 )
 output_mapping: Optional[Dict[str, str]] = Field(
 None, description="Mapping from n8n node outputs to workflow outputs"
 )
    class Config:
        orm_mode = True
