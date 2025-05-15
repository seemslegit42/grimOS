"""Prometheus metrics for the event consumer service."""
import time
from prometheus_client import Counter, Gauge, Histogram, Info

# Define metrics
EVENTS_PROCESSED = Counter(
    'events_processed_total',
    'Total number of events processed',
    ['event_type', 'status']
)

PROCESSING_TIME = Histogram(
    'event_processing_seconds',
    'Time spent processing events',
    ['event_type'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

DEAD_LETTER_QUEUE_SIZE = Gauge(
    'dead_letter_queue_size',
    'Number of messages in the dead letter queue'
)

CONSUMER_INFO = Info(
    'event_consumer',
    'Information about the event consumer'
)

CONSUMER_UP = Gauge(
    'event_consumer_up',
    'Whether the event consumer is running'
)

# Set initial values
CONSUMER_INFO.info({
    'version': '0.1.0',
    'kafka_bootstrap_servers': 'kafka:9092',
    'consumer_group': 'user-events-consumer'
})

CONSUMER_UP.set(1)  # 1 = up, 0 = down

# Helper functions for easier metric recording
def record_event_processed(event_type, success=True):
    """Record a processed event in Prometheus metrics.
    
    Args:
        event_type: Type of event
        success: Whether processing was successful
    """
    status = 'success' if success else 'failure'
    EVENTS_PROCESSED.labels(event_type=event_type, status=status).inc()


def observe_processing_time(event_type):
    """Create a context manager to observe processing time.
    
    Args:
        event_type: Type of event
        
    Returns:
        context manager that records processing time
    """
    class Timer:
        def __enter__(self):
            self.start = time.time()
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            duration = time.time() - self.start
            PROCESSING_TIME.labels(event_type=event_type).observe(duration)
    
    return Timer()


def update_dlq_size(size):
    """Update the dead letter queue size metric.
    
    Args:
        size: Current size of the dead letter queue
    """
    DEAD_LETTER_QUEUE_SIZE.set(size)


def set_consumer_status(is_running):
    """Update the consumer status metric.
    
    Args:
        is_running: Whether the consumer is running
    """
    CONSUMER_UP.set(1 if is_running else 0)
