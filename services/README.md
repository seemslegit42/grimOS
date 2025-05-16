# grimOS Microservices

This directory contains the microservices architecture for Grimoire OS.

## Microservices

* **API Gateway**: Entry point for all client requests, handles authentication verification, routing, and rate limiting.
* **Auth Service**: Handles user authentication, registration, and account management.
* **User Service**: Manages user profiles, preferences, and activity.
* **Event Consumer**: Processes events from Kafka for asynchronous operations.

## Architecture

```
┌─────────────┐     ┌─────────────┐
│             │     │             │
│  Frontend   │────▶│ API Gateway │
│             │     │             │
└─────────────┘     └──────┬──────┘
                           │
                           ▼
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼
┌─────────────────┐               ┌─────────────────┐
│                 │  ◀─── gRPC ──▶│                 │
│  Auth Service   │               │  User Service   │
│                 │               │                 │
└────────┬────────┘               └────────┬────────┘
         │                                 │
         │                                 │
         ▼                                 ▼
┌─────────────────┐               ┌─────────────────┐
│                 │               │                 │
│  Auth Database  │               │  User Database  │
│                 │               │                 │
└─────────────────┘               └─────────────────┘
         │                                 │
         └─────────────┬─────────────────┬─┘
                       │                 │
                       ▼                 ▼
              ┌─────────────────┐ ┌─────────────────┐
              │                 │ │                 │
              │      Kafka      │ │ Event Consumer  │
              │                 │ │                 │
              └─────────────────┘ └─────────────────┘
```

## Getting Started

1. Create a `.env` file based on the example:

   ```bash
   cp .env.example .env
   ```

2. Generate gRPC code:

   ```bash
   chmod +x generate_grpc.sh
   ./generate_grpc.sh
   ```

3. Start the microservices:

   ```bash
   docker-compose up -d
   ```

4. API Gateway will be available at http://localhost:5000

## Development

Each microservice has its own directory with a README.md that explains how to work with that service.

### Inter-Service Communication

The Grimoire OS platform uses two primary methods for inter-service communication:

1. **gRPC** for synchronous communication (see [README_GRPC.md](./README_GRPC.md) for details)
2. **Kafka** for asynchronous event-driven communication

## Deployment

For production deployment, consider:

1. Using Kubernetes for orchestration
2. Setting up proper secrets management
3. Configuring TLS termination
4. Implementing monitoring and logging

## Security Considerations

* All sensitive values should be in the `.env` file and not committed to version control
* JWT secrets should be strong and rotated periodically
* Database credentials should be unique per environment
* In production, always use TLS for all services
* gRPC connections should use TLS in production

## Architecture Decisions

* **Stateless Services**: Each microservice is designed to be stateless, making them easy to scale horizontally.
* **Database Per Service**: Each service owns its database schema and data.
* **API Gateway Pattern**: Centralizes common concerns like authentication and routing.
* **JWT Authentication**: Enables efficient, stateless authentication between services.
* **gRPC Communication**: Provides efficient, type-safe synchronous communication between services.
* **Event-Driven Architecture**: Uses Kafka for asynchronous communication and event processing.

## Adding New Microservices

When adding a new microservice:

1. Create a new directory under `services/`
2. Add the service to the `docker-compose.yml` file
3. Configure the API gateway to route appropriate requests to the new service
4. If using gRPC, define the service interface in a `.proto` file and run `generate_grpc.sh`

## Testing

Each service has its own test suite. To run tests for all services:

```bash
docker-compose -f docker-compose.test.yml up
```

## Monitoring

For production environments, consider adding:

* Prometheus for metrics collection
* Grafana for visualization
* ELK stack for log aggregation

## Additional Documentation

* [gRPC Integration Guide](./README_GRPC.md) - Detailed guide for implementing and using gRPC
* [GRPC_INTEGRATION.md](./GRPC_INTEGRATION.md) - Technical reference for gRPC integration
