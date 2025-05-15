"""
Connector service for the Interoperability Engine
"""
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
from cryptography.fernet import Fernet

from app.models.connector import Connector, ConnectorStatus, Credential
from app.schemas.connector import ConnectorCreate, ConnectorUpdate, CredentialCreate, ConnectorTestRequest
from app.core.database import get_db, get_mongo_db
from app.core.config import settings


class ConnectorService:
    """Service for managing integration connectors"""
    
    def __init__(
        self, 
        db: AsyncSession = Depends(get_db),
        mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)
    ):
        self.db = db
        self.mongo_db = mongo_db
        self.credential_key = Fernet(settings.CREDENTIAL_ENCRYPTION_KEY.encode())
    
    async def create_connector(self, connector_data: ConnectorCreate, owner_id: uuid.UUID) -> Connector:
        """Create a new connector"""
        # Create connector instance
        connector = Connector(
            name=connector_data.name,
            description=connector_data.description,
            type=connector_data.type,
            system_name=connector_data.system_name,
            auth_config=connector_data.auth_config.dict(),
            base_config=connector_data.base_config,
            operations=json.dumps([op.dict() for op in connector_data.operations]),
            tags=connector_data.tags,
            is_custom=connector_data.is_custom,
            status=ConnectorStatus.ACTIVE,
            owner_id=owner_id
        )
        
        # Add to database
        self.db.add(connector)
        await self.db.commit()
        await self.db.refresh(connector)
        
        # If connector has custom configurations, store them in MongoDB
        if connector_data.base_config:
            await self.mongo_db.connector_configs.insert_one({
                "connector_id": str(connector.id),
                "config": connector_data.base_config,
                "created_at": datetime.utcnow()
            })
        
        return connector
    
    async def get_connector(self, connector_id: uuid.UUID) -> Connector:
        """Get a connector by ID"""
        result = await self.db.execute(
            select(Connector).where(Connector.id == connector_id)
        )
        connector = result.scalars().first()
        
        if not connector:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Connector with ID {connector_id} not found"
            )
            
        return connector
    
    async def update_connector(self, connector_id: uuid.UUID, connector_data: ConnectorUpdate) -> Connector:
        """Update a connector"""
        # Get current connector
        connector = await self.get_connector(connector_id)
        
        # Update fields if provided
        update_data = {}
        for field, value in connector_data.dict(exclude_unset=True).items():
            if field == "operations" and value is not None:
                update_data[field] = json.dumps([op.dict() for op in value])
            elif value is not None:
                update_data[field] = value
        
        # Update in database
        if update_data:
            await self.db.execute(
                update(Connector)
                .where(Connector.id == connector_id)
                .values(**update_data)
            )
            await self.db.commit()
            await self.db.refresh(connector)
        
        # Update MongoDB config if needed
        if connector_data.base_config:
            await self.mongo_db.connector_configs.update_one(
                {"connector_id": str(connector.id)},
                {
                    "$set": {
                        "config": connector_data.base_config,
                        "updated_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
        
        return connector
    
    async def delete_connector(self, connector_id: uuid.UUID) -> None:
        """Delete a connector"""
        connector = await self.get_connector(connector_id)
        
        # Delete from database
        await self.db.execute(
            delete(Connector).where(Connector.id == connector_id)
        )
        await self.db.commit()
        
        # Delete MongoDB config
        await self.mongo_db.connector_configs.delete_one({"connector_id": str(connector_id)})
    
    async def list_connectors(
        self, 
        owner_id: Optional[uuid.UUID] = None,
        system_name: Optional[str] = None,
        connector_type: Optional[str] = None,
        is_custom: Optional[bool] = None,
        tags: Optional[List[str]] = None
    ) -> List[Connector]:
        """List connectors with optional filters"""
        query = select(Connector)
        
        # Apply filters
        if owner_id:
            query = query.where(Connector.owner_id == owner_id)
        if system_name:
            query = query.where(Connector.system_name == system_name)
        if connector_type:
            query = query.where(Connector.type == connector_type)
        if is_custom is not None:
            query = query.where(Connector.is_custom == is_custom)
            
        # Execute query
        result = await self.db.execute(query)
        connectors = result.scalars().all()
        
        # Filter by tags if provided
        if tags:
            filtered_connectors = []
            for connector in connectors:
                if set(tags).issubset(set(connector.tags)):
                    filtered_connectors.append(connector)
            return filtered_connectors
        
        return list(connectors)
    
    async def create_credential(self, credential_data: CredentialCreate, owner_id: uuid.UUID) -> Credential:
        """Create a new credential with encrypted data"""
        # Encrypt sensitive data
        encrypted_data = self.encrypt_credential_data(credential_data.data)
        
        # Create credential instance
        credential = Credential(
            name=credential_data.name,
            description=credential_data.description,
            type=credential_data.type,
            data=encrypted_data,
            tags=credential_data.tags,
            owner_id=owner_id
        )
        
        # Add to database
        self.db.add(credential)
        await self.db.commit()
        await self.db.refresh(credential)
        
        return credential
    
    def encrypt_credential_data(self, data: Dict[str, Any]) -> str:
        """Encrypt credential data"""
        json_data = json.dumps(data)
        encrypted_data = self.credential_key.encrypt(json_data.encode())
        return encrypted_data.decode()
    
    def decrypt_credential_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt credential data"""
        decrypted_data = self.credential_key.decrypt(encrypted_data.encode())
        return json.loads(decrypted_data.decode())
    
    async def test_connector(self, test_data: ConnectorTestRequest) -> Dict[str, Any]:
        """Test a connector with optional input data"""
        # If connector_id is provided, test an existing connector
        if test_data.connector_id:
            connector = await self.get_connector(test_data.connector_id)
            # Get connector config from MongoDB
            config = await self.mongo_db.connector_configs.find_one(
                {"connector_id": str(connector.id)}
            )
            
            # TODO: Implement actual connector testing logic
            # For now, return a mock response
            return {
                "success": True,
                "message": f"Successfully tested connector: {connector.name}",
                "details": {
                    "connector_id": str(connector.id),
                    "type": connector.type,
                    "system": connector.system_name,
                    "test_result": "Connection successful"
                }
            }
        
        # If connector_config is provided, test a config before saving
        elif test_data.connector_config:
            # TODO: Implement config testing logic
            return {
                "success": True,
                "message": "Configuration tested successfully",
                "details": {
                    "type": test_data.connector_config.type,
                    "system": test_data.connector_config.system_name,
                    "test_result": "Configuration valid"
                }
            }
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either connector_id or connector_config must be provided"
            )
