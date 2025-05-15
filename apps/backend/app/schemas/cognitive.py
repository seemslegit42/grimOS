from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

# ScrollWeaver models
class ScrollWeaverRequest(BaseModel):
    natural_language_input: str

class ScrollWeaverStepParameter(BaseModel):
    name: str
    value: Any

class ScrollWeaverStep(BaseModel):
    step_number: int
    action: str  # e.g., "Assign Manual Task", "Send Notification"
    description: str  # e.g., "'Review Q1 Report' to John Doe"
    parameters: Dict[str, Any] = {}

class ScrollWeaverResponse(BaseModel):
    original_input: str
    interpreted_steps: List[ScrollWeaverStep]
    confidence_score: Optional[float] = None
    warnings: Optional[List[str]] = None

# AI Analysis models
class AnalysisTrend(BaseModel):
    trend_type: str  # workflow_duration_anomaly, login_failures, etc.
    workflow_definition_id: Optional[UUID] = None
    message: str
    severity: str  # info, warning, critical
    timestamp: datetime
