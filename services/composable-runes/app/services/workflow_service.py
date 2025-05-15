"""
Workflow service for the Composable Runes module
"""
from typing import Dict, List, Any, Optional, Union
import uuid
from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
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
    
    async def _run_workflow(self, definition: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a workflow based on its definition and inputs
        This is a placeholder for the actual workflow execution logic
        """
        # This would be a complex implementation that:
        # 1. Parses the workflow definition (nodes and connections)
        # 2. Validates inputs against the workflow's input schema
        # 3. Executes each node in the correct order based on dependencies
        # 4. Passes data between nodes
        # 5. Handles conditions, loops, and other control flow
        # 6. Returns the final outputs
        
        # For now, return a simple mock implementation
        return {
            "success": True,
            "message": "Workflow executed successfully (mock)",
            "input_received": inputs
        }
