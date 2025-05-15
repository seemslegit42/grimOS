"""Main application module for event consumer service."""
import logging
import signal
import sys
import threading
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prometheus_client import make_asgi_app

from app.config import settings
from app.consumer import (
    KafkaEventConsumer, 
    handle_user_registered, 
    handle_user_login,
    handle_user_updated,
    handle_user_deleted
)
from app.schemas import EventProcessingResult, EventProcessingStatistics
import app.metrics as metrics

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Create FastAPI app for health checks and metrics
app = FastAPI(
    title="GrimOS User Events Consumer",
    description="Consumes and processes user events from Kafka",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo - in production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Initialize Kafka consumer
consumer = KafkaEventConsumer(
    topics=[settings.KAFKA_USER_EVENTS_TOPIC],
    group_id=settings.KAFKA_GROUP_ID,
)

# Register event handlers
consumer.register_handler("user_registered", handle_user_registered)
consumer.register_handler("user_login", handle_user_login)
consumer.register_handler("user_updated", handle_user_updated)
consumer.register_handler("user_deleted", handle_user_deleted)

# Consumer thread
consumer_thread = None


@app.on_event("startup")
async def startup_event():
    """Start Kafka consumer on application startup."""
    global consumer_thread
    logger.info("Starting Kafka consumer thread")
    consumer_thread = threading.Thread(target=consumer.start, daemon=True)
    consumer_thread.start()


@app.on_event("shutdown")
async def shutdown_event():
    """Stop Kafka consumer on application shutdown."""
    logger.info("Stopping Kafka consumer")
    consumer.stop()
    if consumer_thread:
        consumer_thread.join(timeout=5.0)
    logger.info("Application shutdown complete")


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "event-consumer"}


@app.get("/metrics", tags=["monitoring"])
async def metrics():
    """Get consumer metrics and statistics."""
    stats = consumer.get_statistics()
    return stats.model_dump()


@app.get("/dead-letter-queue", tags=["monitoring"])
async def dead_letter_queue():
    """Get messages in the dead letter queue."""
    messages = consumer.get_dead_letter_queue()
    return {"count": len(messages), "messages": messages}


@app.post("/dead-letter-queue/clear", tags=["management"])
async def clear_dead_letter_queue():
    """Clear the dead letter queue."""
    consumer.dead_letter_queue.clear()
    return {"message": "Dead letter queue cleared"}


class RetryMessage(BaseModel):
    """Message to retry."""
    message: Dict[str, Any]


@app.post("/dead-letter-queue/retry", tags=["management"])
async def retry_message(message: RetryMessage):
    """Retry a message from the dead letter queue."""
    # Not implemented in this demo
    return {"message": "Retry functionality not implemented"}


def handle_signals():
    """Handle OS signals for graceful shutdown."""
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, shutting down...")
        consumer.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    import uvicorn
    
    # Handle signals for graceful shutdown
    handle_signals()
    
    # Start FastAPI application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "local",
    )