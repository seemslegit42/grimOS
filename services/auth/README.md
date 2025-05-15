# Grimoire Auth Service

Authentication and User Management microservice for Grimoire OS.

## Features

* User authentication with JWT tokens (access + refresh tokens)
* User management (CRUD operations)
* Role-based access control
* Token revocation
* Password reset functionality
* Secure password hashing
* Service-to-service authentication

## Tech Stack

* **Framework**: FastAPI
* **Database**: PostgreSQL with SQLAlchemy ORM
* **Authentication**: JWT with Python-Jose
* **Password Hashing**: Passlib with BCrypt
* **Migration**: Alembic
* **Containerization**: Docker

## Getting Started

### Prerequisites

* Docker and Docker Compose
* Python 3.11+ (for local development)
* Poetry (for dependency management)

### Environment Setup

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Modify the values in `.env` to match your environment

### Running with Docker

```bash
docker-compose up -d
```

### Local Development

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Run migrations:

   ```bash
   alembic upgrade head
   ```

3. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the service is running, you can access the OpenAPI documentation at:

* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

## Authentication Flow

### Login Flow

1. User submits credentials (email/password)
2. Server validates credentials
3. If valid, server issues an access token and a refresh token
4. Access token is used for API authentication
5. Refresh token is used to obtain a new access token when it expires

### Token Refresh Flow

1. Client sends refresh token to the refresh endpoint
2. Server validates the refresh token
3. If valid, server issues a new access token and refresh token
4. Old refresh token is invalidated

## Security Considerations

* All passwords are hashed using BCrypt
* Access tokens have a short expiration time (default: 60 minutes)
* Refresh tokens have a longer expiration time (default: 7 days)
* Tokens can be revoked
* Service-to-service communication is secured with dedicated tokens

## Database Schema

### Users Table

* id (UUID, primary key)
* email (string, unique)
* hashed_password (string)
* full_name (string, nullable)
* is_active (boolean)
* is_superuser (boolean)
* created_at (datetime)
* updated_at (datetime)

### RefreshTokens Table

* id (UUID, primary key)
* token (string, unique)
* expires_at (datetime)
* user_id (UUID, foreign key)
* user_agent (string, nullable)
* ip_address (string, nullable)
* created_at (datetime)

## Project Structure

```
auth/
├── app/
│   ├── api/
│   │   ├── deps.py           # Dependencies
│   │   ├── endpoints/        # API route handlers
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   └── users.py      # User management endpoints
│   ├── core/
│   │   ├── config.py         # Configuration settings
│   │   └── security.py       # Security utilities
│   ├── crud/
│   │   └── user.py           # Database CRUD operations
│   ├── db/
│   │   ├── init_db.py        # Database initialization
│   │   ├── migrations/       # Alembic migrations
│   │   └── session.py        # Database session
│   ├── models/
│   │   └── user.py           # SQLAlchemy models
│   ├── schemas/
│   │   └── auth.py           # Pydantic schemas
│   └── main.py               # FastAPI application
├── tests/                    # Test modules
├── alembic.ini               # Alembic configuration
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── pyproject.toml            # Poetry configuration
└── README.md                 # Documentation
```

## Testing

Run tests with pytest:

```bash
pytest
```

## CI/CD

This service is designed to be deployed in a CI/CD pipeline. The Dockerfile provided can be used to build a production-ready image.
