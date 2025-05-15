from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any

from app.core.config import settings
from app.schemas.embeddings import EmbeddingRequest, EmbeddingResponse
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/")
async def create_embeddings(
    request: EmbeddingRequest,
    ai_service: AIService = Depends(),
) -> EmbeddingResponse:
    """
    Generate embeddings for the given texts
    """
    try:
        response = await ai_service.generate_embeddings(
            provider=request.provider,
            texts=request.texts,
            model=request.model,
        )
        return EmbeddingResponse(
            id=response.id,
            model=response.model,
            embeddings=response.embeddings,
            usage=response.usage,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))