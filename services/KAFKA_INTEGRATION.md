# Kafka Integration for grimOS Microservices

This document explains how to use the Kafka messaging system in grimOS microservices architecture.

## Overview

The grimOS microservices use Apache Kafka as a message broker for asynchronous communication between services.
This implementation provides:

1. **Reliable messaging**: Guaranteed delivery with support for retries
2. **Async processing**: Non-blocking event publication using background tasks
3. **Schema validation**: Avro schema definition for message structure validation
4. **Dead letter queue**: Storage for failed messages with retry capabilities
5. **Monitoring**: Prometheus metrics for observability

## Architecture

The Kafka integration consists of the following components:

* **Kafka Broker**: The main message broker that stores and distributes messages
* **Zookeeper**: Manages the Kafka cluster state
* **Schema Registry**: Stores and validates Avro schemas
* **Kafka UI**: Web interface for monitoring and managing Kafka
* **Event Producers**: Services that publish events (e.g., the auth service)
* **Event Consumers**: Services that process events (e.g., the event-consumer service)

## Event Types

The system currently supports the following event types:

* `user_registered`: Published when a new user registers
* `user_updated`: Published when a user profile is updated
* `user_deleted`: Published when a user is deleted
* `user_login`: Published when a user logs in
* `user_logout`: Published when a user logs out
* `user_password_changed`: Published when a user changes their password
* `user_email_verified`: Published when a user verifies their email

## How to Use

### Publishing Events

In FastAPI services, you can use either synchronous or asynchronous producers:

**Synchronous Example:**

```python
from app.core.kafka import publish_user_event

# Publish an event
publish_user_event(
    event_type="user_registered",
    user_id=user_id,
    user_data=user_data
)
```

**Asynchronous Example:**

```python
from fastapi import BackgroundTasks
from app.core.async_kafka import publish_user_event as publish_user_event_async

async def register_user(
    background_tasks: BackgroundTasks,
    # other params...
):
    # Application logic...

    # Publish event in background
    background_tasks.add_task(
        publish_user_event_async,
        event_type="user_registered",
        user_id=user_id,
        user_data=user_data,
        metadata={"source": "api"}
    )
```

### Consuming Events

To consume events, implement a handler function and register it with the consumer:

```python
from app.schemas import EventProcessingResult

def handle_event(event: Dict[str, Any]) -> EventProcessingResult:
    # Process the event
    return EventProcessingResult(
        success=True,
        message="Event processed successfully"
    )

# Register the handler
consumer.register_handler("event_type", handle_event)
```

## Message Format

Messages follow this basic structure (defined in Avro schema):

```json
{
  "event_type": "user_registered",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2025-05-15T14:30:00.123456",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "roles": ["user"]
  },
  "metadata": {
    "source_ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0...",
    "request_id": "abcdef123456"
  }
}
```

## Monitoring

Monitoring is available via Prometheus metrics exposed at:

* `/metrics` endpoint on the event-consumer service

Available metrics include:

* Event processing counts (success/failure)
* Processing time histograms
* Dead letter queue size
* Consumer status

## Local Development

To run the Kafka system locally:

1. Start Kafka infrastructure:

   ```
   docker-compose up -d zookeeper kafka schema-registry kafka-ui
   ```

2. Access the Kafka UI at:

   ```
   http://localhost:8080
   ```

3. Start the event consumer:
   ```
   docker-compose up -d event-consumer
   ```

## Error Handling

The system implements:

* Automatic retries with exponential backoff
* Dead letter queue for failed messages
* Detailed error logging
* Validation at both schema and business logic levels

## Troubleshooting

Common issues:

* **Message not received by consumer**: Check Kafka broker status and topic configuration
* **Schema validation errors**: Verify the message structure against the Avro schema
* **Connection errors**: Ensure all services can connect to Kafka (network, credentials, etc.)

Check the service logs with:

```
docker-compose logs -f [service-name]
```
