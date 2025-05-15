"""Kafka producer for auth service."""
import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, Optional, Union, List

from confluent_kafka import Producer, KafkaError, KafkaException
from pydantic import BaseModel, ValidationError

from app.core.config import settings

logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_CONFIG = {
    'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
    'client.id': 'auth-service-producer',
    'acks': 'all',            # Wait for all replicas to acknowledge
    'retries': 5,             # Retry up to 5 times
    'retry.backoff.ms': 500,  # 500ms between retries
    'linger.ms': 5,           # Wait for more messages before sending a batch
    'batch.size': 16384,      # Batch size
    'socket.keepalive.enable': True,  # Keep connection alive
    'request.timeout.ms': 30000,      # 30 seconds timeout
}

# Message schemas in dict form for validation
MESSAGE_SCHEMAS = {
    "user_registered": {
        "type": "object",
        "required": ["event_type", "user_id", "data", "timestamp"],
        "properties": {
            "event_type": {"type": "string", "enum": ["user_registered"]},
            "user_id": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
            "data": {
                "type": "object",
                "required": ["id", "email", "is_active"],
                "properties": {
                    "id": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "full_name": {"type": "string", "nullable": True},
                    "is_active": {"type": "boolean"},
                    "is_superuser": {"type": "boolean"}
                }
            }
        }
    }
}

# Initialize Kafka producer with retry logic
MAX_INIT_RETRIES = 3
producer = None

for retry in range(MAX_INIT_RETRIES):
    try:
        producer = Producer(KAFKA_CONFIG)
        logger.info("Kafka producer initialized successfully")
        break
    except Exception as e:
        logger.warning(f"Failed to initialize Kafka producer (attempt {retry+1}/{MAX_INIT_RETRIES}): {e}")
        if retry == MAX_INIT_RETRIES - 1:
            logger.error("All attempts to initialize Kafka producer failed")
            producer = None
        else:
            time.sleep(2 ** retry)  # Exponential backoff


def delivery_report(err: Any, msg: Any) -> None:
    """Delivery callback for Kafka producer.
    
    Args:
        err: Error object or None
        msg: Message object
    """
    if err is not None:
        error_code = err.code()
        if error_code == KafkaError._QUEUE_FULL:
            logger.error(f"Message delivery failed (queue full): {err}")
        elif error_code == KafkaError._MSG_TIMED_OUT:
            logger.error(f"Message delivery timed out: {err}")
        else:
            logger.error(f"Message delivery failed (code {error_code}): {err}")
    else:
        topic = msg.topic()
        partition = msg.partition()
        offset = msg.offset()
        key = msg.key().decode('utf-8') if msg.key() else None
        logger.info(f"Message delivered to {topic} [partition: {partition}, offset: {offset}, key: {key}]")


class RetryableError(Exception):
    """Error that can be retried."""
    pass


def validate_message(event_type: str, data: Dict[str, Any]) -> None:
    """Validate message against its schema.
    
    Args:
        event_type: Event type
        data: Message data
        
    Raises:
        ValidationError: If the message does not match its schema
    """
    if event_type not in MESSAGE_SCHEMAS:
        logger.warning(f"No schema defined for event type '{event_type}', skipping validation")
        return
    
    # Here we would typically use a proper JSON Schema validator
    # For now, we do basic validation of required fields
    schema = MESSAGE_SCHEMAS[event_type]
    required_fields = schema.get("properties", {}).keys()
    
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")


def publish_event(topic: str, key: str, data: Dict[str, Any] | BaseModel, 
                  max_retries: int = 3, validation: bool = True) -> bool:
    """Publish an event to Kafka with retry logic.
    
    Args:
        topic: Kafka topic
        key: Message key
        data: Message data (dict or Pydantic model)
        max_retries: Maximum number of retries
        validation: Whether to validate the message against its schema
        
    Returns:
        bool: True if message was published, False otherwise
    """
    if not settings.KAFKA_ENABLED:
        logger.info("Kafka is disabled, skipping event publication")
        return True
        
    if producer is None:
        logger.error("Kafka producer not initialized")
        return False
    
    # Extract data from Pydantic model if needed
    if isinstance(data, BaseModel):
        data_dict = data.model_dump()
        value = data.model_dump_json()
    else:
        data_dict = data
        value = json.dumps(data)
    
    # Validate message against schema if requested
    if validation:
        try:
            event_type = data_dict.get("event_type")
            if event_type:
                validate_message(event_type, data_dict)
        except ValidationError as e:
            logger.error(f"Message validation failed: {e}")
            return False


    # Attempt to publish the message with retries
    for retry in range(max_retries + 1):
        try:
            # Produce message
            producer.produce(
                topic=topic,
                key=key.encode('utf-8') if key else None,
                value=value.encode('utf-8'),
                timestamp=int(datetime.now().timestamp() * 1000),  # Add timestamp in milliseconds
                callback=delivery_report
            )
            
            # Poll to handle callbacks
            producer.poll(0)
            
            # Flush to ensure message is sent
            # Only wait for flush on the last attempt
            if retry == max_retries:
                flush_result = producer.flush(timeout=10)
                if flush_result > 0:
                    logger.warning(f"{flush_result} messages still in queue after flush timeout")
                    return False
            
            return True
            
        except KafkaException as e:
            error_code = e.args[0].code()
            # Handle specific error types
            if error_code == KafkaError._QUEUE_FULL:
                logger.warning(f"Kafka queue full, retrying ({retry+1}/{max_retries})")
                time.sleep(0.5 * (2 ** retry))  # Exponential backoff
                continue
            elif retry < max_retries:
                logger.warning(f"Kafka error, retrying ({retry+1}/{max_retries}): {e}")
                time.sleep(0.5 * (2 ** retry))  # Exponential backoff
                continue
            else:
                logger.error(f"Failed to publish event to Kafka after {max_retries} retries: {e}")
                return False
        except Exception as e:
            logger.error(f"Failed to publish event to Kafka: {e}")
            return False
    
    return False


def publish_user_event(event_type: str, user_id: str, user_data: Dict[str, Any] | BaseModel) -> bool:
    """Publish a user-related event to Kafka.
    
    Args:
        event_type: Type of event (e.g., 'created', 'updated', 'deleted')
        user_id: User ID
        user_data: User data (dict or Pydantic model)
        
    Returns:
        bool: True if message was published, False otherwise
    """
    # Create event payload with timestamp
    event = {
        "event_type": event_type,
        "user_id": user_id,
        "data": user_data.model_dump() if isinstance(user_data, BaseModel) else user_data,
        "timestamp": datetime.now().isoformat()
    }
    
    # Publish to user events topic
    return publish_event(
        topic=settings.KAFKA_USER_EVENTS_TOPIC,
        key=user_id,
        data=event
    )