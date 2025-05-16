"""
API endpoints for workflows in Composable Runes
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.workflow import (
    WorkflowCreate, 
    WorkflowResponse, 
    WorkflowUpdate,
    WorkflowVersionCreate, 
    WorkflowVersionResponse,
    WorkflowWithDefinition,
    WorkflowExecutionCreate,
    WorkflowExecutionResponse
)
from app.services.workflow_service import WorkflowService
from app.core.database import get_db
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    workflow_service: WorkflowService = Depends()
):
    """Create a new workflow (Spell)"""
    return await workflow_service.create_workflow(workflow_data, current_user.id)


@router.get("/{workflow_id}", response_model=WorkflowWithDefinition)
async def get_workflow(
    workflow_id: uuid.UUID,
    version: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    workflow_service: WorkflowService = Depends()
):
    """Get a workflow by ID, optionally with a specific version"""
    workflow = await workflow_service.get_workflow(workflow_id)
    
    # Check access permissions (public workflows or owner)
    if not workflow.is_public and workflow.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this workflow"
        )
    
    # Get the workflow with definition if requested
    result = WorkflowWithDefinition.from_orm(workflow)
    
    if version is not None or workflow.status != "draft":
        # Get specific version or latest published
        try:
            workflow_version = await workflow_service.get_workflow_version(workflow_id, version)
            result.definition = workflow_version.definition
            result.version = workflow_version.version
        except HTTPException:
            # No versions available yet
            pass
    
    return result


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: uuid.UUID,
    workflow_data: WorkflowUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    workflow_service: WorkflowService = Depends()
):
    """Update a workflow's metadata"""
    workflow = await workflow_service.get_workflow(workflow_id)
    
    # Check ownership
    if workflow.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this workflow"
        )
    
    return await workflow_service.update_workflow(workflow_id, workflow_data)


@router.post("/{workflow_id}/versions", response_model=WorkflowVersionResponse)
async def create_workflow_version(
    workflow_id: uuid.UUID,
    version_data: WorkflowVersionCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    workflow_service: WorkflowService = Depends()
):
    """Create a new version of a workflow"""
    workflow = await workflow_service.get_workflow(workflow_id)
    
    # Check ownership
    if workflow.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this workflow"
        )
    
    return await workflow_service.create_workflow_version(
        workflow_id, 
        version_data,
        current_user.id
    )


@router.get("/{workflow_id}/versions/{version}", response_model=WorkflowVersionResponse)
async def get_workflow_version(
    workflow_id: uuid.UUID,
    version: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    workflow_service: WorkflowService = Depends()
):
    """Get a specific version of a workflow"""
    workflow = await workflow_service.get_workflow(workflow_id)
    
    # Check access permissions (public workflows or owner)
    if not workflow.is_public and workflow.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this workflow"
        )
    
    return await workflow_service.get_workflow_version(workflow_id, version)


@router.post("/{workflow_id}/execute", response_model=Dict[str, Any])
async def execute_workflow(
    workflow_id: uuid.UUID,
    execution_data: WorkflowExecutionCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    workflow_service: WorkflowService = Depends()
):
    """Execute a workflow with the given inputs"""
    workflow = await workflow_service.get_workflow(workflow_id)
    
    # Check access permissions (public workflows or owner)
    if not workflow.is_public and workflow.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to execute this workflow"
        )
    
    result = await workflow_service.execute_workflow(
        workflow_id,
        execution_data.inputs,
        current_user.id,
        execution_data.version,
        execution_data.is_async
    )
    
    if execution_data.is_async:
        # Return the execution ID for async execution
        return {"execution_id": result, "status": "pending"}
    else:
        # Return the actual result for sync execution
        return result


@router.get("/{workflow_id}/executions/{execution_id}", response_model=WorkflowExecutionResponse)
async def get_execution_status(
    workflow_id: uuid.UUID,
    execution_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    workflow_service: WorkflowService = Depends()
):
    """Get the status and result of a workflow execution"""
    workflow = await workflow_service.get_workflow(workflow_id)
    
    # Check access permissions (public workflows or owner)
    if not workflow.is_public and workflow.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this workflow execution"
        )
    
    execution = await workflow_service.get_execution(execution_id)
    
    # Verify this execution belongs to the specified workflow
    if execution.workflow_id != workflow_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found for this workflow"
        )
    
    return execution


@router.get("/", response_model=List[WorkflowResponse])
async def list_workflows(
    owner_id: Optional[uuid.UUID] = None,
    category: Optional[str] = None,
    is_public: Optional[bool] = None,
    is_template: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    workflow_service: WorkflowService = Depends()
):
    """
    List workflows with optional filters
    If owner_id is provided, returns workflows owned by that user (if public or current user is owner)
    Otherwise returns workflows owned by current user plus public workflows
    """
    # This endpoint would typically use a filter service to handle the query params
    # For now, we implement basic filtering and access control
    
    # Define the owner ID to filter by. If not provided, list current user's and public workflows.
    filter_owner_id = owner_id if owner_id else current_user.id

    workflows = await workflow_service.list_workflows(
        owner_id=filter_owner_id,
        category=category,
        is_public=is_public,
        is_template=is_template,
        current_user_id=current_user.id # Pass current user for access control
    )

    return workflows
