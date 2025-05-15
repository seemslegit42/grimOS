"""
API router for Composable Runes
"""
from fastapi import APIRouter

from app.api.api_v1.endpoints import workflows, runes, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Additional endpoints to be implemented
# api_router.include_router(runes.router, prefix="/runes", tags=["runes"])
