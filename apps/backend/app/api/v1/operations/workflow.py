from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, Body
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.workflow import (
    WorkflowDefinition, 
    WorkflowDefinitionCreate, 
    WorkflowDefinitionUpdate, 
    WorkflowInstance, 
    WorkflowInstanceCreate,
    TaskCompletion
)
from app.schemas.common import PaginatedResponse, PaginationMeta
from app.repositories.workflow import workflow_definition_repository, workflow_instance_repository

router = APIRouter(
    prefix="/workflows",
    tags=["operations", "workflow"],
)

# Workflow Definition endpoints
@router.post("/definitions", response_model=WorkflowDefinition, status_code=status.HTTP_201_CREATED)
async def create_workflow_definition(
    workflow_in: WorkflowDefinitionCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new workflow definition
    """
    # In a real application, we would get the user ID from the authentication token
    # For MVP, we'll use a placeholder user ID
    user_id = UUID("00000000-0000-0000-0000-000000000000")
    
    # Create the workflow definition
    workflow = workflow_definition_repository.create(db, obj_in=workflow_in)
    
    # Set the created_by field (this would ideally be handled in the create method)
    workflow.created_by = user_id
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    
    return workflow

@router.get("/definitions", response_model=PaginatedResponse)
async def get_workflow_definitions(
    db: Session = Depends(get_db),
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    """
    Retrieve a list of workflow definitions
    """
    # Get total count
    total = workflow_definition_repository.count(db)
    
    # Get data
    workflows = workflow_definition_repository.get_multi(
        db, skip=offset, limit=limit
    )
    
    # Calculate pagination metadata
    page_size = limit
    total_pages = (total + page_size - 1) // page_size
    current_page = (offset // page_size) + 1
    
    # Prepare response
    pagination = PaginationMeta(
        total_items=total,
        total_pages=total_pages,
        current_page=current_page,
        page_size=page_size,
    )
    
    return PaginatedResponse(
        data=workflows,
        pagination=pagination,
    )

@router.get("/definitions/{definition_id}", response_model=WorkflowDefinition)
async def get_workflow_definition(
    definition_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve a specific workflow definition
    """
    workflow = workflow_definition_repository.get_with_runes(db, definition_id)
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow definition with ID {definition_id} not found",
        )
    return workflow

@router.put("/definitions/{definition_id}", response_model=WorkflowDefinition)
async def update_workflow_definition(
    definition_id: UUID,
    workflow_in: WorkflowDefinitionUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing workflow definition
    """
    workflow = workflow_definition_repository.get(db, definition_id)
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow definition with ID {definition_id} not found",
        )
    
    # Update the workflow definition
    updated_workflow = workflow_definition_repository.update(db, db_obj=workflow, obj_in=workflow_in)
    
    return updated_workflow

# Workflow Instance endpoints
@router.post("/instances", response_model=WorkflowInstance, status_code=status.HTTP_201_CREATED)
async def create_workflow_instance(
    instance_in: WorkflowInstanceCreate,
    db: Session = Depends(get_db),
):
    """
    Create and start a new workflow instance from a definition
    """
    try:
        # Create the workflow instance
        instance = workflow_instance_repository.create(
            db,
            definition_id=instance_in.definition_id,
            name=instance_in.name,
            initial_payload=instance_in.initial_payload,
        )
        return instance
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get("/instances", response_model=PaginatedResponse)
async def get_workflow_instances(
    db: Session = Depends(get_db),
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,
    definition_id: Optional[UUID] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    """
    Retrieve a list of workflow instances with optional filtering
    """
    # Get total count
    total = workflow_instance_repository.count(
        db, 
        definition_id=definition_id,
        status=status,
    )
    
    # Get data
    instances = workflow_instance_repository.get_multi(
        db, 
        skip=offset, 
        limit=limit,
        definition_id=definition_id,
        status=status,
    )
    
    # Calculate pagination metadata
    page_size = limit
    total_pages = (total + page_size - 1) // page_size
    current_page = (offset // page_size) + 1
    
    # Prepare response
    pagination = PaginationMeta(
        total_items=total,
        total_pages=total_pages,
        current_page=current_page,
        page_size=page_size,
    )
    
    return PaginatedResponse(
        data=instances,
        pagination=pagination,
    )

@router.get("/instances/{instance_id}", response_model=WorkflowInstance)
async def get_workflow_instance(
    instance_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve a specific workflow instance
    """
    instance = workflow_instance_repository.get(db, instance_id)
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow instance with ID {instance_id} not found",
        )
    return instance

@router.post("/instances/{instance_id}/tasks/{task_id}/complete", response_model=WorkflowInstance)
async def complete_task(
    instance_id: UUID,
    task_id: str,
    task_completion: TaskCompletion,
    db: Session = Depends(get_db),
):
    """
    Mark a manual task within a workflow instance as complete
    """
    try:
        # Complete the task
        instance = workflow_instance_repository.update_task(
            db,
            instance_id=instance_id,
            task_id=task_id,
            outcome=task_completion.outcome,
            notes=task_completion.notes,
        )
        return instance
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
