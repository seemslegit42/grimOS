from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

# UBA Login Anomaly models
class LocationData(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UBALoginAnomalyAlertBase(BaseModel):
    user_id: UUID
    username: str
    alert_type: str  # impossible_travel, multiple_failed_logins, new_location
    description: str
    ip_address: str
    location: Optional[LocationData] = None
    timestamp: datetime
    severity: str  # low, medium, high
    details: Optional[Dict[str, Any]] = None

class UBALoginAnomalyAlertCreate(UBALoginAnomalyAlertBase):
    status: str = "new"  # new, reviewed, false_positive, investigating

class UBALoginAnomalyAlertUpdate(BaseModel):
    status: str  # reviewed, false_positive, investigating

class UBALoginAnomalyAlert(UBALoginAnomalyAlertBase):
    id: UUID
    status: str  # new, reviewed, false_positive, investigating
    created_at: datetime

    class Config:
        from_attributes = True
