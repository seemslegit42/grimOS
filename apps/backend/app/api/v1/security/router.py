from fastapi import APIRouter

from app.api.v1.security import threat_intelligence, uba, rbac

router = APIRouter(
    prefix="/security",
    tags=["security"],
)

router.include_router(threat_intelligence.router)
router.include_router(uba.router)
router.include_router(rbac.router)
