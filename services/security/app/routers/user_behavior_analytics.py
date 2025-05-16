from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
import models
import schemas
from services import user_behavior_analytics_service

router = APIRouter()

@router.post("/login-events", response_model=schemas.UserLoginEvent, status_code=status.HTTP_201_CREATED)
def record_login_event(
    login_event: schemas.UserLoginEventCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Record a new user login event and analyze for anomalies
    """
    # Create the login event
    db_login_event = user_behavior_analytics_service.create_login_event(db, login_event)
    
    # Analyze for anomalies in the background
    background_tasks.add_task(
        user_behavior_analytics_service.analyze_login_event,
        db=db,
        login_event_id=db_login_event.id
    )
    
    return db_login_event

@router.get("/login-events", response_model=List[schemas.UserLoginEvent])
def get_login_events(
    user_id: Optional[str] = None,
    username: Optional[str] = None,
    success: Optional[bool] = None,
    days: int = Query(7, description="Number of days to include"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get user login events with optional filtering
    """
    since_date = datetime.now() - timedelta(days=days)
    
    return user_behavior_analytics_service.get_login_events(
        db, 
        user_id=user_id, 
        username=username, 
        success=success, 
        since_date=since_date,
        skip=skip, 
        limit=limit
    )

@router.get("/anomalies", response_model=List[schemas.LoginAnomaly])
def get_login_anomalies(
    user_id: Optional[str] = None,
    username: Optional[str] = None,
    resolved: Optional[bool] = None,
    severity: Optional[str] = None,
    days: int = Query(7, description="Number of days to include"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get detected login anomalies with optional filtering
    """
    since_date = datetime.now() - timedelta(days=days)
    
    return user_behavior_analytics_service.get_login_anomalies(
        db, 
        user_id=user_id, 
        username=username, 
        resolved=resolved,
        severity=severity,
        since_date=since_date,
        skip=skip, 
        limit=limit
    )

@router.post("/anomalies/{anomaly_id}/resolve", response_model=schemas.LoginAnomaly)
def resolve_anomaly(
    anomaly_id: int,
    resolution: schemas.LoginAnomalyResolve,
    db: Session = Depends(get_db)
):
    """
    Mark a login anomaly as resolved
    """
    anomaly = db.query(models.LoginAnomaly).filter(models.LoginAnomaly.id == anomaly_id).first()
    if not anomaly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Anomaly with id {anomaly_id} not found"
        )
    
    if anomaly.resolved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Anomaly with id {anomaly_id} is already resolved"
        )
    
    return user_behavior_analytics_service.resolve_anomaly(db, anomaly, resolution)

@router.post("/update-baselines", status_code=status.HTTP_202_ACCEPTED)
def update_user_baselines(
    background_tasks: BackgroundTasks,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Trigger an update of user login behavior baselines
    """
    background_tasks.add_task(
        user_behavior_analytics_service.update_user_baselines,
        db=db,
        user_id=user_id
    )
    
    return {"message": "Baseline update started in the background"}

@router.get("/baselines/{user_id}", response_model=schemas.UserLoginBaseline)
def get_user_baseline(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the login behavior baseline for a specific user
    """
    baseline = db.query(models.UserLoginBaseline).filter(models.UserLoginBaseline.user_id == user_id).first()
    if not baseline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Baseline for user {user_id} not found"
        )
    
    return baseline

@router.get("/stats")
def get_uba_stats(
    days: int = Query(7, description="Number of days to include in stats"),
    db: Session = Depends(get_db)
):
    """
    Get statistics about user behavior analytics
    """
    since_date = datetime.now() - timedelta(days=days)
    
    # Get total login events
    total_logins = db.query(models.UserLoginEvent).filter(
        models.UserLoginEvent.timestamp >= since_date
    ).count()
    
    # Get successful vs failed logins
    successful_logins = db.query(models.UserLoginEvent).filter(
        models.UserLoginEvent.timestamp >= since_date,
        models.UserLoginEvent.success == True
    ).count()
    
    failed_logins = db.query(models.UserLoginEvent).filter(
        models.UserLoginEvent.timestamp >= since_date,
        models.UserLoginEvent.success == False
    ).count()
    
    # Get anomalies by type
    anomaly_types = db.query(
        models.LoginAnomaly.anomaly_type,
        db.func.count(models.LoginAnomaly.id)
    ).filter(
        models.LoginAnomaly.timestamp >= since_date
    ).group_by(
        models.LoginAnomaly.anomaly_type
    ).all()
    
    # Get anomalies by severity
    anomaly_severity = db.query(
        models.LoginAnomaly.severity,
        db.func.count(models.LoginAnomaly.id)
    ).filter(
        models.LoginAnomaly.timestamp >= since_date
    ).group_by(
        models.LoginAnomaly.severity
    ).all()
    
    # Get total anomalies
    total_anomalies = db.query(models.LoginAnomaly).filter(
        models.LoginAnomaly.timestamp >= since_date
    ).count()
    
    # Get resolved vs unresolved anomalies
    resolved_anomalies = db.query(models.LoginAnomaly).filter(
        models.LoginAnomaly.timestamp >= since_date,
        models.LoginAnomaly.resolved == True
    ).count()
    
    return {
        "login_events": {
            "total": total_logins,
            "successful": successful_logins,
            "failed": failed_logins
        },
        "anomalies": {
            "total": total_anomalies,
            "resolved": resolved_anomalies,
            "unresolved": total_anomalies - resolved_anomalies,
            "by_type": dict(anomaly_types),
            "by_severity": dict(anomaly_severity)
        }
    }