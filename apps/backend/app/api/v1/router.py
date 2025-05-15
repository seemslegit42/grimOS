from fastapi import APIRouter

from app.api.v1.security.router import router as security_router
from app.api.v1.operations.router import router as operations_router
from app.api.v1.cognitive.router import router as cognitive_router

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to GrimOS API v1"}

# Include module routers
router.include_router(security_router)
router.include_router(operations_router)
router.include_router(cognitive_router)