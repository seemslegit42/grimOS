"""
API Gateway for grimOS microservices
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


app = FastAPI(
    title="grimOS API Gateway",
    description="Universal API Gateway for grimOS Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "grimOS API Gateway",
        "version": "1.0.0",
        "environment": ENVIRONMENT
    }


@app.get("/health")
async def health_check(request: Request):
    """Health check for API Gateway and downstream services"""
    registry = request.app.state.service_registry
    service_health = {}
    
    for service_name, service_info in registry.items():
        service_url = service_info["url"]
        service_status = "unknown"
        
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{service_url}/health")
                if response.status_code == 200:
                    service_status = "healthy"
                else:
                    service_status = "unhealthy"
        except Exception as e:
            logger.error(f"Error checking {service_name} health: {str(e)}")
            service_status = "unreachable"
        
        service_health[service_name] = service_status
    
    return {
        "status": "healthy",
        "services": service_health
    }


async def verify_authentication(request: Request):
    """Verify JWT token in Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header.split(" ")[1]
    
    # In a real implementation, validate the JWT token
    # TODO: Implement proper JWT validation
    
    # Mock user for development
    return {
        "id": "user-123",
        "username": "testuser",
        "roles": ["user"]
    }


# Proxy routes
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_request(
    service: str,
    path: str,
    request: Request,
    user: Dict = Depends(verify_authentication)
):
    """
    Proxy requests to microservices
    """
    # Check if service exists
    registry = request.app.state.service_registry
    if service not in registry:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")
    
    service_url = registry[service]["url"]
    client = request.app.state.http_client
    
    # Get request details
    method = request.method
    url = f"{service_url}/{path}"
    headers = dict(request.headers)
    
    # Add user information to headers
    headers["X-User-ID"] = user["id"]
    headers["X-Username"] = user["username"]
    headers["X-User-Roles"] = ",".join(user["roles"])
    
    # Remove host header to avoid conflicts
    if "host" in headers:
        del headers["host"]
    
    # Read request body for methods that may have one
    body = None
    if method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
    
    try:
        # Forward the request to the appropriate service
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params,
            follow_redirects=True
        )
        
        # Log the request
        logger.info(f"Proxied {method} request to {service}: {path}")
        
        # Return the response from the service
        return JSONResponse(
            content=response.json() if response.headers.get("content-type") == "application/json" else response.text,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.RequestError as exc:
        logger.error(f"Error proxying request to {service}: {str(exc)}")
        raise HTTPException(status_code=503, detail=f"Service '{service}' unavailable")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
