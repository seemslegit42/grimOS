from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.core.config import settings
from app.services.ai_providers import check_provider_status

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def health_check():
    """
    Check the health of the AI service and its providers
    """
    providers_status = {
        "openai": check_provider_status("openai"),
        "gemini": check_provider_status("gemini"),
        "groq": check_provider_status("groq"),
    }
    
    return {
        "status": "operational",
        "version": "1.0.0",
        "providers": providers_status,
        "config": {
            "default_openai_model": settings.DEFAULT_OPENAI_MODEL,
            "default_gemini_model": settings.DEFAULT_GEMINI_MODEL,
            "default_groq_model": settings.DEFAULT_GROQ_MODEL,
        }
    }