"""
API endpoints for connectors in the Interoperability Engine
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.connector import (
    ConnectorCreate, 
    ConnectorResponse, 
    ConnectorUpdate,
    CredentialCreate,
    CredentialResponse,
    ConnectorTestRequest
)
from app.services.connector_service import ConnectorService
from app.core.database import get_db, get_mongo_db
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=ConnectorResponse, status_code=status.HTTP_201_CREATED)
async def create_connector(
    connector_data: ConnectorCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    connector_service: ConnectorService = Depends()
):
    """Create a new connector for external system integration"""
    return await connector_service.create_connector(connector_data, current_user.id)


@router.get("/{connector_id}", response_model=ConnectorResponse)
async def get_connector(
    connector_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    connector_service: ConnectorService = Depends()
):
    """Get a connector by ID"""
    connector = await connector_service.get_connector(connector_id)
    
    # Check access permissions (only owner can access)
    if connector.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this connector"
        )
    
    return connector


@router.put("/{connector_id}", response_model=ConnectorResponse)
async def update_connector(
    connector_id: uuid.UUID,
    connector_data: ConnectorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    connector_service: ConnectorService = Depends()
):
    """Update a connector"""
    connector = await connector_service.get_connector(connector_id)
    
    # Check ownership
    if connector.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this connector"
        )
    
    return await connector_service.update_connector(connector_id, connector_data)


@router.delete("/{connector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connector(
    connector_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    connector_service: ConnectorService = Depends()
):
    """Delete a connector"""
    connector = await connector_service.get_connector(connector_id)
    
    # Check ownership
    if connector.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this connector"
        )
    
    await connector_service.delete_connector(connector_id)
    return None


@router.get("/", response_model=List[ConnectorResponse])
async def list_connectors(
    system_name: Optional[str] = None,
    connector_type: Optional[str] = None,
    is_custom: Optional[bool] = None,
    tags: Optional[List[str]] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    connector_service: ConnectorService = Depends()
):
    """
    List connectors with optional filters
    Returns connectors owned by current user
    """
    return await connector_service.list_connectors(
        owner_id=current_user.id,
        system_name=system_name,
        connector_type=connector_type,
        is_custom=is_custom,
        tags=tags
    )


@router.post("/credentials", response_model=CredentialResponse, status_code=status.HTTP_201_CREATED)
async def create_credential(
    credential_data: CredentialCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    connector_service: ConnectorService = Depends()
):
    """Create a new credential for connector authentication"""
    return await connector_service.create_credential(credential_data, current_user.id)


@router.post("/test", response_model=Dict[str, Any])
async def test_connector(
    test_data: ConnectorTestRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    connector_service: ConnectorService = Depends()
):
    """Test a connector with optional input data"""
    # If testing an existing connector, verify ownership
    if test_data.connector_id:
        connector = await connector_service.get_connector(test_data.connector_id)
        if connector.owner_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to test this connector"
            )
    
    return await connector_service.test_connector(test_data)
