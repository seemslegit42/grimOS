# grimOS Backend Setup Guide

This document provides instructions for setting up and running the grimOS backend.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Redis 6 or higher
- Kafka (optional for event-driven features)
- pip or uv (Python package manager)

## Getting Started

### Quick Setup

For a quick setup, simply run:

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
1. Create a virtual environment if it doesn't exist
2. Install all dependencies
3. Set up environment variables
4. Create the database if it doesn't exist
5. Run database migrations

### Manual Setup

1. Clone the repository if you haven't already:
   ```bash
   git clone https://github.com/yourusername/grimOS.git
   cd grimOS
   ```

2. Create a virtual environment and activate it:
   ```bash
   # Using Python's venv module
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # OR
   .venv\Scripts\activate     # On Windows
   ```

3. Install the dependencies:
   ```bash
   cd apps/backend
   pip install -e .
   # OR using uv (faster)
   uv pip install -e .
   ```

4. Set up the environment variables:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file to set your database connection string and other settings:
   ```
   DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/grimos
   REDIS_URL=redis://localhost:6379/0
   KAFKA_BOOTSTRAP_SERVERS=localhost:9092
   SECRET_KEY=your-secret-key-here
   ENVIRONMENT=development
   DEBUG=true
   ALLOWED_ORIGINS=http://localhost:3000
   ```

6. Initialize the database:
   ```bash
   # Create a PostgreSQL database
   createdb -U postgres grimos

   # Run migrations
   alembic upgrade head
   ```

## Running the Application

### Development Mode

```bash
# From the backend directory
uvicorn app.main:app --reload --port 8000
```

### Docker Setup

You can also run the entire stack using Docker Compose:

```bash
# From the root directory
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- Zookeeper and Kafka (for event processing)
- The grimOS backend

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Core Modules

The backend is structured into three main modules:

### 1. Security Module

Provides threat intelligence APIs and user behavior analytics (UBA) for detecting security anomalies.

### 2. Operations Module

Manages workflows and data integration from various sources.

### 3. Cognitive Core Module

Provides AI-powered data analysis and the ScrollWeaver natural language processing service for converting plain language to structured workflows.

## Development Guidelines

- Follow the repository pattern for database operations
- Use Pydantic models for data validation
- Add type hints to all functions
- Write tests for all new features
- Keep the code modular and maintainable

## Installing Additional Dependencies

If you need additional Python packages:

```bash
pip install package-name
```

Then add them to `pyproject.toml` to ensure reproducibility.

## Troubleshooting

- **Database connection issues**: Ensure PostgreSQL is running and the connection string is correct
- **Import errors**: Make sure your virtual environment is activated
- **Migration errors**: Check if the database exists and you have the right permissions
   alembic upgrade head
   ```

7. Start the development server:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   # OR using the provided script
   npm run dev
   ```

8. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Structure

The grimOS backend API is structured according to the API Design Specification. It consists of three main modules:

1. **Security Module APIs**
   - Threat Intelligence API
   - User Behavior Analytics (UBA) API

2. **Operations Module APIs**
   - Workflow Management API (RuneForge POC Backend)
   - Data Integration API

3. **Cognitive Core APIs**
   - Basic AI Data Analysis API
   - ScrollWeaver POC API (NL to Workflow Stub)

## Development

### Code Organization

- `app/api/` - API endpoints
- `app/models/` - SQLAlchemy ORM models
- `app/schemas/` - Pydantic schemas for validation and serialization
- `app/repositories/` - Data access layer
- `app/services/` - Business logic
- `app/core/` - Core application settings and utilities
- `app/db/` - Database setup and session management

### Testing

Run the tests with pytest:
```
pytest
```

### Linting

Lint the code with ruff:
```
ruff check .
```

Format the code with ruff:
```
ruff format .
```

## Deployment

For deployment instructions, see the `Grimoire™ (grimOS) - Deployment Plan for MVP.md` document in the `docs` directory.
