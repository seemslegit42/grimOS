from sqlalchemy import Column, String, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.models.base import BaseModel


class ScrollWeaverRequest(BaseModel):
    __tablename__ = "scrollweaver_requests"

    # Input natural language content
    natural_language_input = Column(Text, nullable=False)
    
    # User who created the request
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Output/response
    response = Column(JSONB, nullable=True)
    
    # Processing metadata
    processing_status = Column(String, nullable=False, default="pending")  # pending, processing, completed, failed
    error = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)


class AnalysisTrend(BaseModel):
    __tablename__ = "analysis_trends"

    # Type of trend 
    trend_type = Column(String, nullable=False, index=True)  # workflow_duration, login_failures, etc.
    
    # Related resources
    resource_id = Column(UUID(as_uuid=True), nullable=True, index=True)  # workflow_id, etc.
    resource_type = Column(String, nullable=True)
    
    # Trend data
    message = Column(Text, nullable=False)
    severity = Column(String, nullable=False, index=True)  # info, warning, critical
    
    # Additional data
    details = Column(JSONB, nullable=True)
