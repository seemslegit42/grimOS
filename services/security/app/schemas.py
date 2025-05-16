from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

# Threat Intelligence Schemas
class ThreatIndicatorBase(BaseModel):
    type: str = Field(..., description="Type of indicator (IP, domain, hash, etc.)")
    value: str = Field(..., description="The actual indicator value")
    source: str = Field(..., description="Source of the indicator")
    confidence: Optional[float] = Field(None, description="Confidence score if available")
    description: Optional[str] = Field(None, description="Description of the threat")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class ThreatIndicatorCreate(ThreatIndicatorBase):
    pass

class ThreatIndicator(ThreatIndicatorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ThreatFeedConfig(BaseModel):
    name: str = Field(..., description="Name of the feed")
    url: str = Field(..., description="URL of the feed")
    api_key: Optional[str] = Field(None, description="API key if required")
    feed_type: str = Field(..., description="Type of feed (STIX, CSV, etc.)")
    collection_id: Optional[str] = Field(None, description="Collection ID for TAXII feeds")
    enabled: bool = Field(True, description="Whether the feed is enabled")

# User Behavior Analytics Schemas
class UserLoginEventBase(BaseModel):
    user_id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    success: bool = Field(True, description="Whether login was successful")
    ip_address: str = Field(..., description="IP address of the login attempt")
    user_agent: str = Field(..., description="User agent string")
    country: Optional[str] = Field(None, description="Country of origin if available")
    city: Optional[str] = Field(None, description="City of origin if available")

class UserLoginEventCreate(UserLoginEventBase):
    pass

class UserLoginEvent(UserLoginEventBase):
    id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True

class UserLoginBaselineBase(BaseModel):
    user_id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    common_ip_addresses: List[str] = Field(default_factory=list, description="Commonly used IP addresses")
    common_countries: List[str] = Field(default_factory=list, description="Commonly accessed countries")
    common_cities: List[str] = Field(default_factory=list, description="Commonly accessed cities")
    common_times: Dict[str, int] = Field(default_factory=dict, description="Common login times (hour of day)")
    common_days: Dict[str, int] = Field(default_factory=dict, description="Common login days (day of week)")

class UserLoginBaseline(UserLoginBaselineBase):
    id: int
    last_updated: datetime
    
    class Config:
        orm_mode = True

class LoginAnomalyBase(BaseModel):
    user_id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    login_event_id: int = Field(..., description="ID of the related login event")
    anomaly_type: str = Field(..., description="Type of anomaly detected")
    severity: str = Field(..., description="Severity level (low, medium, high)")
    description: str = Field(..., description="Description of the anomaly")

class LoginAnomalyCreate(LoginAnomalyBase):
    pass

class LoginAnomaly(LoginAnomalyBase):
    id: int
    timestamp: datetime
    resolved: bool
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class LoginAnomalyResolve(BaseModel):
    resolved_by: str = Field(..., description="User who resolved the anomaly")
    notes: Optional[str] = Field(None, description="Notes about the resolution")