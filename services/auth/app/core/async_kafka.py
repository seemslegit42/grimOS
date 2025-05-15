"""Async Kafka producer using aiokafka."""
import json
import logging
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global aiokafka producer
producer: Optional[AIOKafkaProducer] = None


async def get_producer() -> AIOKafkaProducer:
    """Get or create a Kafka producer.
    
    Returns:
        AIOKafkaProducer: Kafka producer
    """
    global producer
    
    if producer is None:
        try:
            # Create producer
            producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                client_id="auth-service-async-producer",
                enable_idempotence=True,  # Exactly-once delivery
                acks="all",               # Wait for all replicas
                max_batch_size=16384,     # 16KB batch size
                linger_ms=5,              # 5ms linger
                compression_type="gzip",  # Compress messages
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                retry_backoff_ms=100,     # 100ms between retries
                delivery_timeout_ms=30000, # 30s timeout
            )
            
            # Start producer
            await producer.start()
            logger.info("Async Kafka producer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize async Kafka producer: {e}")
            producer = None
    
    return producer


async def close_producer() -> None:
    """Close the Kafka producer."""
    global producer
    
    if producer is not None:
        await producer.stop()
        producer = None
        logger.info("Async Kafka producer closed")


async def publish_event(
    topic: str, 
    key: str, 
    data: Dict[str, Any] | BaseModel, 
    headers: Optional[List[tuple]] = None
) -> bool:
    """Publish an event to Kafka.
    
    Args:
        topic: Kafka topic
        key: Message key
        data: Message data (dict or Pydantic model)
        headers: Optional message headers
        
    Returns:
        bool: True if message was published, False otherwise
    """
    if not settings.KAFKA_ENABLED:
        logger.info("Kafka is disabled, skipping event publication")
        return True
    
    try:
        # Get producer
        producer = await get_producer()
        if producer is None:
            logger.error("Async Kafka producer not initialized")
            return False
        
        # Convert data to dict if it's a Pydantic model
        if isinstance(data, BaseModel):
            value = data.model_dump()
        else:
            value = data
        
        # Send message
        await producer.send_and_wait(
            topic=topic,
            key=key,
            value=value,
            headers=headers
        )
        
        logger.info(f"Event published to {topic} with key {key}")
        return True
    
    except KafkaError as e:
        logger.error(f"Kafka error: {e}")
        return False
    except Exception as e:
        logger.exception(f"Failed to publish event: {e}")
        return False


async def publish_user_event(
    event_type: str, 
    user_id: str, 
    user_data: Dict[str, Any] | BaseModel,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """Publish a user-related event to Kafka.
    
    Args:
        event_type: Type of event (e.g., 'created', 'updated', 'deleted')
        user_id: User ID
        user_data: User data (dict or Pydantic model)
        metadata: Additional metadata
        
    Returns:
        bool: True if message was published, False otherwise
    """
    # Create event payload
    event = {
        "event_type": event_type,
        "user_id": user_id,
        "data": user_data.model_dump() if isinstance(user_data, BaseModel) else user_data,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    
    # Add headers for message tracing
    headers = [
        ("event_type", event_type.encode('utf-8')),
        ("timestamp", datetime.now().isoformat().encode('utf-8')),
        ("source", "auth-service".encode('utf-8'))
    ]
    
    # Publish to user events topic
    return await publish_event(
        topic=settings.KAFKA_USER_EVENTS_TOPIC,
        key=user_id,
        data=event,
        headers=headers
    )


# Helper method to register shutdown handler in FastAPI
def setup_kafka_lifecycle(app):
    """Set up Kafka producer lifecycle handlers.
    
    Args:
        app: FastAPI application
    """
    @app.on_event("shutdown")
    async def shutdown_event():
        """Close Kafka producer on application shutdown."""
        await close_producer()
