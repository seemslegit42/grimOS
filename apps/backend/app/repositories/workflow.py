from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID

from app.repositories.base import BaseRepository
from app.models.workflow import WorkflowDefinition, Rune, WorkflowInstance
from app.schemas.workflow import WorkflowDefinitionCreate, WorkflowDefinitionUpdate


class WorkflowDefinitionRepository(BaseRepository[WorkflowDefinition, WorkflowDefinitionCreate, WorkflowDefinitionUpdate]):
    def get_with_runes(self, db: Session, id: UUID) -> Optional[WorkflowDefinition]:
        """Get a workflow definition with all its runes"""
        return db.query(WorkflowDefinition).filter(WorkflowDefinition.id == id).first()


class WorkflowInstanceRepository:
    def create(self, db: Session, *, definition_id: UUID, name: Optional[str] = None, initial_payload: Optional[Dict[str, Any]] = None) -> WorkflowInstance:
        """Create a new workflow instance"""
        # Get the workflow definition to get its name
        definition = db.query(WorkflowDefinition).get(definition_id)
        if not definition:
            raise ValueError(f"Workflow definition with id {definition_id} not found")
        
        # Create the workflow instance
        db_obj = WorkflowInstance(
            definition_id=definition_id,
            definition=definition,
            name=name,
            status="pending",
            payload=initial_payload or {},
            execution_log=[],
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: UUID) -> Optional[WorkflowInstance]:
        """Get a workflow instance by id"""
        return db.query(WorkflowInstance).filter(WorkflowInstance.id == id).first()
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, definition_id: Optional[UUID] = None, status: Optional[str] = None
    ) -> List[WorkflowInstance]:
        """Get multiple workflow instances with filters"""
        query = db.query(WorkflowInstance)
        if definition_id:
            query = query.filter(WorkflowInstance.definition_id == definition_id)
        if status:
            query = query.filter(WorkflowInstance.status == status)
        return query.offset(skip).limit(limit).all()
    
    def count(self, db: Session, *, definition_id: Optional[UUID] = None, status: Optional[str] = None) -> int:
        """Count workflow instances with filters"""
        query = db.query(WorkflowInstance)
        if definition_id:
            query = query.filter(WorkflowInstance.definition_id == definition_id)
        if status:
            query = query.filter(WorkflowInstance.status == status)
        return query.count()
    
    def update_task(self, db: Session, *, instance_id: UUID, task_id: str, outcome: str, notes: Optional[str] = None) -> WorkflowInstance:
        """Update a manual task in a workflow instance"""
        instance = self.get(db, instance_id)
        if not instance:
            raise ValueError(f"Workflow instance with id {instance_id} not found")
        
        # In a real implementation, we would check if the task exists and if it's a manual task
        # Then update the task and potentially advance the workflow
        # For MVP, this is simplified
        
        # Add a log entry
        if not instance.execution_log:
            instance.execution_log = []
        
        import datetime
        instance.execution_log.append({
            "step_id": task_id,
            "status": "completed",
            "message": f"Task completed with outcome: {outcome}" + (f" - Notes: {notes}" if notes else ""),
            "timestamp": datetime.datetime.utcnow().isoformat(),
        })
        
        # For MVP, we'll just mark the workflow as completed
        # In a real implementation, we would advance to the next step
        instance.status = "completed"
        instance.end_time = datetime.datetime.utcnow()
        
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance


workflow_definition_repository = WorkflowDefinitionRepository(WorkflowDefinition)
workflow_instance_repository = WorkflowInstanceRepository()
