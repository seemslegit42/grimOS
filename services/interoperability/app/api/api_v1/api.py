"""
API router for Interoperability Engine
"""
from fastapi import APIRouter

from app.api.api_v1.endpoints import connectors, integrations, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(connectors.router, prefix="/connectors", tags=["connectors"])
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Additional endpoints to be implemented
# api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
