# grimOS Development Guide

This guide provides detailed information for developers working on the grimOS platform. It covers setup, architecture, coding standards, and development workflows.

## System Architecture

grimOS follows a microservices architecture with the following key components:

### Core Services

1. **Cognitive Core (AI Service)**
   - Agent lifecycle management
   - LLM integration and orchestration
   - Memory and knowledge management
   - Core reasoning capabilities

2. **Composable Runes (Workflow Engine)**
   - Workflow definitions with versioning
   - Workflow execution engine
   - Workflow monitoring and analytics
   - Task scheduling and orchestration

3. **Interoperability Engine (iPaaS Layer)**
   - System connectors for enterprise apps
   - Data transformation pipelines
   - Secure credential management
   - Integration monitoring and logging

4. **API Gateway**
   - Traffic routing to microservices
   - Authentication and authorization
   - Rate limiting and request validation
   - API documentation

### Data Infrastructure

- **PostgreSQL**: Primary relational database
- **Redis**: In-memory cache and message broker
- **MongoDB**: Flexible document store for connectors
- **Kafka**: Event streaming for inter-service communication
- **ChromaDB**: Vector database for embeddings

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ and pnpm
- Python 3.11+
- Git

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/your-org/grimos.git
   cd grimos
   ```

2. Run the setup script:
   ```
   ./setup-grimos.ps1  # Windows
   # or
   ./setup-grimos.sh   # Linux/macOS
   ```

3. Start the development environment:
   ```
   ./start-dev.ps1  # Windows
   # or
   ./start-dev.sh   # Linux/macOS
   ```

4. Access the services:
   - API Gateway: http://localhost:8080
   - Cognitive Core: http://localhost:8001
   - Composable Runes: http://localhost:8002
   - Interoperability Engine: http://localhost:8003
   - Frontend: http://localhost:3000

### Environment Configuration

Each service has its own `.env` file for configuration. The main environment variables include:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `MONGO_CONNECTION_STRING`: MongoDB connection string (for Interoperability Engine)
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka connection details
- `SECRET_KEY`: For JWT token signing
- API keys for various AI providers

## Component Development

### 1. Cognitive Core

Responsible for AI agent management and execution:

- Agent definitions and capabilities
- LLM provider integration (OpenAI, Google, etc.)
- Memory management and context handling
- Tool integration and execution

### 2. Composable Runes

Handles workflow creation and execution:

- Workflow models with versioning
- Step-by-step execution tracking
- Integration with the Cognitive Core
- Workflow templates and composition

### 3. Interoperability Engine

Manages external system integrations:

- Connector definitions for various systems
- Authentication and credential management
- Data transformation and mapping
- Integration monitoring and error handling

## API Standards

All APIs follow these standards:

- RESTful design with proper HTTP methods
- JSON for request/response payloads
- JWT-based authentication
- Versioning with `/api/v1/` prefix
- Comprehensive error responses

## Deployment

The platform can be deployed using:

1. **Docker Compose** (Development/Testing)
2. **Kubernetes** (Production)
   - Helm charts for each component
   - Infrastructure as Code with Terraform

## Contribution Guidelines

1. Create a feature branch from `main`
2. Follow the coding standards
3. Write unit tests for your changes
4. Update documentation as needed
5. Submit a pull request

## Troubleshooting

Common issues and solutions:

1. **Database connection errors**
   - Check PostgreSQL container is running
   - Verify connection strings in .env files

2. **Microservice communication issues**
   - Ensure Kafka is running properly
   - Check service discovery configuration

3. **Authentication problems**
   - Verify JWT secret key configuration
   - Check token expiration settings

## Resources and Documentation

- [Architecture Diagram](docs/architecture.png)
- [API Documentation](docs/api.md)
- [Data Models](docs/data-models.md)
- [Workflow Engine Guide](docs/workflow-engine.md)
- [Integration Guide](docs/integration.md)
