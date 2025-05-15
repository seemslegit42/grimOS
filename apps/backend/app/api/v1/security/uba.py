from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

from app.db.session import get_db
from app.schemas.uba import UBALoginAnomalyAlert, UBALoginAnomalyAlertUpdate
from app.schemas.common import PaginatedResponse, PaginationMeta
from app.repositories.uba_login_anomaly import uba_login_anomaly_repository

router = APIRouter(
    prefix="/uba/login-anomalies",
    tags=["security", "uba"],
)

@router.get("", response_model=PaginatedResponse)
async def get_login_anomalies(
    db: Session = Depends(get_db),
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_id: Optional[UUID] = None,
    alert_type: Optional[str] = None,
    status: Optional[str] = "new",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_by: str = "timestamp",
    sort_order: str = "desc",
):
    """
    Retrieve a list of login anomaly alerts with optional filtering
    """
    # Filters
    filters = {}
    if user_id:
        filters["user_id"] = user_id
    if alert_type:
        filters["alert_type"] = alert_type
    if status:
        filters["status"] = status
    
    # Date filtering would require more sophisticated SQL queries
    # For MVP, we'll handle it in memory after fetching
    
    # Get total count
    total = uba_login_anomaly_repository.count(db, **filters)
    
    # Get data
    anomalies = uba_login_anomaly_repository.get_multi(
        db, skip=offset, limit=limit, **filters
    )
    
    # Filter by date if needed
    if start_date or end_date:
        filtered_anomalies = []
        for anomaly in anomalies:
            if start_date and anomaly.timestamp < start_date:
                continue
            if end_date and anomaly.timestamp > end_date:
                continue
            filtered_anomalies.append(anomaly)
        anomalies = filtered_anomalies
        # Note: this affects pagination accuracy, but is acceptable for MVP
    
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
        data=anomalies,
        pagination=pagination,
    )

@router.patch("/{alert_id}", response_model=UBALoginAnomalyAlert)
async def update_login_anomaly(
    alert_id: UUID = Path(..., description="The ID of the login anomaly alert"),
    alert_update: UBALoginAnomalyAlertUpdate = None,
    db: Session = Depends(get_db),
):
    """
    Update the status of a login anomaly alert
    """
    # Get the alert
    db_alert = uba_login_anomaly_repository.get(db, alert_id)
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Login anomaly alert with ID {alert_id} not found",
        )
    
    # Update the alert
    updated_alert = uba_login_anomaly_repository.update(db, db_obj=db_alert, obj_in=alert_update)
    
    return updated_alert
