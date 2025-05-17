import requests
from typing import List, Dict, TypedDict, Any
from sqlalchemy.orm import Session
from app.models.threat_indicator import ThreatIndicator
from app.repositories.threat_indicator import threat_indicator_repository

class ThreatIndicatorData(TypedDict):
    value: str
    type: str
    source: str
    severity: str
    description: str
    tags: List[str]
    first_seen: str
    last_seen: str
    metadata: Dict[str, Any]

def fetch_threat_intelligence_feed(feed_url: str) -> List[ThreatIndicatorData]:
    """
    Fetch threat intelligence data from a given feed URL.
    """
    response = requests.get(feed_url)
    response.raise_for_status()
    return response.json()

def ingest_threat_intelligence(db: Session, feed_data: List[ThreatIndicatorData]):
    """
    Ingest threat intelligence data into the database.
    """
    for item in feed_data:
        # Map feed data to ThreatIndicator fields
        indicator = ThreatIndicator(
            indicator_value=item["value"],
            indicator_type=item["type"],
            source=item["source"],
            severity=item.get("severity"),
            description=item.get("description"),
            tags=item.get("tags"),
            first_seen=item.get("first_seen"),
            last_seen=item["last_seen"],
            metadata=item.get("metadata"),
        )
        # Deduplication logic (e.g., check if indicator already exists)
        existing = threat_indicator_repository.get_by_field(
            db, field="indicator_value", value=indicator.indicator_value
        )
        if not existing:
            threat_indicator_repository.create(db, obj_in=indicator)
