"""
Workflow service for the Composable Runes module
"""
from typing import Dict, List, Any, Optional, Union
import uuid
from datetime import datetime, timezone
import httpx
import os
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.workflow import (
    RuneDefinition,
    Workflow, 
    WorkflowVersion, 
    WorkflowExecution,
    WorkflowStatus,
    ExecutionStatus
)
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowVersionCreate,
    WorkflowResponse,
    RuneDefinitionCreate,
    WorkflowVersionResponse,
    WorkflowExecutionResponse,
    RuneDefinitionResponse,
)
from app.core.database import get_db
from sqlalchemy.sql.expression import and_

class WorkflowService:
    """Service for managing workflows"""
    
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def create_workflow(self, workflow_data: WorkflowCreate, owner_id: uuid.UUID) -> Workflow:
        """Create a new workflow"""
        # Create workflow instance
        workflow = Workflow(
            name=workflow_data.name,
            description=workflow_data.description,
            owner_id=owner_id,
            category=workflow_data.category,
            tags=workflow_data.tags,
            is_public=workflow_data.is_public,
            is_template=workflow_data.is_template,
            status=WorkflowStatus.DRAFT
        )
        
        # Add to database
        self.db.add(workflow)
        await self.db.commit()
        await self.db.refresh(workflow)
        
        # If definition is provided, create first version
        if workflow_data.definition:
            await self.create_workflow_version(
                workflow.id,
                WorkflowVersionCreate(
                    definition=workflow_data.definition,
                    comment="Initial version"
                ),
                owner_id
            )
        
        return workflow
    
    async def get_workflow(self, workflow_id: uuid.UUID) -> Workflow:
        """Get a workflow by ID"""
        result = await self.db.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        workflow = result.scalars().first()
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow with ID {workflow_id} not found"
            )
            
        return workflow
    
    async def update_workflow(self, workflow_id: uuid.UUID, workflow_data: WorkflowUpdate) -> Workflow:
        """Update a workflow's metadata"""
        # Get current workflow
        workflow = await self.get_workflow(workflow_id)
        
        # Update fields if provided
        update_data = {}
        if workflow_data.name is not None:
            update_data["name"] = workflow_data.name
        if workflow_data.description is not None:
            update_data["description"] = workflow_data.description
        if workflow_data.category is not None:
            update_data["category"] = workflow_data.category
        if workflow_data.tags is not None:
            update_data["tags"] = workflow_data.tags
        if workflow_data.status is not None:
            update_data["status"] = workflow_data.status
        if workflow_data.is_public is not None:
            update_data["is_public"] = workflow_data.is_public
        if workflow_data.is_template is not None:
            update_data["is_template"] = workflow_data.is_template
        
        # Update in database
        if update_data:
            await self.db.execute(
                update(Workflow)
                .where(Workflow.id == workflow_id)
                .values(**update_data)
            )
            await self.db.commit()
            await self.db.refresh(workflow)
        
        return workflow
    
    async def create_workflow_version(
        self, 
        workflow_id: uuid.UUID, 
        version_data: WorkflowVersionCreate,
        created_by: uuid.UUID
    ) -> WorkflowVersion:
        """Create a new version of a workflow"""
        # Get current workflow
        workflow = await self.get_workflow(workflow_id)
        
        # Get latest version number
        latest_version = await self.get_latest_version_number(workflow_id)
        new_version = latest_version + 1 if latest_version is not None else 1
        
        # Create new version
        workflow_version = WorkflowVersion(
            workflow_id=workflow_id,
            version=new_version,
            definition=version_data.definition,
            comment=version_data.comment,
            created_by=created_by
        )
        
        # Add to database
        self.db.add(workflow_version)
        await self.db.commit()
        await self.db.refresh(workflow_version)
        
        return workflow_version
    
    async def get_latest_version_number(self, workflow_id: uuid.UUID) -> Optional[int]:
        """Get the latest version number for a workflow"""
        result = await self.db.execute(
            select(WorkflowVersion.version)
            .where(WorkflowVersion.workflow_id == workflow_id)
            .order_by(WorkflowVersion.version.desc())
            .limit(1)
        )
        latest = result.scalars().first()
        return latest
    
    async def get_workflow_version(self, workflow_id: uuid.UUID, version: Optional[int] = None) -> WorkflowVersion:
        """Get a specific version of a workflow"""
        # If version is not specified, get the latest
        if version is None:
            latest_version = await self.get_latest_version_number(workflow_id)
            if latest_version is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No versions found for workflow {workflow_id}"
                )
            version = latest_version
        
        # Query for the specific version
        result = await self.db.execute(
            select(WorkflowVersion)
            .where(
                WorkflowVersion.workflow_id == workflow_id,
                WorkflowVersion.version == version
            )
        )
        workflow_version = result.scalars().first()
        
        if not workflow_version:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Version {version} not found for workflow {workflow_id}"
            )
            
        return workflow_version
    
    async def execute_workflow(
        self,
        workflow_id: uuid.UUID,
        inputs: Dict[str, Any],
        user_id: uuid.UUID,
        version: Optional[int] = None,
        is_async: bool = False
    ) -> Any:
        """
        Execute a workflow with the given inputs
        
        If is_async is True, returns the execution ID
        Otherwise, executes synchronously and returns the result
        """
        # Get workflow and version
        workflow = await self.get_workflow(workflow_id)
        workflow_version = await self.get_workflow_version(workflow_id, version)
        
        # Create execution record
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            version=workflow_version.version,
            inputs=inputs,
            status=ExecutionStatus.PENDING,
            initiated_by=user_id,
        )
        
        self.db.add(execution)
        await self.db.commit()
        await self.db.refresh(execution)

        if is_async:
            # Start background task for execution
            # In a real implementation, this would use a task queue
            # self.background_tasks.add_task(self._execute_workflow_async, execution.id)
            return execution.id
        else:
            # Execute synchronously
            result = await self._execute_workflow(execution.id)
            return result
    
    async def _execute_workflow(self, execution_id: uuid.UUID) -> Dict[str, Any]:
        """Internal method to execute a workflow"""
        # Get execution record
        result = await self.db.execute(
 select(WorkflowExecution).where(WorkflowExecution.id == execution_id)
        )
        execution = result.scalars().first()

        if not execution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Execution with ID {execution_id} not found"
            )

        # Update status to running
        execution.status = ExecutionStatus.RUNNING
        await self.db.commit()

        try:
            # Get workflow definition
            workflow_version = await self.get_workflow_version(
 execution.workflow_id,
                execution.version
            )

            # Execute the workflow in n8n
            n8n_response = await self._execute_workflow_in_n8n(
 workflow_version.definition, execution.inputs
 )

            # Update execution record with results
            # Assuming n8n's execution API returns the final output in the response body
            execution.outputs = n8n_response # Adjust based on actual n8n response structure
            execution.status = ExecutionStatus.COMPLETED
            execution.completed_at = datetime.now(timezone.utc)
 await self.db.commit()

 return n8n_response

        except Exception as e:
            # Update execution record with error
            execution.error = str(e)
            execution.status = ExecutionStatus.FAILED
            execution.completed_at = datetime.now(timezone.utc)
 await self.db.commit()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Workflow execution failed: {str(e)}"
            )

    async def get_execution(self, execution_id: uuid.UUID) -> WorkflowExecution:
        """Get the status and result of a workflow execution"""
        result = await self.db.execute(
 select(WorkflowExecution).where(WorkflowExecution.id == execution_id)
        )
        execution = result.scalars().first()

        if not execution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Execution with ID {execution_id} not found"
            )
from sqlalchemy.ext.asyncio import AsyncSession


class WorkflowAndRuneService:
    """Service for managing workflows and runes in Composable Runes"""

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    # --- Workflow Methods (Keep existing methods, but use the new class name) ---
    async def create_workflow(self, workflow_data: WorkflowCreate, owner_id: uuid.UUID) -> Workflow:
 """Create a new workflow"""
 # Create workflow instance
 workflow = Workflow(
 name=workflow_data.name,
 description=workflow_data.description,
 owner_id=owner_id,
 category=workflow_data.category,
 tags=workflow_data.tags,
 is_public=workflow_data.is_public,
 is_template=workflow_data.is_template,
 status=WorkflowStatus.DRAFT
 )

 # Add to database
 self.db.add(workflow)
 await self.db.commit()
 await self.db.refresh(workflow)

 # If definition is provided, create first version
 if workflow_data.definition:
 await self.create_workflow_version(
 workflow.id,
 WorkflowVersionCreate(
 definition=workflow_data.definition,
 comment="Initial version"
 ),
 owner_id
 )

 return workflow

 async def get_workflow(self, workflow_id: uuid.UUID) -> Workflow:
 """Get a workflow by ID"""
 result = await self.db.execute(
 select(Workflow).where(Workflow.id == workflow_id)
 )
 workflow = result.scalars().first()

 if not workflow:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail=f"Workflow with ID {workflow_id} not found"
 )

 return workflow

 async def update_workflow(self, workflow_id: uuid.UUID, workflow_data: WorkflowUpdate) -> Workflow:
 """Update a workflow's metadata"""
 # Get current workflow
 workflow = await self.get_workflow(workflow_id)

 # Update fields if provided
 update_data = {}
 if workflow_data.name is not None:
 update_data["name"] = workflow_data.name
 if workflow_data.description is not None:
 update_data["description"] = workflow_data.description
 if workflow_data.category is not None:
 update_data["category"] = workflow_data.category
 if workflow_data.tags is not None:
 update_data["tags"] = workflow_data.tags
 if workflow_data.status is not None:
 update_data["status"] = workflow_data.status
 if workflow_data.is_public is not None:
 update_data["is_public"] = workflow_data.is_public
 if workflow_data.is_template is not None:
 update_data["is_template"] = workflow_data.is_template

 # Update in database
 if update_data:
 await self.db.execute(
 update(Workflow)
 .where(Workflow.id == workflow_id)
 .values(**update_data)
 )
 await self.db.commit()
 await self.db.refresh(workflow)

 return workflow

 async def create_workflow_version(
 self,
 workflow_id: uuid.UUID,
 version_data: WorkflowVersionCreate,
 created_by: uuid.UUID
 ) -> WorkflowVersion:
 """Create a new version of a workflow"""
 # Get current workflow
 workflow = await self.get_workflow(workflow_id)

 # Get latest version number
 latest_version = await self.get_latest_version_number(workflow_id)
 new_version = latest_version + 1 if latest_version is not None else 1

 # Create new version
 workflow_version = WorkflowVersion(
 workflow_id=workflow_id,
 version=new_version,
 definition=version_data.definition,
 comment=version_data.comment,
 created_by=created_by
 )

 # Add to database
 self.db.add(workflow_version)
 await self.db.commit()
 await self.db.refresh(workflow_version)

 return workflow_version

 async def get_latest_version_number(self, workflow_id: uuid.UUID) -> Optional[int]:
 """Get the latest version number for a workflow"""
 result = await self.db.execute(
 select(WorkflowVersion.version)
 .where(WorkflowVersion.workflow_id == workflow_id)
 .order_by(WorkflowVersion.version.desc())
 .limit(1)
 )
 latest = result.scalars().first()
 return latest

 async def get_workflow_version(self, workflow_id: uuid.UUID, version: Optional[int] = None) -> WorkflowVersion:
 """Get a specific version of a workflow"""
 # If version is not specified, get the latest
 if version is None:
 latest_version = await self.get_latest_version_number(workflow_id)
 if latest_version is None:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail=f"No versions found for workflow {workflow_id}"
 )
 version = latest_version

 # Query for the specific version
 result = await self.db.execute(
 select(WorkflowVersion)
 .where(
 WorkflowVersion.workflow_id == workflow_id,
 WorkflowVersion.version == version
 )
 )
 workflow_version = result.scalars().first()

 if not workflow_version:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail=f"Version {version} not found for workflow {workflow_id}"
 )

 return workflow_version

 async def execute_workflow(
 self,
 workflow_id: uuid.UUID,
 inputs: Dict[str, Any],
 user_id: uuid.UUID,
 version: Optional[int] = None,
 is_async: bool = False
 ) -> Any:
 """
 Execute a workflow with the given inputs

 If is_async is True, returns the execution ID
 Otherwise, executes synchronously and returns the result
 """
 # Get workflow and version
 workflow = await self.get_workflow(workflow_id)
 workflow_version = await self.get_workflow_version(workflow_id, version)

 # Create execution record
 execution = WorkflowExecution(
 workflow_id=workflow_id,
 version=workflow_version.version,
 inputs=inputs,
 status=ExecutionStatus.PENDING,
 initiated_by=user_id,
 )

 self.db.add(execution)
 await self.db.commit()
 await self.db.refresh(execution)

 if is_async:
 # Start background task for execution
 # In a real implementation, this would use a task queue
 # self.background_tasks.add_task(self._execute_workflow_async, execution.id)
 return execution.id
 else:
 # Execute synchronously
 result = await self._execute_workflow(execution.id)
 return result

 async def _execute_workflow(self, execution_id: uuid.UUID) -> Dict[str, Any]:
 """Internal method to execute a workflow"""
 # Get execution record
 result = await self.db.execute(
 select(WorkflowExecution).where(WorkflowExecution.id == execution_id)
 )
 execution = result.scalars().first()

 if not execution:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail=f"Execution with ID {execution_id} not found"
 )

 # Update status to running
 execution.status = ExecutionStatus.RUNNING
 await self.db.commit()

 try:
 # Get workflow definition
 workflow_version = await self.get_workflow_version(
 execution.workflow_id,
 execution.version
 )

 # Execute the workflow in n8n
 n8n_response = await self._execute_workflow_in_n8n(
 workflow_version.definition, execution.inputs
 )

 # Update execution record with results
 # Assuming n8n's execution API returns the final output in the response body
 execution.outputs = n8n_response # Adjust based on actual n8n response structure
 execution.status = ExecutionStatus.COMPLETED
 execution.completed_at = datetime.now(timezone.utc)
 await self.db.commit()

 return n8n_response

 except Exception as e:
 # Update execution record with error
 execution.error = str(e)
 execution.status = ExecutionStatus.FAILED
 execution.completed_at = datetime.now(timezone.utc)
 await self.db.commit()

 raise HTTPException(
 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
 detail=f"Workflow execution failed: {str(e)}"
 )

 async def get_execution(self, execution_id: uuid.UUID) -> WorkflowExecution:
 """Get the status and result of a workflow execution"""
 result = await self.db.execute(
 select(WorkflowExecution).where(WorkflowExecution.id == execution_id)
 )
 execution = result.scalars().first()

 if not execution:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail=f"Execution with ID {execution_id} not found"
 )

 return execution

 async def _execute_workflow_in_n8n(self, workflow_definition: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
 """Executes a workflow definition in n8n via its API."""
 n8n_user = os.getenv("N8N_BASIC_AUTH_USER")
 n8n_password = os.getenv("N8N_BASIC_AUTH_PASSWORD")
 n8n_url = "http://n8n:5678/api/v1/executions" # Use internal Docker service name

 if not n8n_user or not n8n_password:
 raise HTTPException(
 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
 detail="n8n basic auth credentials not configured."
 )

 async with httpx.AsyncClient() as client:
 try:
 response = await client.post(
 n8n_url,
 json={"workflow": workflow_definition, "parameters": inputs},
 auth=(n8n_user, n8n_password),
 timeout=600.0 # Set a reasonable timeout for workflow execution
 )
 response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
 return response.json()
 except httpx.HTTPStatusError as e:
 error_detail = f"n8n API returned error {e.response.status_code}: {e.response.text}"
 raise HTTPException(
 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
 detail=f"Failed to execute workflow in n8n: {error_detail}"
 ) from e
 except httpx.RequestError as e:
 raise HTTPException(
 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
 detail=f"Error communicating with n8n API: {str(e)}"
 ) from e

 # --- Rune Methods ---

 async def create_rune(self, rune_data: RuneDefinitionCreate, creator_id: uuid.UUID) -> RuneDefinition:
 """Create a new rune definition"""
 rune = RuneDefinition(
 name=rune_data.name,
 description=rune_data.description,
 category=rune_data.category,
 definition=rune_data.definition,
 is_public=rune_data.is_public,
 version=rune_data.version,
 creator_id=creator_id,
 is_verified=False # New runes are not verified by default
 )
 self.db.add(rune)
 await self.db.commit()
 await self.db.refresh(rune)
 return rune

 async def get_rune(self, rune_id: uuid.UUID) -> RuneDefinition:
 """Get a rune definition by ID"""
 result = await self.db.execute(
 select(RuneDefinition).where(RuneDefinition.id == rune_id)
 )
 rune = result.scalars().first()
 if not rune:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_NOT_FOUND,
 detail=f"Rune with ID {rune_id} not found"
 )
 return rune

 async def list_runes(
 self,
 category: Optional[str] = None,
 is_public: Optional[bool] = None,
 ) -> List[RuneDefinition]:
 """List rune definitions with optional filters"""
 query = select(RuneDefinition)

 filters = []
 if category is not None:
 filters.append(RuneDefinition.category == category)
 if is_public is not None:
 filters.append(RuneDefinition.is_public == is_public)

 if filters:
 query = query.where(and_(*filters))

 result = await self.db.execute(query)
 return result.scalars().all()
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.core.database import get_db
from app.models.workflow import Workflow, WorkflowVersion, WorkflowExecution, WorkflowStep
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowVersionCreate


class WorkflowService:
    """Service for managing workflows (Spells) in Composable Runes"""
    
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def create_workflow(self, workflow_data: WorkflowCreate, owner_id: uuid.UUID) -> Workflow:
        """Create a new workflow"""
        # Create the workflow
        workflow = Workflow(
            name=workflow_data.name,
            description=workflow_data.description,
            owner_id=owner_id,
            category=workflow_data.category,
            tags=workflow_data.tags,
            is_public=workflow_data.is_public,
            is_template=workflow_data.is_template,
        )
        
        self.db.add(workflow)
        await self.db.commit()
        await self.db.refresh(workflow)
        
        # Create the initial version if definition is provided
        if workflow_data.definition:
            version = WorkflowVersion(
                workflow_id=workflow.id,
                version=1,
                definition=workflow_data.definition,
                created_by=owner_id,
            )
            
            self.db.add(version)
            await self.db.commit()
            await self.db.refresh(version)
        
        return workflow
    
    async def get_workflow(self, workflow_id: uuid.UUID) -> Workflow:
        """Get a workflow by ID"""
        result = await self.db.execute(select(Workflow).filter(Workflow.id == workflow_id))
        workflow = result.scalars().first()
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workflow not found"
            )
            
        return workflow
    
    async def update_workflow(self, workflow_id: uuid.UUID, workflow_data: WorkflowUpdate) -> Workflow:
        """Update a workflow's metadata"""
        workflow = await self.get_workflow(workflow_id)
        
        # Update the workflow attributes
        update_data = workflow_data.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            # Skip the definition as it's handled separately with versioning
            if key != "definition":
                setattr(workflow, key, value)
        
        await self.db.commit()
        await self.db.refresh(workflow)
        
        return workflow
    
    async def create_workflow_version(
        self, 
        workflow_id: uuid.UUID, 
        version_data: WorkflowVersionCreate,
        created_by: uuid.UUID
    ) -> WorkflowVersion:
        """Create a new version of a workflow"""
        # Make sure the workflow exists
        workflow = await self.get_workflow(workflow_id)
        
        # Get the latest version number
        result = await self.db.execute(
            select(WorkflowVersion)
            .filter(WorkflowVersion.workflow_id == workflow_id)
            .order_by(WorkflowVersion.version.desc())
        )
        latest_version = result.scalars().first()
        
        new_version_number = 1
        if latest_version:
            new_version_number = latest_version.version + 1
        
        # Create new version
        version = WorkflowVersion(
            workflow_id=workflow_id,
            version=new_version_number,
            definition=version_data.definition,
            created_by=created_by,
            comment=version_data.comment
        )
        
        self.db.add(version)
        await self.db.commit()
        await self.db.refresh(version)
        
        return version
    
    async def get_workflow_version(
        self, 
        workflow_id: uuid.UUID, 
        version: Optional[int] = None
    ) -> WorkflowVersion:
        """Get a specific version of a workflow, or the latest if version is None"""
        if version:
            result = await self.db.execute(
                select(WorkflowVersion)
                .filter(
                    WorkflowVersion.workflow_id == workflow_id,
                    WorkflowVersion.version == version
                )
            )
            workflow_version = result.scalars().first()
            
            if not workflow_version:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Workflow version {version} not found"
                )
        else:
            # Get the latest version
            result = await self.db.execute(
                select(WorkflowVersion)
                .filter(WorkflowVersion.workflow_id == workflow_id)
                .order_by(WorkflowVersion.version.desc())
            )
            workflow_version = result.scalars().first()
            
            if not workflow_version:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No versions found for this workflow"
                )
        
        return workflow_version
    
    async def execute_workflow(
        self,
        workflow_id: uuid.UUID,
        inputs: Dict[str, Any],
        user_id: uuid.UUID,
        version: Optional[int] = None,
        is_async: bool = False
    ) -> Union[Dict[str, Any], uuid.UUID]:
        """
        Execute a workflow with the given inputs
        Returns the result directly if is_async=False, or an execution ID if is_async=True
        """
        # Get the workflow version to execute
        workflow_version = await self.get_workflow_version(workflow_id, version)
        
        # Create an execution record
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            version=workflow_version.version,
            inputs=inputs,
            initiated_by=user_id,
            status="pending" if is_async else "running"
        )
        
        self.db.add(execution)
        await self.db.commit()
        await self.db.refresh(execution)
        
        if is_async:
            # For async execution, trigger the background task and return the ID
            # ... (implementation omitted) ...
            return execution.id
        else:
            # For sync execution, run the workflow and update the record
            try:
                # Execute the workflow definition
                result = await self._run_workflow(workflow_version.definition, inputs)
                
                # Update the execution record
                execution.status = "completed"
                execution.outputs = result
                execution.completed_at = datetime.utcnow()
                
                await self.db.commit()
                return result
                
            except Exception as e:
                # Handle execution error
                execution.status = "failed"
                execution.error = str(e)
                execution.completed_at = datetime.utcnow()
                
                await self.db.commit()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Workflow execution failed: {str(e)}"
                )
    
    async def get_execution(self, execution_id: uuid.UUID) -> WorkflowExecution:
        """Get details of a workflow execution"""
        result = await self.db.execute(
            select(WorkflowExecution).filter(WorkflowExecution.id == execution_id)
        )
        execution = result.scalars().first()
        
        if not execution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Execution not found"
            )
            
        return execution
    
    async def _execute_workflow_in_n8n(self, workflow_definition: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a workflow definition in n8n via its API."""
        n8n_user = os.getenv("N8N_BASIC_AUTH_USER")
        n8n_password = os.getenv("N8N_BASIC_AUTH_PASSWORD")
        n8n_url = "http://n8n:5678/api/v1/executions" # Use internal Docker service name

        if not n8n_user or not n8n_password:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="n8n basic auth credentials not configured."
            )

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    n8n_url,
                    json={"workflow": workflow_definition, "parameters": inputs},
                    auth=(n8n_user, n8n_password),
                    timeout=600.0 # Set a reasonable timeout for workflow execution
                )
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                return response.json()
            except httpx.HTTPStatusError as e:
                error_detail = f"n8n API returned error {e.response.status_code}: {e.response.text}"
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to execute workflow in n8n: {error_detail}"
                ) from e
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error communicating with n8n API: {str(e)}"
                ) from e

    async def _run_workflow(self, definition: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
 """Internal method to execute a workflow"""
 # This method is now a wrapper that calls the n8n execution function
 return await self._execute_workflow_in_n8n(definition, inputs)