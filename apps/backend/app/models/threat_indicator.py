from sqlalchemy import Column, String, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import BaseModel


class ThreatIndicator(BaseModel):
    __tablename__ = "threat_indicators"

    # Core indicator data
    indicator_value = Column(String, nullable=False, index=True)
    indicator_type = Column(String, nullable=False, index=True)  # ip, domain, hash_md5, hash_sha256, url
    source = Column(String, nullable=False, index=True)
    severity = Column(String, index=True)  # low, medium, high, critical
    description = Column(String)
    
    # Additional metadata
    tags = Column(ARRAY(String), nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=False)
    
    # For deduplication and future use
    metadata = Column(JSONB, nullable=True)
