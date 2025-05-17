from fastapi import APIRouter

from app.api.v1.security.router import router as security_router
from app.api.v1.operations.router import router as operations_router
from app.api.v1.cognitive.router import router as cognitive_router
from app.api.v1.auth.router import router as auth_router
from app.api.v1.admin.router import router as admin_router

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to GrimOS API v1"}

# Include module routers
router.include_router(security_router)
router.include_router(operations_router)
router.include_router(cognitive_router)
# Include auth router
router.include_router(auth_router, prefix="/auth", tags=["auth"])
# Include admin router
router.include_router(admin_router)