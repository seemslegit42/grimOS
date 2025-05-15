from fastapi import APIRouter

from app.api.v1.operations import workflow, integration

router = APIRouter(
    prefix="/operations",
    tags=["operations"],
)

router.include_router(workflow.router)
router.include_router(integration.router)
