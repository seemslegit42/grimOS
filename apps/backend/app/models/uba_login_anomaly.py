from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.models.base import BaseModel


class UBALoginAnomalyAlert(BaseModel):
    __tablename__ = "uba_login_anomaly_alerts"

    # Core alert data
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    username = Column(String, nullable=False, index=True)
    alert_type = Column(String, nullable=False, index=True)  # impossible_travel, multiple_failed_logins, new_location
    description = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    
    # Location data (optional)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Alert metadata
    timestamp = Column(DateTime, nullable=False, index=True)
    status = Column(String, nullable=False, index=True, default="new")  # new, reviewed, false_positive, investigating
    severity = Column(String, nullable=False, index=True)  # low, medium, high
    
    # Additional details
    details = Column(JSONB, nullable=True)
