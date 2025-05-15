"""Main application module for the User service."""
import logging
import threading

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.grpc.server import serve as serve_grpc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Create FastAPI app
app = FastAPI(
    title="Grimoire User Service",
    description="User Management microservice for Grimoire OS",
    version="0.1.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Configure CORS
if settings.ENVIRONMENT != "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "user"}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    # Log request
    logging.info(f"Request: {request.method} {request.url.path}")
    
    # Call next middleware or endpoint
    response = await call_next(request)
    
    # Log response
    logging.info(f"Response: {response.status_code}")
    
    return response


# Global variable to store the gRPC server
grpc_server = None


@app.on_event("startup")
async def startup_event():
    """Start the gRPC server when the FastAPI app starts."""
    global grpc_server
    # Start gRPC server in a separate thread
    grpc_thread = threading.Thread(
        target=lambda: setattr(globals(), "grpc_server", serve_grpc(port=settings.GRPC_SERVER_PORT)),
        daemon=True,
    )
    grpc_thread.start()
    logging.info("gRPC server thread started")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop the gRPC server when the FastAPI app stops."""
    global grpc_server
    if grpc_server:
        logging.info("Stopping gRPC server")
        grpc_server.stop(grace=None)  # Immediately stop the server