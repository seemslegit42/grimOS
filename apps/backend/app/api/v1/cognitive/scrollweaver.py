from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.cognitive import ScrollWeaverRequest, ScrollWeaverResponse
from app.repositories.cognitive import scrollweaver_repository
from app.models.cognitive import ScrollWeaverRequest as ScrollWeaverRequestModel

router = APIRouter(
    prefix="/scrollweaver",
    tags=["cognitive", "scrollweaver"],
)

@router.post("/generate", response_model=ScrollWeaverResponse)
async def generate_workflow_from_nl(
    request: ScrollWeaverRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a workflow from natural language input.
    
    This endpoint analyzes natural language text and converts it into
    structured workflow steps that can be used to create a workflow.
    
    Example:
        "Assign document review to John then send notification to manager"
    
    Returns interpreted steps with confidence score and potential warnings.
    """
    # In a real application, we would get the user ID from the authentication token
    # For MVP, we'll use a placeholder user ID
    user_id = "00000000-0000-0000-0000-000000000000"
    
    # Process the request
    response = await scrollweaver_repository.process_request(db, user_id=user_id, request=request)
    
    return response

@router.get("/history", response_model=Dict[str, List[Dict[str, Any]]])
async def get_scrollweaver_history(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None, description="Filter by processing status (pending, processing, completed, failed)")
):
    """
    Retrieve the history of ScrollWeaver natural language processing requests.
    
    Returns the most recent requests with their processing status and results.
    """
    # In a real application, we would get the user ID from the authentication token
    # and filter by that user's requests
    # For MVP, we'll use a placeholder user ID
    user_id = "00000000-0000-0000-0000-000000000000"
    
    # Query the database for ScrollWeaver requests
    query = db.query(ScrollWeaverRequestModel)
    
    # Filter by status if provided
    if status:
        query = query.filter(ScrollWeaverRequestModel.processing_status == status)
    
    # Sort by creation date (newest first)
    query = query.order_by(ScrollWeaverRequestModel.created_at.desc())
    
    # Apply pagination
    query = query.offset(offset).limit(limit)
    
    # Get the results
    requests = query.all()
    
    # Format the results
    result = []
    for req in requests:
        result.append({
            "id": str(req.id),
            "input": req.natural_language_input,
            "status": req.processing_status,
            "created_at": req.created_at,
            "confidence_score": req.confidence_score,
            "error": req.error,
            "response": req.response
        })
    
    return {"data": result}
