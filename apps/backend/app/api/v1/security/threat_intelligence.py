from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session
import uuid

from app.db.session import get_db
from app.schemas.security import ThreatIndicator
from app.schemas.common import PaginatedResponse, PaginationMeta
from app.repositories.threat_indicator import threat_indicator_repository
from app.services.threat_intelligence_ingestion import fetch_threat_intelligence_feed, ingest_threat_intelligence

router = APIRouter(
    prefix="/threat-intelligence",
    tags=["security", "threat-intelligence"],
)

@router.get("/indicators", response_model=PaginatedResponse)
async def get_threat_indicators(
    db: Session = Depends(get_db),
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    source: Optional[str] = None,
    type: Optional[str] = None,
    severity: Optional[str] = None,
    sort_by: str = "last_seen",
    sort_order: str = "desc",
):
    """
    Retrieve a list of threat indicators with optional filtering
    """
    # Filters
    filters = {}
    if source:
        filters["source"] = source
    if type:
        filters["indicator_type"] = type
    if severity:
        filters["severity"] = severity
    
    # Get total count
    total = threat_indicator_repository.count(db, **filters)
    
    # Get data
    indicators = threat_indicator_repository.get_multi(
        db, skip=offset, limit=limit, **filters
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
        data=indicators,
        pagination=pagination,
    )

@router.post("/ingest", status_code=201)
async def ingest_feed(
    feed_url: str,
    db: Session = Depends(get_db),
):
    """
    Ingest threat intelligence data from a feed URL.
    """
    try:
        feed_data = fetch_threat_intelligence_feed(feed_url)
        ingest_threat_intelligence(db, feed_data)
        return {"message": "Feed ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
