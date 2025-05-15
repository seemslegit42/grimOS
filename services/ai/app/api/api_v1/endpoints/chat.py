from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict, Any, AsyncIterator

from app.core.config import settings
from app.schemas.chat import ChatRequest, ChatMessage, ChatResponse
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/")
async def chat_completion(
    request: ChatRequest,
    ai_service: AIService = Depends(),
) -> ChatResponse:
    """
    Generate a chat completion response (non-streaming)
    """
    try:
        response = await ai_service.generate_chat_completion(
            provider=request.provider,
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False,
        )
        return ChatResponse(
            id=response.id,
            model=response.model,
            created=response.created,
            choices=response.choices,
            usage=response.usage,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def stream_chat_completion(
    request: ChatRequest,
    ai_service: AIService = Depends(),
) -> StreamingResponse:
    """
    Stream a chat completion response
    """
    try:
        async def generate() -> AsyncIterator[str]:
            async for chunk in ai_service.generate_chat_completion(
                provider=request.provider,
                messages=request.messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True,
            ):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))