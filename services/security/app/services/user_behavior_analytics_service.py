from sqlalchemy.orm import Session
import httpx
import json
import os
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import math
from collections import Counter

import models
import schemas

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optional GeoIP service
try:
    import geoip2.database
    GEOIP_ENABLED = True
    GEOIP_DB_PATH = os.getenv("GEOIP_DB_PATH", "./GeoLite2-City.mmdb")
    if not os.path.exists(GEOIP_DB_PATH):
        logger.warning(f"GeoIP database not found at {GEOIP_DB_PATH}. Geolocation will be disabled.")
        GEOIP_ENABLED = False
except ImportError:
    logger.warning("GeoIP library not available. Geolocation will be disabled.")
    GEOIP_ENABLED = False

def create_login_event(db: Session, login_event: schemas.UserLoginEventCreate) -> models.UserLoginEvent:
    """
    Create a new user login event
    """
    # Enrich with geolocation if available
    country = login_event.country
    city = login_event.city
    
    if not country and not city and GEOIP_ENABLED:
        try:
            with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
                response = reader.city(login_event.ip_address)
                country = response.country.name
                city = response.city.name
        except Exception as e:
            logger.warning(f"Error getting geolocation for IP {login_event.ip_address}: {str(e)}")
    
    # Create the login event
    db_login_event = models.UserLoginEvent(
        user_id=login_event.user_id,
        username=login_event.username,
        success=login_event.success,
        ip_address=login_event.ip_address,
        user_agent=login_event.user_agent,
        country=country,
        city=city
    )
    
    db.add(db_login_event)
    db.commit()
    db.refresh(db_login_event)
    
    return db_login_event

def get_login_events(
    db: Session,
    user_id: Optional[str] = None,
    username: Optional[str] = None,
    success: Optional[bool] = None,
    since_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.UserLoginEvent]:
    """
    Get user login events with optional filtering
    """
    query = db.query(models.UserLoginEvent)
    
    if user_id:
        query = query.filter(models.UserLoginEvent.user_id == user_id)
    
    if username:
        query = query.filter(models.UserLoginEvent.username == username)
    
    if success is not None:
        query = query.filter(models.UserLoginEvent.success == success)
    
    if since_date:
        query = query.filter(models.UserLoginEvent.timestamp >= since_date)
    
    return query.order_by(models.UserLoginEvent.timestamp.desc()).offset(skip).limit(limit).all()

def get_login_anomalies(
    db: Session,
    user_id: Optional[str] = None,
    username: Optional[str] = None,
    resolved: Optional[bool] = None,
    severity: Optional[str] = None,
    since_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.LoginAnomaly]:
    """
    Get login anomalies with optional filtering
    """
    query = db.query(models.LoginAnomaly)
    
    if user_id:
        query = query.filter(models.LoginAnomaly.user_id == user_id)
    
    if username:
        query = query.filter(models.LoginAnomaly.username == username)
    
    if resolved is not None:
        query = query.filter(models.LoginAnomaly.resolved == resolved)
    
    if severity:
        query = query.filter(models.LoginAnomaly.severity == severity)
    
    if since_date:
        query = query.filter(models.LoginAnomaly.timestamp >= since_date)
    
    return query.order_by(models.LoginAnomaly.timestamp.desc()).offset(skip).limit(limit).all()

def resolve_anomaly(
    db: Session,
    anomaly: models.LoginAnomaly,
    resolution: schemas.LoginAnomalyResolve
) -> models.LoginAnomaly:
    """
    Mark a login anomaly as resolved
    """
    anomaly.resolved = True
    anomaly.resolved_by = resolution.resolved_by
    anomaly.resolved_at = datetime.now()
    
    db.commit()
    db.refresh(anomaly)
    
    return anomaly

def analyze_login_event(db: Session, login_event_id: int):
    """
    Analyze a login event for anomalies
    """
    # Get the login event
    login_event = db.query(models.UserLoginEvent).filter(models.UserLoginEvent.id == login_event_id).first()
    if not login_event:
        logger.error(f"Login event with id {login_event_id} not found")
        return
    
    # Skip analysis for failed logins (they're handled separately)
    if not login_event.success:
        check_for_brute_force(db, login_event)
        return
    
    # Get the user's baseline
    baseline = db.query(models.UserLoginBaseline).filter(
        models.UserLoginBaseline.user_id == login_event.user_id
    ).first()
    
    # If no baseline exists, create one and skip analysis
    if not baseline:
        create_initial_baseline(db, login_event)
        return
    
    # Check for anomalies
    anomalies = []
    
    # Check for new location
    if login_event.country and login_event.country not in baseline.common_countries:
        anomalies.append({
            "type": "new_country",
            "severity": "medium",
            "description": f"Login from a new country: {login_event.country}"
        })
    
    if login_event.city and login_event.city not in baseline.common_cities:
        anomalies.append({
            "type": "new_city",
            "severity": "low",
            "description": f"Login from a new city: {login_event.city}"
        })
    
    if login_event.ip_address not in baseline.common_ip_addresses:
        anomalies.append({
            "type": "new_ip_address",
            "severity": "low",
            "description": f"Login from a new IP address: {login_event.ip_address}"
        })
    
    # Check for impossible travel
    check_for_impossible_travel(db, login_event, baseline, anomalies)
    
    # Check for unusual time
    login_hour = login_event.timestamp.hour
    if str(login_hour) not in baseline.common_times or baseline.common_times.get(str(login_hour), 0) < 3:
        anomalies.append({
            "type": "unusual_time",
            "severity": "low",
            "description": f"Login at unusual hour: {login_hour}:00"
        })
    
    # Create anomaly records
    for anomaly in anomalies:
        db_anomaly = models.LoginAnomaly(
            user_id=login_event.user_id,
            username=login_event.username,
            login_event_id=login_event.id,
            anomaly_type=anomaly["type"],
            severity=anomaly["severity"],
            description=anomaly["description"]
        )
        
        db.add(db_anomaly)
    
    db.commit()

def check_for_brute_force(db: Session, login_event: models.UserLoginEvent):
    """
    Check for brute force login attempts
    """
    if login_event.success:
        return
    
    # Look for multiple failed logins in the last hour
    one_hour_ago = login_event.timestamp - timedelta(hours=1)
    
    failed_count = db.query(models.UserLoginEvent).filter(
        models.UserLoginEvent.user_id == login_event.user_id,
        models.UserLoginEvent.success == False,
        models.UserLoginEvent.timestamp >= one_hour_ago
    ).count()
    
    # If there are more than 5 failed attempts in the last hour, create an anomaly
    if failed_count >= 5:
        # Check if we already have a brute_force anomaly for this user in the last hour
        existing_anomaly = db.query(models.LoginAnomaly).filter(
            models.LoginAnomaly.user_id == login_event.user_id,
            models.LoginAnomaly.anomaly_type == "brute_force",
            models.LoginAnomaly.timestamp >= one_hour_ago
        ).first()
        
        if not existing_anomaly:
            db_anomaly = models.LoginAnomaly(
                user_id=login_event.user_id,
                username=login_event.username,
                login_event_id=login_event.id,
                anomaly_type="brute_force",
                severity="high",
                description=f"Multiple failed login attempts ({failed_count} in the last hour)"
            )
            
            db.add(db_anomaly)
            db.commit()

def check_for_impossible_travel(
    db: Session, 
    login_event: models.UserLoginEvent, 
    baseline: models.UserLoginBaseline,
    anomalies: List[Dict[str, str]]
):
    """
    Check for impossible travel (login from different locations in an impossibly short time)
    """
    if not login_event.country or not login_event.city:
        return
    
    # Get the user's most recent successful login before this one
    previous_login = db.query(models.UserLoginEvent).filter(
        models.UserLoginEvent.user_id == login_event.user_id,
        models.UserLoginEvent.success == True,
        models.UserLoginEvent.id != login_event.id,
        models.UserLoginEvent.timestamp < login_event.timestamp
    ).order_by(models.UserLoginEvent.timestamp.desc()).first()
    
    if not previous_login or not previous_login.country or not previous_login.city:
        return
    
    # If the locations are the same, no need to check
    if (previous_login.country == login_event.country and 
        previous_login.city == login_event.city):
        return
    
    # Calculate time difference in hours
    time_diff = (login_event.timestamp - previous_login.timestamp).total_seconds() / 3600
    
    # Very simplified check - in a real system, we would use actual distance calculations
    # and more sophisticated travel time estimates
    if previous_login.country != login_event.country:
        # Different countries - assume minimum 4 hours for travel
        if time_diff < 4:
            anomalies.append({
                "type": "impossible_travel",
                "severity": "high",
                "description": (
                    f"Impossible travel detected: Login from {login_event.city}, {login_event.country} "
                    f"only {time_diff:.1f} hours after login from {previous_login.city}, {previous_login.country}"
                )
            })

def create_initial_baseline(db: Session, login_event: models.UserLoginEvent):
    """
    Create an initial baseline for a user based on their first login
    """
    baseline = models.UserLoginBaseline(
        user_id=login_event.user_id,
        username=login_event.username,
        common_ip_addresses=[login_event.ip_address] if login_event.ip_address else [],
        common_countries=[login_event.country] if login_event.country else [],
        common_cities=[login_event.city] if login_event.city else [],
        common_times={str(login_event.timestamp.hour): 1},
        common_days={str(login_event.timestamp.weekday()): 1}
    )
    
    db.add(baseline)
    db.commit()

def update_user_baselines(db: Session, user_id: Optional[str] = None):
    """
    Update user login behavior baselines
    """
    # Get users to update
    if user_id:
        users = [user_id]
    else:
        # Get all unique user IDs from login events
        user_records = db.query(models.UserLoginEvent.user_id).distinct().all()
        users = [record[0] for record in user_records]
    
    # Process each user
    for uid in users:
        try:
            # Get successful login events for this user in the last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            login_events = db.query(models.UserLoginEvent).filter(
                models.UserLoginEvent.user_id == uid,
                models.UserLoginEvent.success == True,
                models.UserLoginEvent.timestamp >= thirty_days_ago
            ).all()
            
            if not login_events:
                logger.info(f"No recent login events for user {uid}")
                continue
            
            # Extract data for baseline
            ip_addresses = [event.ip_address for event in login_events if event.ip_address]
            countries = [event.country for event in login_events if event.country]
            cities = [event.city for event in login_events if event.city]
            
            # Count occurrences of each hour and day
            hours = [event.timestamp.hour for event in login_events]
            days = [event.timestamp.weekday() for event in login_events]
            
            hour_counts = Counter(hours)
            day_counts = Counter(days)
            
            # Get or create baseline
            baseline = db.query(models.UserLoginBaseline).filter(
                models.UserLoginBaseline.user_id == uid
            ).first()
            
            if not baseline:
                # Get username from the most recent login
                username = login_events[0].username if login_events else "unknown"
                
                baseline = models.UserLoginBaseline(
                    user_id=uid,
                    username=username,
                    common_ip_addresses=[],
                    common_countries=[],
                    common_cities=[],
                    common_times={},
                    common_days={}
                )
                db.add(baseline)
            
            # Update baseline
            # For IP addresses, countries, and cities, we'll keep the most common ones
            baseline.common_ip_addresses = [ip for ip, count in Counter(ip_addresses).most_common(10)]
            baseline.common_countries = [country for country, count in Counter(countries).most_common(5)]
            baseline.common_cities = [city for city, count in Counter(cities).most_common(10)]
            
            # For hours and days, we'll keep the counts
            baseline.common_times = {str(hour): count for hour, count in hour_counts.items()}
            baseline.common_days = {str(day): count for day, count in day_counts.items()}
            
            baseline.last_updated = datetime.now()
            
            db.commit()
            
            logger.info(f"Updated baseline for user {uid}")
        
        except Exception as e:
            logger.error(f"Error updating baseline for user {uid}: {str(e)}")
            db.rollback()