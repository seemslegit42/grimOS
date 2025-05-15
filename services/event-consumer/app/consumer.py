"""Kafka consumer for processing user events."""
import json
import logging
import time
import threading
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from confluent_kafka import Consumer, KafkaError, KafkaException
from pydantic import ValidationError

from app.config import settings
from app.schemas import EventProcessingResult, EventProcessingStatistics, EventType, UserEvent
from app.schema_validator import validator
import app.metrics as metrics

logger = logging.getLogger(__name__)


class DeadLetterQueue:
    """Simple in-memory dead letter queue for failed messages."""
    
    def __init__(self, max_size: int = 1000):
        """Initialize dead letter queue.
        
        Args:
            max_size: Maximum size of the queue
        """
        self.queue = []
        self.max_size = max_size
        self.lock = threading.Lock()
      def add(self, message: Dict[str, Any], error: str):
        """Add a message to the dead letter queue.
        
        Args:
            message: Message to add
            error: Error message
        """
        with self.lock:
            self.queue.append({
                "message": message,
                "error": error,
                "timestamp": datetime.now().isoformat()
            })
            
            # Trim queue if it exceeds max size
            if len(self.queue) > self.max_size:
                self.queue = self.queue[-self.max_size:]
            
            # Update metrics
            metrics.update_dlq_size(len(self.queue))
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all messages in the queue.
        
        Returns:
            List of messages
        """
        with self.lock:
            return list(self.queue)
    
    def clear(self):
        """Clear the queue."""
        with self.lock:
            self.queue = []


class RetryPolicy:
    """Retry policy for failed messages."""
    
    def __init__(self, max_retries: int = 3, initial_backoff_ms: int = 500,
                 max_backoff_ms: int = 10000, backoff_multiplier: float = 2.0):
        """Initialize retry policy.
        
        Args:
            max_retries: Maximum number of retries
            initial_backoff_ms: Initial backoff time in milliseconds
            max_backoff_ms: Maximum backoff time in milliseconds
            backoff_multiplier: Backoff multiplier for exponential backoff
        """
        self.max_retries = max_retries
        self.initial_backoff_ms = initial_backoff_ms
        self.max_backoff_ms = max_backoff_ms
        self.backoff_multiplier = backoff_multiplier
    
    def get_backoff_time(self, retry_count: int) -> float:
        """Get backoff time for a retry attempt.
        
        Args:
            retry_count: Retry attempt count (0-based)
            
        Returns:
            Backoff time in seconds
        """
        backoff_ms = min(
            self.initial_backoff_ms * (self.backoff_multiplier ** retry_count),
            self.max_backoff_ms
        )
        return backoff_ms / 1000  # Convert to seconds


class KafkaEventConsumer:
    """Kafka consumer for processing events."""
    
    def __init__(self, topics: List[str], group_id: str):
        """Initialize Kafka consumer.
        
        Args:
            topics: List of topics to subscribe to
            group_id: Consumer group ID
        """
        self.topics = topics
        self.group_id = group_id
        self.running = False
        self.consumer = None
        self.event_handlers = {}
        self.retry_policy = RetryPolicy()
        self.dead_letter_queue = DeadLetterQueue()
        self.stats = EventProcessingStatistics()
        self.processing_errors: Set[str] = set()  # Track message IDs with errors
        
        # Configure consumer
        self.config = {
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'group.id': group_id,
            'auto.offset.reset': settings.KAFKA_AUTO_OFFSET_RESET,
            'enable.auto.commit': False,  # Manual commit for better control
            'session.timeout.ms': 60000,  # 60 seconds
            'heartbeat.interval.ms': 20000,  # 20 seconds
            'max.poll.interval.ms': 300000,  # 5 minutes
            'fetch.min.bytes': 1,          # Get messages as soon as they're available
            'fetch.max.wait.ms': 500,      # Wait up to 500ms for min.bytes
        }
        
    def register_handler(self, event_type: str, handler: Callable[[Dict[str, Any]], EventProcessingResult]):
        """Register a handler for a specific event type.
        
        Args:
            event_type: Event type to handle
            handler: Handler function
        """
        self.event_handlers[event_type] = handler
        logger.info(f"Registered handler for event type: {event_type}")
    
    def get_statistics(self) -> EventProcessingStatistics:
        """Get event processing statistics.
        
        Returns:
            EventProcessingStatistics: Event processing statistics
        """
        return self.stats
    
    def get_dead_letter_queue(self) -> List[Dict[str, Any]]:
        """Get messages in the dead letter queue.
        
        Returns:
            List of messages
        """
        return self.dead_letter_queue.get_all()
      def start(self):
        """Start consuming messages."""
        try:
            # Initialize consumer
            self.consumer = Consumer(self.config)
            self.consumer.subscribe(self.topics)
            logger.info(f"Subscribed to topics: {self.topics}")
            
            self.running = True
            # Update metrics
            metrics.set_consumer_status(True)
            logger.info("Kafka consumer started")
            
            # Track processing time
            processing_start = None
            
            while self.running:
                try:
                    # Poll for messages
                    msg = self.consumer.poll(timeout=1.0)
                    
                    if msg is None:
                        continue
                    
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            # End of partition event - not an error
                            logger.debug(f"Reached end of partition: {msg.topic()}/{msg.partition()}")
                        else:
                            # Error
                            logger.error(f"Consumer error: {msg.error()}")
                        continue
                      # Start timing message processing
                    processing_start = time.time()
                    
                    # Process message
                    result = self._process_message(msg)
                    
                    # Update processing time statistics
                    if processing_start:
                        processing_time_ms = (time.time() - processing_start) * 1000
                        # Update average processing time
                        if self.stats.total_processed > 0:
                            self.stats.processing_time_ms_avg = (
                                (self.stats.processing_time_ms_avg * (self.stats.total_processed - 1) + processing_time_ms) 
                                / self.stats.total_processed
                            )
                        else:
                            self.stats.processing_time_ms_avg = processing_time_ms
                    
                    # Only commit offset if processing was successful or we've decided not to retry
                    if result or not getattr(msg, '_should_retry', False):
                        self.consumer.commit(msg)
                
                except KafkaException as e:
                    logger.error(f"Kafka exception: {e}")
                except Exception as e:
                    logger.exception(f"Unexpected error while consuming messages: {e}")
                    
                # Brief pause to prevent CPU spinning in case of continuous errors
                if len(self.processing_errors) > 10:
                    logger.warning(f"High error rate detected ({len(self.processing_errors)} errors), pausing briefly")
                    time.sleep(0.5)
                    self.processing_errors.clear()
        
        except Exception as e:
            logger.exception(f"Failed to start consumer: {e}")
        finally:
            self.stop()
      def stop(self):
        """Stop consuming messages."""
        self.running = False
        if self.consumer:
            self.consumer.close()
            # Update metrics
            metrics.set_consumer_status(False)
            logger.info("Kafka consumer stopped")
    
    def _process_message(self, msg, retry_count: int = 0) -> bool:
        """Process a Kafka message.
        
        Args:
            msg: Kafka message
            retry_count: Retry attempt count
            
        Returns:
            bool: True if message was successfully processed, False otherwise
        """
        message_id = f"{msg.topic()}-{msg.partition()}-{msg.offset()}"
        
        try:
            # Parse message value
            value = json.loads(msg.value().decode('utf-8'))
            logger.debug(f"Processing message: {message_id}")
            
            # Extract event type
            event_type = value.get('event_type')
            if not event_type:
                logger.warning(f"Message missing event_type: {value}")
                self.stats.failed += 1
                self.dead_letter_queue.add(value, "Missing event_type field")
                return False
              # Update event type stats
            if event_type in self.stats.event_types:
                self.stats.event_types[event_type] += 1
            else:
                self.stats.event_types[event_type] = 1
            
            # Find handler for event type
            handler = self.event_handlers.get(event_type)
            if not handler:
                logger.warning(f"No handler registered for event type: {event_type}")
                self.stats.failed += 1
                return False
            
            # Parse event
            try:
                # Check for correct event type enum value
                if hasattr(EventType, event_type.upper()):
                    # Convert string to enum value if needed
                    if isinstance(event_type, str):
                        event_type_enum = getattr(EventType, event_type.upper())
                        value['event_type'] = event_type_enum
                
                # Validate against Avro schema if available
                schema_name = "user_event"
                if not validator.validate(schema_name, value):
                    logger.warning(f"Message failed Avro schema validation for {schema_name}")
                    # We'll still try to process it with our Pydantic model
                
                event = UserEvent(**value)
                self.stats.last_event_timestamp = event.timestamp
            except ValidationError as e:
                logger.error(f"Failed to parse event: {e}")
                self.processing_errors.add(message_id)
                self.stats.failed += 1
                self.dead_letter_queue.add(value, f"Validation error: {e}")
                return False
              # Process event
            try:
                # Start timing the processing
                with metrics.observe_processing_time(event_type):
                    result = handler(event.model_dump())
                
                self.stats.total_processed += 1
                
                if result.success:
                    logger.info(f"Successfully processed {event_type} event: {result.message}")
                    self.stats.successful += 1
                    metrics.record_event_processed(event_type, success=True)
                    return True
                else:
                    logger.error(f"Failed to process {event_type} event: {result.error}")
                    self.processing_errors.add(message_id)
                    self.stats.failed += 1
                    metrics.record_event_processed(event_type, success=False)
                    
                    # Check if we should retry
                    if result.retry_recommended and retry_count < self.retry_policy.max_retries:
                        backoff = self.retry_policy.get_backoff_time(retry_count)
                        logger.info(f"Retrying message {message_id} in {backoff:.2f}s (attempt {retry_count+1}/{self.retry_policy.max_retries})")
                        
                        # Set retry flag on message
                        setattr(msg, '_should_retry', True)
                        
                        # Wait for backoff time
                        time.sleep(backoff)
                        
                        # Increment retry stats
                        self.stats.retried += 1
                        
                        # Retry processing
                        return self._process_message(msg, retry_count + 1)
                    
                    # No more retries
                    self.dead_letter_queue.add(value, result.error or "Unknown error")
                    return False
            
            except Exception as e:
                logger.exception(f"Error processing event: {e}")
                self.processing_errors.add(message_id)
                self.stats.failed += 1
                self.dead_letter_queue.add(value, str(e))
                return False
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode message: {e}")
            self.processing_errors.add(message_id)
            self.stats.failed += 1
            return False
        except Exception as e:
            logger.exception(f"Error processing message: {e}")
            self.processing_errors.add(message_id)
            self.stats.failed += 1
            return False


# Event handlers
def handle_user_registered(event: Dict[str, Any]) -> EventProcessingResult:
    """Handle user registered event.
    
    Args:
        event: User registered event
        
    Returns:
        EventProcessingResult: Processing result
    """
    try:
        user_id = event.get('user_id')
        user_data = event.get('data', {})
        email = user_data.get('email')
        timestamp = event.get('timestamp')
        
        logger.info(f"New user registered: {email} (ID: {user_id}) at {timestamp}")
        
        # Here you would typically:
        # 1. Send welcome email
        # Send welcome email to the user
        logger.info(f"Sending welcome email to {email}...")
        # send_welcome_email(email, user_data.get('full_name'))
        
        # 2. Create user profile in another service
        logger.info(f"Creating user profile for {email}...")
        # create_user_profile(user_id, email, user_data)
        
        # 3. Initialize user data in other systems
        logger.info(f"Initializing user data for {email}...")
        # initialize_user_data(user_id, email)
        
        # For demo purposes, we'll just simulate a success response
        # In real-world systems, you'd implement actual service calls
        
        return EventProcessingResult(
            success=True,
            message=f"Successfully processed user registration for {email}",
            event_id=user_id,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        # For demo, we'll simulate occasional retries
        should_retry = "timeout" in str(e).lower() or "connection" in str(e).lower()
        
        logger.exception(f"Error handling user_registered event: {e}")
        return EventProcessingResult(
            success=False,
            message="Failed to process user registration",
            error=str(e),
            retry_recommended=should_retry
        )


def handle_user_login(event: Dict[str, Any]) -> EventProcessingResult:
    """Handle user login event.
    
    Args:
        event: User login event
        
    Returns:
        EventProcessingResult: Processing result
    """
    try:
        user_id = event.get('user_id')
        user_data = event.get('data', {})
        email = user_data.get('email')
        metadata = event.get('metadata', {})
        
        # Check for required metadata
        ip_address = metadata.get('ip_address')
        user_agent = metadata.get('user_agent')
        device_info = metadata.get('device_info')
        
        logger.info(f"User login: {email} (ID: {user_id}) from IP {ip_address}")
        
        # Here you would typically:
        # 1. Update last login timestamp
        # 2. Check for suspicious activity
        # 3. Record session information
        
        return EventProcessingResult(
            success=True,
            message=f"Successfully processed login for {email}",
            event_id=user_id
        )
    
    except Exception as e:
        logger.exception(f"Error handling user_login event: {e}")
        return EventProcessingResult(
            success=False, 
            message="Failed to process user login",
            error=str(e),
            retry_recommended=True
        )


def handle_user_updated(event: Dict[str, Any]) -> EventProcessingResult:
    """Handle user updated event.
    
    Args:
        event: User updated event
        
    Returns:
        EventProcessingResult: Processing result
    """
    try:
        user_id = event.get('user_id')
        user_data = event.get('data', {})
        email = user_data.get('email')
        
        logger.info(f"User updated: {email} (ID: {user_id})")
        
        # Here you would typically:
        # 1. Update user profile in downstream services
        # 2. Sync user data to other systems
        
        return EventProcessingResult(
            success=True,
            message=f"Successfully processed user update for {email}",
            event_id=user_id
        )
    
    except Exception as e:
        logger.exception(f"Error handling user_updated event: {e}")
        return EventProcessingResult(
            success=False,
            message="Failed to process user update",
            error=str(e),
            retry_recommended=True
        )


def handle_user_deleted(event: Dict[str, Any]) -> EventProcessingResult:
    """Handle user deleted event.
    
    Args:
        event: User deleted event
        
    Returns:
        EventProcessingResult: Processing result
    """
    try:
        user_id = event.get('user_id')
        user_data = event.get('data', {})
        email = user_data.get('email')
        
        logger.info(f"User deleted: {email} (ID: {user_id})")
        
        # Here you would typically:
        # 1. Delete or deactivate user in downstream services
        # 2. Clean up associated data
        # 3. Archive user data if needed
        
        return EventProcessingResult(
            success=True,
            message=f"Successfully processed user deletion for {email}",
            event_id=user_id
        )
    
    except Exception as e:
        logger.exception(f"Error handling user_deleted event: {e}")
        return EventProcessingResult(
            success=False,
            message="Failed to process user deletion",
            error=str(e),
            retry_recommended=True
        )