from fastapi import APIRouter
from app.api.endpoints import demo

api_router = APIRouter()

# Include the demo stats endpoint
api_router.include_router(demo.router, prefix="/stats", tags=["stats"])