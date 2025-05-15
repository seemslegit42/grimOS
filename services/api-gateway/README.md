# Grimoire API Gateway

API Gateway for Grimoire OS microservices.

## Features

* Centralized API routing
* Authentication & authorization middleware
* Request validation
* Rate limiting
* Service discovery
* CORS handling
* Error handling
* Logging

## Tech Stack

* **Runtime**: Node.js
* **Framework**: Express.js
* **Proxy**: http-proxy-middleware
* **Authentication**: JWT (jose)
* **Security**: Helmet, CORS
* **Containerization**: Docker

## Getting Started

### Prerequisites

* Docker and Docker Compose
* Node.js 18+ (for local development)
* npm or yarn (for dependency management)

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
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Gateway Architecture

The API Gateway serves as the entry point for all client requests to the Grimoire microservices architecture. It handles:

1. **Routing**: Directs requests to the appropriate microservice
2. **Authentication**: Validates JWT tokens
3. **Rate Limiting**: Prevents abuse of the API
4. **Logging**: Records all requests for monitoring
5. **Error Handling**: Provides consistent error responses

## Microservice Communication

The API Gateway proxies requests to downstream services:

* **Auth Service**: User authentication and management
* _(Future services will be added here)_

## Security Considerations

* All requests to microservices pass through the gateway
* Authentication is verified before proxying protected endpoints
* Rate limiting prevents brute force and DDoS attacks
* HTTPS is enforced in production
* Security headers are added with Helmet

## Project Structure

```
api-gateway/
├── src/
│   ├── middlewares/         # Middleware functions
│   │   ├── auth.middleware.js    # Authentication middleware
│   │   ├── error.middleware.js   # Error handling middleware
│   │   └── proxy.middleware.js   # Service proxy middleware
│   ├── routes/              # Route definitions
│   │   └── auth.routes.js   # Auth service routes
│   └── index.js             # Main application
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── package.json             # npm configuration
└── README.md                # Documentation
```

## API Endpoints

| Endpoint         | Service      | Description              |
| ---------------- | ------------ | ------------------------ |
| `/api/v1/auth/*` | Auth Service | Authentication endpoints |
| `/health`        | API Gateway  | Health check endpoint    |

## Error Handling

The API Gateway provides standardized error responses:

```json
{
  "status": "error",
  "message": "Error description",
  "details": {} // Optional additional details
}
```

## Logging

Request logging is enabled by default using Morgan middleware. In production, you may want to integrate with a more robust logging solution.

## CI/CD

This service is designed to be deployed in a CI/CD pipeline. The Dockerfile provided can be used to build a production-ready image.

## Future Enhancements

* Add distributed tracing
* Implement circuit breaker pattern
* Add API key management for third-party access
* Add service discovery integration
* Implement request transformation
