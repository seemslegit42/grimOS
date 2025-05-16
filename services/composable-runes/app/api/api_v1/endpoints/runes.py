"""
API endpoints for Runes (reusable workflow components) in Composable Runes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Union
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.workflow import RuneDefinitionCreate, RuneDefinitionResponse
from app.services.workflow_service import WorkflowAndRuneService # Use the renamed service
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.workflow import RuneDefinition # Import the model

router = APIRouter()

@router.post("/", response_model=RuneDefinitionResponse, status_code=status.HTTP_201_CREATED)
async def create_rune_definition(
    rune_data: RuneDefinitionCreate,
    current_user=Depends(get_current_user),
    service: WorkflowAndRuneService = Depends(),
):
    """Create a new Rune definition"""
 return await service.create_rune(rune_data, current_user.id)

@router.get("/{rune_id}", response_model=RuneDefinitionResponse)
async def get_rune_definition(
    rune_id: uuid.UUID,
    current_user=Depends(get_current_user),
    service: WorkflowAndRuneService = Depends(),
):
    """Get a Rune definition by ID"""
 rune = await service.get_rune(rune_id)
    # Basic access control (creator or public/verified)
    if not rune.is_public and not rune.is_verified and rune.creator_id != current_user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this rune definition"
        )
    return RuneDefinitionResponse.from_orm(rune)


@router.get("/", response_model=List[RuneDefinitionResponse])
async def list_rune_definitions(
    category: Optional[str] = None,
    is_public: Optional[bool] = None,
    current_user=Depends(get_current_user),
    service: WorkflowAndRuneService = Depends(),
):
    """List Rune definitions with optional filters"""
 return await service.list_runes(category=category, is_public=is_public, current_user_id=current_user.id)