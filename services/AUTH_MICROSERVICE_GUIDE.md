# Authentication Microservice Guide

This guide explains how the authentication and user management functionality has been extracted from the monolithic FastAPI backend into a standalone microservice architecture.

## Architecture Overview

The new architecture consists of:

1. **Auth Microservice**: A FastAPI application that handles all authentication and user management
2. **API Gateway**: An Express.js application that routes requests to the appropriate microservice
3. **Shared Database**: PostgreSQL database used by the Auth service

## Components

### Auth Microservice (`/services/auth`)

The Auth microservice is responsible for:

* User authentication (login/logout)
* User registration
* Password reset functionality
* User management (CRUD operations)
* JWT token issuance and validation
* Refresh token management

Key technologies:

* FastAPI
* SQLAlchemy ORM
* Pydantic for validation
* JWT for authentication
* Alembic for migrations
* PostgreSQL for data storage

### API Gateway (`/services/api-gateway`)

The API Gateway serves as:

* Single entry point for all client requests
* Authentication verifier
* Request router to appropriate microservices
* Rate limiter
* Error handler

Key technologies:

* Express.js
* http-proxy-middleware
* jose for JWT verification
* helmet for security headers

## How to Run

1. Create a `.env` file (copy from `.env.example`) in the `/services` directory
2. Start the services:
   ```bash
   cd services
   make up
   ```
3. Run migrations:
   ```bash
   make migrate
   ```
4. Create an admin user:
   ```bash
   make create-admin
   ```

## API Endpoints

### Authentication

* `POST /api/v1/auth/login` - Login with email/password
* `POST /api/v1/auth/refresh` - Refresh access token
* `POST /api/v1/auth/logout` - Logout (invalidate refresh token)
* `GET /api/v1/auth/me` - Get current user information

### User Management

* `GET /api/v1/users` - List all users (admin only)
* `POST /api/v1/users` - Create a new user (admin only)
* `GET /api/v1/users/{user_id}` - Get user by ID
* `PUT /api/v1/users/{user_id}` - Update a user
* `DELETE /api/v1/users/{user_id}` - Delete a user (admin only)
* `PUT /api/v1/users/me/password` - Update current user's password

## Authentication Flow

1. **Login Flow**:

   * Client sends credentials to `/api/v1/auth/login`
   * Server validates credentials and issues access and refresh tokens
   * Client stores both tokens

2. **Making Authenticated Requests**:

   * Client includes access token in Authorization header
   * Gateway verifies token before forwarding request to microservice

3. **Token Refresh Flow**:

   * When access token expires, client sends refresh token to `/api/v1/auth/refresh`
   * Server validates refresh token and issues new access and refresh tokens
   * Old refresh token is invalidated

4. **Logout Flow**:
   * Client sends refresh token to `/api/v1/auth/logout`
   * Server invalidates the refresh token

## Security Considerations

* Access tokens have a short lifetime (default: 60 minutes)
* Refresh tokens have a longer lifetime (default: 7 days) but are tracked in the database
* All passwords are hashed using bcrypt
* Tokens include the user agent and IP address for tracking
* The API Gateway validates all tokens before forwarding requests
* Environment variables are used for all sensitive configuration

## Database Schema

The database schema includes:

1. **Users Table**:

   * `id` (UUID, primary key)
   * `email` (string, unique)
   * `hashed_password` (string)
   * `full_name` (string, nullable)
   * `is_active` (boolean)
   * `is_superuser` (boolean)
   * `created_at` (datetime)
   * `updated_at` (datetime)

2. **RefreshTokens Table**:
   * `id` (UUID, primary key)
   * `token` (string, unique)
   * `expires_at` (datetime)
   * `user_id` (UUID, foreign key to users)
   * `user_agent` (string, nullable)
   * `ip_address` (string, nullable)
   * `created_at` (datetime)

## Future Enhancements

1. **Service Discovery**: Implement service discovery for automatic registration
2. **Circuit Breaker**: Add circuit breaker pattern to handle service failures
3. **Distributed Tracing**: Implement distributed tracing for request tracking
4. **Metrics**: Add Prometheus metrics for monitoring
5. **OAuth Support**: Add OAuth 2.0 provider capabilities
6. **Multi-factor Authentication**: Implement MFA for additional security
