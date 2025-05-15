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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("api-gateway")


# Define service URLs from environment variables
SERVICE_URLS = {
    "backend": os.getenv("BACKEND_URL", "http://backend:8000"),
    "cognitive-core": os.getenv("COGNITIVE_CORE_URL", "http://cognitive-core:8001"),
    "composable-runes": os.getenv("COMPOSABLE_RUNES_URL", "http://composable-runes:8002"),
    "interoperability": os.getenv("INTEROPERABILITY_URL", "http://interoperability:8003"),
}

# Secret key for JWT token validation
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: setup clients
    logger.info("Starting API Gateway service")
    
    # Create and configure HTTP clients for backend services
    app.state.http_client = httpx.AsyncClient(timeout=30.0)
    
    # Register services
    app.state.service_registry = {
        "backend": {"url": SERVICE_URLS["backend"], "health": True},
        "cognitive-core": {"url": SERVICE_URLS["cognitive-core"], "health": True},
        "composable-runes": {"url": SERVICE_URLS["composable-runes"], "health": True},
        "interoperability": {"url": SERVICE_URLS["interoperability"], "health": True},
    }
    
    yield
    
    # Shutdown: close clients
    logger.info("Shutting down API Gateway service")
    await app.state.http_client.aclose()
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
