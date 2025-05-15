from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, constr

# Threat Intelligence models
class ThreatIndicatorBase(BaseModel):
    indicator_value: str
    indicator_type: str  # ip, domain, hash_md5, hash_sha256, url
    source: str
    severity: Optional[str] = None  # low, medium, high, critical
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    first_seen: Optional[datetime] = None
    last_seen: datetime

class ThreatIndicatorCreate(ThreatIndicatorBase):
    pass

class ThreatIndicatorUpdate(BaseModel):
    indicator_value: Optional[str] = None
    indicator_type: Optional[str] = None
    source: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None

class ThreatIndicator(ThreatIndicatorBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
