from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import datetime

class ThreatIndicator(Base):
    """Model for storing threat intelligence indicators"""
    __tablename__ = "threat_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)  # IP, domain, hash, etc.
    value = Column(String, index=True)  # The actual indicator value
    source = Column(String, index=True)  # Source of the indicator
    confidence = Column(Float, nullable=True)  # Confidence score if available
    description = Column(Text, nullable=True)  # Description of the threat
    metadata = Column(JSON, nullable=True)  # Additional metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships can be added here if needed

class UserLoginEvent(Base):
    """Model for storing user login events for behavior analytics"""
    __tablename__ = "user_login_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    username = Column(String, index=True)
    success = Column(Boolean, default=True)  # Whether login was successful
    ip_address = Column(String, index=True)
    user_agent = Column(String)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    timestamp = Column(DateTime, default=func.now())
    
    # Relationships can be added here if needed

class UserLoginBaseline(Base):
    """Model for storing user login behavior baselines"""
    __tablename__ = "user_login_baselines"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    common_ip_addresses = Column(JSON)  # List of commonly used IP addresses
    common_countries = Column(JSON)  # List of commonly accessed countries
    common_cities = Column(JSON)  # List of commonly accessed cities
    common_times = Column(JSON)  # Common login times (hour of day)
    common_days = Column(JSON)  # Common login days (day of week)
    last_updated = Column(DateTime, default=func.now())
    
    # Relationships can be added here if needed

class LoginAnomaly(Base):
    """Model for storing detected login anomalies"""
    __tablename__ = "login_anomalies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    username = Column(String, index=True)
    login_event_id = Column(Integer, ForeignKey("user_login_events.id"))
    anomaly_type = Column(String, index=True)  # new_location, impossible_travel, brute_force, etc.
    severity = Column(String, index=True)  # low, medium, high
    description = Column(Text)
    timestamp = Column(DateTime, default=func.now())
    resolved = Column(Boolean, default=False)
    resolved_by = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationship to the login event
    login_event = relationship("UserLoginEvent")