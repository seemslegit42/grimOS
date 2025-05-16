from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import os
import json
from datetime import datetime, timedelta

from database import get_db
import models
import schemas
from services import threat_intelligence_service

router = APIRouter()

@router.get("/", response_model=List[schemas.ThreatIndicator])
def get_threat_indicators(
    skip: int = 0, 
    limit: int = 100, 
    indicator_type: Optional[str] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get a list of threat indicators with optional filtering
    """
    return threat_intelligence_service.get_threat_indicators(
        db, skip=skip, limit=limit, indicator_type=indicator_type, source=source
    )

@router.post("/", response_model=schemas.ThreatIndicator, status_code=status.HTTP_201_CREATED)
def create_threat_indicator(
    indicator: schemas.ThreatIndicatorCreate,
    db: Session = Depends(get_db)
):
    """
    Manually add a new threat indicator
    """
    # Check if indicator already exists
    existing_indicator = db.query(models.ThreatIndicator).filter(
        models.ThreatIndicator.type == indicator.type,
        models.ThreatIndicator.value == indicator.value,
        models.ThreatIndicator.source == indicator.source
    ).first()
    
    if existing_indicator:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Indicator already exists with id: {existing_indicator.id}"
        )
    
    return threat_intelligence_service.create_threat_indicator(db, indicator)

@router.get("/feeds", response_model=List[schemas.ThreatFeedConfig])
def get_feed_configurations(db: Session = Depends(get_db)):
    """
    Get a list of configured threat intelligence feeds
    """
    return threat_intelligence_service.get_feed_configurations(db)

@router.post("/feeds", response_model=schemas.ThreatFeedConfig, status_code=status.HTTP_201_CREATED)
def create_feed_configuration(
    feed_config: schemas.ThreatFeedConfig,
    db: Session = Depends(get_db)
):
    """
    Add a new threat intelligence feed configuration
    """
    return threat_intelligence_service.create_feed_configuration(db, feed_config)

@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
def trigger_feed_ingestion(
    background_tasks: BackgroundTasks,
    feed_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Trigger ingestion of threat intelligence feeds
    """
    background_tasks.add_task(
        threat_intelligence_service.ingest_feeds, 
        db=db, 
        feed_name=feed_name
    )
    return {"message": "Feed ingestion started in the background"}

@router.get("/stats")
def get_threat_intelligence_stats(
    days: int = Query(7, description="Number of days to include in stats"),
    db: Session = Depends(get_db)
):
    """
    Get statistics about threat indicators
    """
    since_date = datetime.now() - timedelta(days=days)
    
    # Get counts by type
    type_counts = db.query(
        models.ThreatIndicator.type, 
        db.func.count(models.ThreatIndicator.id)
    ).group_by(
        models.ThreatIndicator.type
    ).all()
    
    # Get counts by source
    source_counts = db.query(
        models.ThreatIndicator.source, 
        db.func.count(models.ThreatIndicator.id)
    ).group_by(
        models.ThreatIndicator.source
    ).all()
    
    # Get recent indicators count
    recent_count = db.query(models.ThreatIndicator).filter(
        models.ThreatIndicator.created_at >= since_date
    ).count()
    
    # Get total count
    total_count = db.query(models.ThreatIndicator).count()
    
    return {
        "total_indicators": total_count,
        "recent_indicators": recent_count,
        "by_type": dict(type_counts),
        "by_source": dict(source_counts)
    }

@router.delete("/{indicator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_threat_indicator(
    indicator_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a threat indicator
    """
    indicator = db.query(models.ThreatIndicator).filter(models.ThreatIndicator.id == indicator_id).first()
    if not indicator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Indicator with id {indicator_id} not found"
        )
    
    db.delete(indicator)
    db.commit()
    return None