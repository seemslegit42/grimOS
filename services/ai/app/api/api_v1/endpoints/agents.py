"""
Agent API routes for the Cognitive Core
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate, AgentMemory
from app.services.agent_service import AgentService
from app.core.database import get_db
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """Create a new agent"""
    return await agent_service.create_agent(agent_data, current_user.id)


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """Get an agent by ID"""
    agent = await agent_service.get_agent(agent_id)
    
    # Check if user has access to this agent
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this agent"
        )
        
    return agent


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: uuid.UUID,
    agent_data: AgentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """Update an existing agent"""
    agent = await agent_service.get_agent(agent_id)
    
    # Check if user has access to this agent
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this agent"
        )
        
    return await agent_service.update_agent(agent_id, agent_data)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """Delete an agent"""
    agent = await agent_service.get_agent(agent_id)
    
    # Check if user has access to this agent
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this agent"
        )
        
    await agent_service.delete_agent(agent_id)
    return None


@router.get("/", response_model=List[AgentResponse])
async def get_user_agents(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """Get all agents for the current user"""
    return await agent_service.get_agents_by_owner(current_user.id)


@router.post("/{agent_id}/memory", status_code=status.HTTP_204_NO_CONTENT)
async def set_agent_memory(
    agent_id: uuid.UUID,
    memory_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """Store a memory for an agent"""
    agent = await agent_service.get_agent(agent_id)
    
    # Check if user has access to this agent
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this agent's memory"
        )
        
    memory = AgentMemory(
        agent_id=agent_id,
        key=memory_data.get("key"),
        value=memory_data.get("value"),
        ttl=memory_data.get("ttl")
    )
    
    await agent_service.set_memory(memory)
    return None


@router.get("/{agent_id}/memory/{key}", response_model=Dict[str, Any])
async def get_agent_memory(
    agent_id: uuid.UUID,
    key: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """Retrieve a memory for an agent"""
    agent = await agent_service.get_agent(agent_id)
    
    # Check if user has access to this agent
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this agent's memory"
        )
        
    memory = await agent_service.get_memory(agent_id, key)
    
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found"
        )
        
    return memory


@router.delete("/{agent_id}/memory/{key}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_memory(
    agent_id: uuid.UUID,
    key: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """Delete a memory for an agent"""
    agent = await agent_service.get_agent(agent_id)
    
    # Check if user has access to this agent
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this agent's memory"
        )
        
    await agent_service.delete_memory(agent_id, key)
    return None


@router.post("/{agent_id}/memory/search", response_model=List[Dict[str, Any]])
async def search_agent_memory(
    agent_id: uuid.UUID,
    search_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """Search an agent's vector memory using semantic search"""
    agent = await agent_service.get_agent(agent_id)
    
    # Check if user has access to this agent
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this agent's memory"
        )
        
    query = search_data.get("query")
    limit = search_data.get("limit", 5)
    
    results = await agent_service.search_vector_memory(agent_id, query, limit)
    return results
