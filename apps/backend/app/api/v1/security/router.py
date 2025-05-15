from fastapi import APIRouter

from app.api.v1.security import threat_intelligence, uba

router = APIRouter(
    prefix="/security",
    tags=["security"],
)

router.include_router(threat_intelligence.router)
router.include_router(uba.router)
