"""API router configuration."""
from fastapi import APIRouter

from app.api.endpoints import health, profile

# Create API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(profile.router, prefix="/profile")
api_router.include_router(health.router, prefix="/health")