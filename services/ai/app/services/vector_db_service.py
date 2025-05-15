"""
Vector database service for managing embeddings and semantic search
"""
from typing import List, Dict, Any, Optional
import uuid
import httpx
import logging
import json
from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorDBService:
    """Service for interacting with ChromaDB for vector storage and retrieval"""
    
    def __init__(self):
        self.base_url = f"http://{settings.VECTOR_DB_HOST}:{settings.VECTOR_DB_PORT}"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def _create_collection_if_not_exists(self, collection_name: str) -> bool:
        """Create a collection if it doesn't exist"""
        try:
            # First check if collection exists
            response = await self.client.get(
                f"{self.base_url}/api/v1/collections"
            )
            
            if response.status_code == 200:
                collections = response.json()
                for collection in collections:
                    if collection.get("name") == collection_name:
                        return True
                        
            # Collection doesn't exist, create it
            response = await self.client.post(
                f"{self.base_url}/api/v1/collections",
                json={"name": collection_name, "metadata": {"hnsw:space": "cosine"}}
            )
            
            if response.status_code == 201:
                logger.info(f"Created collection: {collection_name}")
                return True
            else:
                logger.error(f"Failed to create collection: {response.status_code}, {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            return False
    
    async def add_memory(self, agent_id: str, text: str, metadata: Dict[str, Any]) -> str:
        """Add a memory to the vector database"""
        collection_name = f"agent_{agent_id}"
        
        # Create collection if it doesn't exist
        await self._create_collection_if_not_exists(collection_name)
        
        # Generate a unique ID for this memory
        memory_id = str(uuid.uuid4())
        
        try:
            # Add document to collection
            response = await self.client.post(
                f"{self.base_url}/api/v1/collections/{collection_name}/add",
                json={
                    "ids": [memory_id],
                    "documents": [text],
                    "metadatas": [metadata]
                }
            )
            
            if response.status_code == 201:
                return memory_id
            else:
                logger.error(f"Failed to add memory: {response.status_code}, {response.text}")
                raise Exception(f"Failed to add memory: {response.text}")
                
        except Exception as e:
            logger.error(f"Error adding memory: {str(e)}")
            raise
    
    async def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific memory by ID"""
        # We need to find which collection contains this memory
        try:
            collections_response = await self.client.get(
                f"{self.base_url}/api/v1/collections"
            )
            
            if collections_response.status_code != 200:
                logger.error(f"Failed to get collections: {collections_response.status_code}")
                return None
                
            collections = collections_response.json()
            
            # Search each collection for the memory ID
            for collection in collections:
                collection_name = collection.get("name")
                
                if not collection_name.startswith("agent_"):
                    continue
                    
                # Query for the specific ID
                response = await self.client.post(
                    f"{self.base_url}/api/v1/collections/{collection_name}/get",
                    json={"ids": [memory_id]}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Check if we found the memory
                    if result.get("ids") and len(result.get("ids")) > 0:
                        return {
                            "id": result["ids"][0],
                            "text": result["documents"][0],
                            "metadata": result["metadatas"][0]
                        }
            
            # Memory not found in any collection
            return None
            
        except Exception as e:
            logger.error(f"Error getting memory: {str(e)}")
            return None
    
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory from the vector database"""
        # Similar to get_memory, we need to find which collection contains this memory
        try:
            collections_response = await self.client.get(
                f"{self.base_url}/api/v1/collections"
            )
            
            if collections_response.status_code != 200:
                logger.error(f"Failed to get collections: {collections_response.status_code}")
                return False
                
            collections = collections_response.json()
            
            # Search each collection for the memory ID
            for collection in collections:
                collection_name = collection.get("name")
                
                if not collection_name.startswith("agent_"):
                    continue
                    
                # First check if the memory exists in this collection
                check_response = await self.client.post(
                    f"{self.base_url}/api/v1/collections/{collection_name}/get",
                    json={"ids": [memory_id]}
                )
                
                if check_response.status_code == 200:
                    result = check_response.json()
                    
                    # If we found the memory, delete it
                    if result.get("ids") and len(result.get("ids")) > 0:
                        delete_response = await self.client.post(
                            f"{self.base_url}/api/v1/collections/{collection_name}/delete",
                            json={"ids": [memory_id]}
                        )
                        
                        if delete_response.status_code == 200:
                            return True
            
            # Memory not found in any collection
            return False
            
        except Exception as e:
            logger.error(f"Error deleting memory: {str(e)}")
            return False
    
    async def search_memories(self, agent_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for memories similar to the query"""
        collection_name = f"agent_{agent_id}"
        
        # Check if collection exists
        collections_response = await self.client.get(
            f"{self.base_url}/api/v1/collections"
        )
        
        if collections_response.status_code != 200:
            logger.error(f"Failed to get collections: {collections_response.status_code}")
            return []
            
        collections = collections_response.json()
        collection_exists = False
        
        for collection in collections:
            if collection.get("name") == collection_name:
                collection_exists = True
                break
                
        if not collection_exists:
            return []
            
        try:
            # Perform a query
            response = await self.client.post(
                f"{self.base_url}/api/v1/collections/{collection_name}/query",
                json={
                    "query_texts": [query],
                    "n_results": limit
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Format results
                memories = []
                for i in range(len(result["ids"][0])):
                    memories.append({
                        "id": result["ids"][0][i],
                        "text": result["documents"][0][i],
                        "metadata": result["metadatas"][0][i],
                        "distance": result["distances"][0][i]
                    })
                
                return memories
            else:
                logger.error(f"Failed to search memories: {response.status_code}, {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching memories: {str(e)}")
            return []
