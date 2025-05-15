"""API router for auth service."""
from fastapi import APIRouter

from app.api.endpoints import auth, profile, register, users

# Create main API router
api_router = APIRouter()

# Include routers from endpoints
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(users.router, prefix="/users")
api_router.include_router(register.router, prefix="/register")
api_router.include_router(profile.router, prefix="/profile")
