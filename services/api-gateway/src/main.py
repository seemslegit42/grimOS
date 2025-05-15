"""
Enhanced API Gateway service for grimOS Universal API Fabric
"""
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, List, Any, Optional

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.auth import verify_token
from app.api.router import api_router
from app.services.service_registry import ServiceRegistry
from app.services.rate_limiter import RateLimiter


# Setup logging
logger = configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: setup clients
    logger.info("Starting API Gateway service")
    
    # Create and configure HTTP clients for backend services
    app.state.http_client = httpx.AsyncClient(timeout=30.0)
    app.state.service_registry = ServiceRegistry()
    app.state.rate_limiter = RateLimiter()
    
    # Register services
    await app.state.service_registry.register_services()
    
    # Start background tasks for service health checking
    # ...
    
    yield
    
    # Shutdown: clean up resources
    logger.info("Shutting down API Gateway service")
    await app.state.http_client.aclose()


app = FastAPI(
    title="grimOS Universal API Fabric",
    description="API Gateway for grimOS microservices",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to grimOS Universal API Fabric",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api-gateway"}


@app.get("/services")
async def list_services(request: Request):
    """List all registered services"""
    services = await request.app.state.service_registry.list_services()
    return {"services": services}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
