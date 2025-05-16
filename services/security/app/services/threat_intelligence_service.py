from sqlalchemy.orm import Session
import httpx
import json
import os
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import time

# For STIX/TAXII support
try:
    import stix2
    from taxii2client.v20 import Server, Collection
except ImportError:
    logging.warning("STIX/TAXII libraries not available. Some feed types may not work.")

import models
import schemas

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory cache for feed configurations (in a real implementation, this would be in the database)
FEED_CONFIGS = []

def get_threat_indicators(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    indicator_type: Optional[str] = None,
    source: Optional[str] = None
) -> List[models.ThreatIndicator]:
    """
    Get threat indicators with optional filtering
    """
    query = db.query(models.ThreatIndicator)
    
    if indicator_type:
        query = query.filter(models.ThreatIndicator.type == indicator_type)
    
    if source:
        query = query.filter(models.ThreatIndicator.source == source)
    
    return query.order_by(models.ThreatIndicator.created_at.desc()).offset(skip).limit(limit).all()

def create_threat_indicator(
    db: Session, 
    indicator: schemas.ThreatIndicatorCreate
) -> models.ThreatIndicator:
    """
    Create a new threat indicator
    """
    db_indicator = models.ThreatIndicator(
        type=indicator.type,
        value=indicator.value,
        source=indicator.source,
        confidence=indicator.confidence,
        description=indicator.description,
        metadata=indicator.metadata
    )
    
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    
    return db_indicator

def get_feed_configurations(db: Session) -> List[schemas.ThreatFeedConfig]:
    """
    Get all configured threat feeds
    """
    # In a real implementation, this would be stored in the database
    # For MVP, we'll use an in-memory list
    return FEED_CONFIGS

def create_feed_configuration(
    db: Session, 
    feed_config: schemas.ThreatFeedConfig
) -> schemas.ThreatFeedConfig:
    """
    Add a new threat feed configuration
    """
    # In a real implementation, this would be stored in the database
    # For MVP, we'll use an in-memory list
    FEED_CONFIGS.append(feed_config)
    return feed_config

async def ingest_feeds(db: Session, feed_name: Optional[str] = None):
    """
    Ingest threat intelligence from configured feeds
    """
    feeds_to_process = [f for f in FEED_CONFIGS if f.enabled]
    
    if feed_name:
        feeds_to_process = [f for f in feeds_to_process if f.name == feed_name]
    
    if not feeds_to_process:
        logger.warning(f"No enabled feeds found to process")
        return
    
    for feed in feeds_to_process:
        try:
            logger.info(f"Processing feed: {feed.name}")
            
            if feed.feed_type.lower() == "stix":
                await process_stix_feed(db, feed)
            elif feed.feed_type.lower() == "csv":
                await process_csv_feed(db, feed)
            elif feed.feed_type.lower() == "json":
                await process_json_feed(db, feed)
            else:
                logger.warning(f"Unsupported feed type: {feed.feed_type}")
        
        except Exception as e:
            logger.error(f"Error processing feed {feed.name}: {str(e)}")

async def process_stix_feed(db: Session, feed: schemas.ThreatFeedConfig):
    """
    Process a STIX/TAXII feed
    """
    try:
        # Connect to TAXII server
        server = Server(feed.url, auth=feed.api_key)
        
        # Get the collection
        if not feed.collection_id:
            logger.error(f"No collection ID specified for TAXII feed: {feed.name}")
            return
        
        collection = Collection(feed.collection_id, server)
        
        # Get objects from the collection
        response = collection.get_objects()
        
        # Process each object
        for obj in response.get('objects', []):
            try:
                stix_obj = stix2.parse(obj)
                
                # Handle different types of STIX objects
                if isinstance(stix_obj, stix2.v20.sdo.Indicator):
                    # Extract indicator value and type
                    pattern = stix_obj.pattern
                    indicator_type = "unknown"
                    indicator_value = "unknown"
                    
                    # Very basic pattern parsing (would be more robust in production)
                    if "ipv4-addr" in pattern:
                        indicator_type = "ip"
                        # Extract IP from pattern like [ipv4-addr:value = '1.2.3.4']
                        indicator_value = pattern.split("'")[1]
                    elif "domain-name" in pattern:
                        indicator_type = "domain"
                        indicator_value = pattern.split("'")[1]
                    elif "file:hashes" in pattern:
                        indicator_type = "hash"
                        indicator_value = pattern.split("'")[1]
                    
                    # Create the indicator
                    if indicator_type != "unknown" and indicator_value != "unknown":
                        create_threat_indicator(db, schemas.ThreatIndicatorCreate(
                            type=indicator_type,
                            value=indicator_value,
                            source=feed.name,
                            confidence=stix_obj.confidence if hasattr(stix_obj, 'confidence') else None,
                            description=stix_obj.description if hasattr(stix_obj, 'description') else None,
                            metadata={"stix_id": stix_obj.id}
                        ))
            
            except Exception as e:
                logger.error(f"Error processing STIX object: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error connecting to TAXII server: {str(e)}")

async def process_csv_feed(db: Session, feed: schemas.ThreatFeedConfig):
    """
    Process a CSV feed
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {}
            if feed.api_key:
                headers["Authorization"] = f"Bearer {feed.api_key}"
            
            response = await client.get(feed.url, headers=headers)
            response.raise_for_status()
            
            # Parse CSV content
            lines = response.text.strip().split('\n')
            if not lines:
                logger.warning(f"Empty CSV feed: {feed.name}")
                return
            
            # Assume first line is header
            headers = lines[0].split(',')
            
            # Process each line
            for line in lines[1:]:
                try:
                    values = line.split(',')
                    if len(values) != len(headers):
                        logger.warning(f"Malformed CSV line: {line}")
                        continue
                    
                    # Create a dict from headers and values
                    data = dict(zip(headers, values))
                    
                    # Extract indicator data based on common CSV formats
                    # This is a simplified example - real implementation would be more robust
                    indicator_type = data.get('type', data.get('indicator_type', 'unknown'))
                    indicator_value = data.get('value', data.get('indicator', data.get('ioc', 'unknown')))
                    
                    # Map common type names
                    if indicator_type.lower() in ['ip', 'ipv4', 'ipv6', 'ip_address']:
                        indicator_type = 'ip'
                    elif indicator_type.lower() in ['domain', 'hostname', 'domain_name']:
                        indicator_type = 'domain'
                    elif indicator_type.lower() in ['md5', 'sha1', 'sha256', 'hash']:
                        indicator_type = 'hash'
                    
                    # Create the indicator
                    if indicator_type != "unknown" and indicator_value != "unknown":
                        create_threat_indicator(db, schemas.ThreatIndicatorCreate(
                            type=indicator_type,
                            value=indicator_value,
                            source=feed.name,
                            confidence=float(data.get('confidence', 0)) if 'confidence' in data else None,
                            description=data.get('description', None),
                            metadata=data
                        ))
                
                except Exception as e:
                    logger.error(f"Error processing CSV line: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error fetching CSV feed: {str(e)}")

async def process_json_feed(db: Session, feed: schemas.ThreatFeedConfig):
    """
    Process a JSON feed
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {}
            if feed.api_key:
                headers["Authorization"] = f"Bearer {feed.api_key}"
            
            response = await client.get(feed.url, headers=headers)
            response.raise_for_status()
            
            # Parse JSON content
            data = response.json()
            
            # Handle different JSON formats
            # This is a simplified example - real implementation would be more robust
            indicators = []
            
            # Try to find indicators in common JSON structures
            if isinstance(data, list):
                indicators = data
            elif isinstance(data, dict):
                # Look for common field names that might contain indicators
                for field in ['indicators', 'data', 'results', 'items', 'objects']:
                    if field in data and isinstance(data[field], list):
                        indicators = data[field]
                        break
            
            if not indicators:
                logger.warning(f"Could not find indicators in JSON feed: {feed.name}")
                return
            
            # Process each indicator
            for item in indicators:
                try:
                    if not isinstance(item, dict):
                        continue
                    
                    # Extract indicator data based on common JSON formats
                    indicator_type = item.get('type', item.get('indicator_type', 'unknown'))
                    indicator_value = item.get('value', item.get('indicator', item.get('ioc', 'unknown')))
                    
                    # Map common type names
                    if indicator_type.lower() in ['ip', 'ipv4', 'ipv6', 'ip_address']:
                        indicator_type = 'ip'
                    elif indicator_type.lower() in ['domain', 'hostname', 'domain_name']:
                        indicator_type = 'domain'
                    elif indicator_type.lower() in ['md5', 'sha1', 'sha256', 'hash']:
                        indicator_type = 'hash'
                    
                    # Create the indicator
                    if indicator_type != "unknown" and indicator_value != "unknown":
                        create_threat_indicator(db, schemas.ThreatIndicatorCreate(
                            type=indicator_type,
                            value=indicator_value,
                            source=feed.name,
                            confidence=float(item.get('confidence', 0)) if 'confidence' in item else None,
                            description=item.get('description', None),
                            metadata=item
                        ))
                
                except Exception as e:
                    logger.error(f"Error processing JSON item: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error fetching JSON feed: {str(e)}")

# Initialize with some example feeds
def initialize_example_feeds():
    """
    Initialize with some example open-source threat feeds
    """
    example_feeds = [
        schemas.ThreatFeedConfig(
            name="AlienVault OTX",
            url="https://otx.alienvault.com/api/v1/indicators/export",
            api_key=None,  # Would need an API key in production
            feed_type="JSON",
            enabled=True
        ),
        schemas.ThreatFeedConfig(
            name="PhishTank",
            url="http://data.phishtank.com/data/online-valid.csv",
            api_key=None,
            feed_type="CSV",
            enabled=True
        )
    ]
    
    for feed in example_feeds:
        if feed not in FEED_CONFIGS:
            FEED_CONFIGS.append(feed)

# Initialize example feeds
initialize_example_feeds()