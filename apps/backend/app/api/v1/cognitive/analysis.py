from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.cognitive import AnalysisTrend
from app.repositories.cognitive import analysis_trend_repository

router = APIRouter(
    prefix="/analysis",
    tags=["cognitive", "analysis"],
)

@router.get("/operational-trends", response_model=Dict[str, List[AnalysisTrend]])
async def get_operational_trends(
    db: Session = Depends(get_db),
    trend_type: Optional[str] = Query(None, description="Filter by trend type (e.g., workflow_duration_anomaly, login_failures)"),
    time_period: Optional[str] = Query(None, description="Filter by time period (today, week, month)"),
    severity: Optional[str] = Query(None, description="Filter by severity (info, warning, critical)"),
):
    """
    Retrieve AI-analyzed operational trends like workflow completion time anomalies, 
    login attempt spikes, and other operational patterns.
    
    Returns trends sorted by severity (critical first) and recency.
    """
    # Get trends from repository
    trends = analysis_trend_repository.get_operational_trends(
        db, 
        trend_type=trend_type,
        time_period=time_period,
        severity=severity,
    )
    
    return {"data": trends}

@router.post("/generate-mock-data", response_model=Dict[str, List[AnalysisTrend]])
async def generate_mock_trends(db: Session = Depends(get_db)):
    """
    Generate mock analysis trend data for development purposes.
    This endpoint is only available in development mode.
    """
    # Check if we're in development mode
    from app.core.config import settings
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available in development mode"
        )
    
    # Generate mock data
    trends = await analysis_trend_repository.generate_mock_trends(db)
    
    return {"data": trends}
