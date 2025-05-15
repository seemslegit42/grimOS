from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

# Data Integration models
class ConnectorConfig(BaseModel):
    url: Optional[str] = None
    method: Optional[str] = None  # GET only for MVP
    headers: Optional[Dict[str, str]] = None
    # Other connector-specific configuration

class ConnectorExecuteRequest(BaseModel):
    connector_type: str  # REST_API_CALL, SLACK_NOTIFICATION
    config: ConnectorConfig
    payload: Optional[Dict[str, Any]] = None

class ConnectorExecuteResponse(BaseModel):
    status: str  # success, failed
    response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
