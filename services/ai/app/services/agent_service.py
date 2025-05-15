"""
Agent service for managing AI agents lifecycle
"""
from typing import List, Dict, Any, Optional, Union, Tuple
import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException, Depends, status

from app.models.agent import Agent, AgentMemoryEntry
from app.schemas.agent import AgentCreate, AgentUpdate, AgentMemory
from app.core.database import get_db
from app.services.vector_db_service import VectorDBService


class AgentService:
    """Service for managing AI agents"""
    
    def __init__(self, db: AsyncSession = Depends(get_db), vector_db: VectorDBService = Depends()):
        self.db = db
        self.vector_db = vector_db
    
    async def create_agent(self, agent_data: AgentCreate, owner_id: uuid.UUID) -> Agent:
        """Create a new agent"""
        agent = Agent(
            **agent_data.dict(),
            owner_id=owner_id
        )
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        return agent
    
    async def get_agent(self, agent_id: uuid.UUID) -> Agent:
        """Get an agent by ID"""
        result = await self.db.execute(select(Agent).filter(Agent.id == agent_id))
        agent = result.scalars().first()
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
        return agent
    
    async def update_agent(self, agent_id: uuid.UUID, agent_data: AgentUpdate) -> Agent:
        """Update an agent"""
        agent = await self.get_agent(agent_id)
        
        update_data = agent_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(agent, key, value)
        
        await self.db.commit()
        await self.db.refresh(agent)
        return agent
    
    async def delete_agent(self, agent_id: uuid.UUID) -> None:
        """Delete an agent"""
        agent = await self.get_agent(agent_id)
        await self.db.delete(agent)
        await self.db.commit()
    
    async def get_agents_by_owner(self, owner_id: uuid.UUID) -> List[Agent]:
        """Get all agents for an owner"""
        result = await self.db.execute(select(Agent).filter(Agent.owner_id == owner_id))
        return result.scalars().all()
    
    async def set_memory(self, memory: AgentMemory) -> None:
        """Store a memory for an agent - could be in regular DB or vector DB"""
        # First, check if this is a vector memory (embeddings)
        if memory.key.startswith("vector:"):
            # This is a vector memory, store in vector DB
            memory_type = "vector"
            vector_id = await self.vector_db.add_memory(
                agent_id=str(memory.agent_id),
                text=memory.value.get("text", ""),
                metadata=memory.value.get("metadata", {}),
            )
            
            # Also store reference in regular DB
            agent_memory = AgentMemoryEntry(
                agent_id=memory.agent_id,
                memory_type=memory_type,
                key=memory.key,
                value={"reference": vector_id},
                vector_id=vector_id,
            )
            
            if memory.ttl:
                agent_memory.expires_at = datetime.utcnow() + timedelta(seconds=memory.ttl)
                
            self.db.add(agent_memory)
            await self.db.commit()
            
        else:
            # Regular memory, store in database
            memory_type = "key_value"
            
            # Check if memory already exists
            result = await self.db.execute(
                select(AgentMemoryEntry).filter(
                    AgentMemoryEntry.agent_id == memory.agent_id,
                    AgentMemoryEntry.key == memory.key,
                    AgentMemoryEntry.memory_type == memory_type
                )
            )
            existing_memory = result.scalars().first()
            
            if existing_memory:
                # Update existing memory
                existing_memory.value = memory.value
                if memory.ttl:
                    existing_memory.expires_at = datetime.utcnow() + timedelta(seconds=memory.ttl)
                else:
                    existing_memory.expires_at = None
            else:
                # Create new memory
                agent_memory = AgentMemoryEntry(
                    agent_id=memory.agent_id,
                    memory_type=memory_type,
                    key=memory.key,
                    value=memory.value,
                )
                
                if memory.ttl:
                    agent_memory.expires_at = datetime.utcnow() + timedelta(seconds=memory.ttl)
                    
                self.db.add(agent_memory)
                
            await self.db.commit()
    
    async def get_memory(self, agent_id: uuid.UUID, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a memory for an agent"""
        if key.startswith("vector:"):
            # Vector memory - needs special handling
            result = await self.db.execute(
                select(AgentMemoryEntry).filter(
                    AgentMemoryEntry.agent_id == agent_id,
                    AgentMemoryEntry.key == key,
                    AgentMemoryEntry.memory_type == "vector"
                )
            )
            memory = result.scalars().first()
            
            if not memory:
                return None
                
            # Get the actual vector from vector DB
            vector_id = memory.vector_id
            vector_data = await self.vector_db.get_memory(vector_id)
            return vector_data
        else:
            # Regular key-value memory
            result = await self.db.execute(
                select(AgentMemoryEntry).filter(
                    AgentMemoryEntry.agent_id == agent_id,
                    AgentMemoryEntry.key == key,
                    AgentMemoryEntry.memory_type == "key_value"
                )
            )
            memory = result.scalars().first()
            
            if not memory:
                return None
                
            return memory.value
    
    async def delete_memory(self, agent_id: uuid.UUID, key: str) -> None:
        """Delete a memory"""
        memory_type = "vector" if key.startswith("vector:") else "key_value"
        
        result = await self.db.execute(
            select(AgentMemoryEntry).filter(
                AgentMemoryEntry.agent_id == agent_id,
                AgentMemoryEntry.key == key,
                AgentMemoryEntry.memory_type == memory_type
            )
        )
        memory = result.scalars().first()
        
        if memory:
            if memory_type == "vector":
                # Also delete from vector DB
                await self.vector_db.delete_memory(memory.vector_id)
                
            await self.db.delete(memory)
            await self.db.commit()
    
    async def search_vector_memory(self, agent_id: uuid.UUID, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search agent's vector memory using semantic search"""
        return await self.vector_db.search_memories(
            agent_id=str(agent_id),
            query=query,
            limit=limit
        )
