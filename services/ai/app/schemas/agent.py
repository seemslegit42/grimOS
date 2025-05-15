"""
Agent schemas for the Cognitive Core
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Literal
import uuid
from datetime import datetime


class AgentBase(BaseModel):
    """Base schema for an AI Agent"""
    name: str = Field(..., description="The name of the agent")
    description: str = Field(..., description="Description of the agent's purpose and capabilities")
    type: Literal["assistant", "autonomous", "collaborative"] = Field(
        ..., description="Type of agent: assistant (user-directed), autonomous (self-directed), collaborative (team player)"
    )
    capabilities: List[str] = Field(
        ..., description="List of capability keys this agent has access to"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Configuration parameters for the agent"
    )
    goals: Optional[List[str]] = Field(
        None, description="The agent's goals (for autonomous agents)"
    )
    model_id: str = Field(
        ..., description="The ID of the AI model to use (e.g., gpt-4, gemini-1.5-pro)"
    )
    provider: Literal["openai", "gemini", "groq", "local"] = Field(
        ..., description="The AI provider to use"
    )


class AgentCreate(AgentBase):
    """Schema for creating a new agent"""
    pass


class AgentUpdate(BaseModel):
    """Schema for updating an existing agent"""
    name: Optional[str] = None
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    parameters: Optional[Dict[str, Any]] = None
    goals: Optional[List[str]] = None
    model_id: Optional[str] = None
    provider: Optional[Literal["openai", "gemini", "groq", "local"]] = None
    is_active: Optional[bool] = None


class AgentResponse(AgentBase):
    """Schema for agent response"""
    id: uuid.UUID = Field(..., description="Unique identifier for the agent")
    created_at: datetime = Field(..., description="When the agent was created")
    updated_at: datetime = Field(..., description="When the agent was last updated")
    is_active: bool = Field(..., description="Whether the agent is active")
    owner_id: uuid.UUID = Field(..., description="ID of the user or organization that owns this agent")

    class Config:
        orm_mode = True


class AgentMemory(BaseModel):
    """Schema for agent memory operations"""
    agent_id: uuid.UUID = Field(..., description="ID of the agent")
    key: str = Field(..., description="Memory key/identifier")
    value: Dict[str, Any] = Field(..., description="Memory content")
    ttl: Optional[int] = Field(None, description="Time to live in seconds, None for permanent")


class AgentCollaborationRequest(BaseModel):
    """Schema for requesting agent collaboration"""
    initiating_agent_id: uuid.UUID = Field(..., description="ID of the initiating agent")
    target_agent_ids: List[uuid.UUID] = Field(..., description="IDs of the target agents")
    task: Dict[str, Any] = Field(..., description="The task description and parameters")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the collaboration")
