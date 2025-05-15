from fastapi import APIRouter

from app.api.v1.cognitive import analysis, scrollweaver

router = APIRouter(
    prefix="/cognitive",
    tags=["cognitive"],
)

router.include_router(analysis.router)
router.include_router(scrollweaver.router)
