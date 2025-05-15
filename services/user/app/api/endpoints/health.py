"""Health check endpoints for the User service."""
import time

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_client
from app.grpc.auth_client import AuthServiceClient

router = APIRouter(tags=["health"])


@router.get("/")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: The health check response.
    """
    return {
        "status": "ok",
        "service": "user",
        "timestamp": int(time.time()),
    }


@router.get("/auth-service")
async def check_auth_service_health(
    auth_client: AuthServiceClient = Depends(get_auth_client),
):
    """
    Check the health of the Auth service.
    
    Args:
        auth_client: The Auth service client.
        
    Returns:
        dict: The health check response.
    """
    health_check = auth_client.health_check("user")
    
    if not health_check or not health_check.status:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service is not healthy",
        )
    
    return {
        "status": "ok",
        "message": health_check.message,
        "timestamp": health_check.timestamp,
    }


@router.get("/grpc")
async def check_grpc_health():
    """
    Check the health of the gRPC server.
    
    Returns:
        dict: The health check response.
    """
    # In a real implementation, you might check if the gRPC server is running
    # For this example, we'll just return a success response
    return {
        "status": "ok",
        "service": "user-grpc",
        "timestamp": int(time.time()),
    }