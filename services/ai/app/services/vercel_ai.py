from typing import Dict, Any, Optional, List, AsyncIterator, Literal, Union
import json
from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.services.ai_service import AIService


class VercelAISDK:
    """
    Integration with Vercel AI SDK
    Provides endpoints compatible with Vercel AI SDK client
    """
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        """
        Set up the routes for Vercel AI SDK
        """
        @self.router.post("/v1/chat/completions")
        async def chat_completions(request: Request) -> Union[Dict[str, Any], StreamingResponse]:
            """
            Vercel AI SDK compatible chat completions endpoint
            """
            body = await request.json()
            
            # Extract parameters
            messages = body.get("messages", [])
            model = body.get("model", None)
            temperature = body.get("temperature", 0.7)
            max_tokens = body.get("max_tokens", None)
            stream = body.get("stream", False)
            
            # Determine provider based on model prefix
            provider = "openai"  # Default
            if model:
                if model.startswith("gemini"):
                    provider = "gemini"
                elif model.startswith("llama") or model.startswith("mixtral"):
                    provider = "groq"
            
            if stream:
                async def generate() -> AsyncIterator[str]:
                    async for chunk in self.ai_service.generate_chat_completion(
                        provider=provider,
                        messages=messages,
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True,
                    ):
                        yield f"data: {chunk}\n\n"
                    yield "data: [DONE]\n\n"
                
                return StreamingResponse(
                    generate(),
                    media_type="text/event-stream",
                )
            else:
                response = await self.ai_service.generate_chat_completion(
                    provider=provider,
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=False,
                )
                return response
        
        @self.router.post("/v1/completions")
        async def completions(request: Request) -> Union[Dict[str, Any], StreamingResponse]:
            """
            Vercel AI SDK compatible completions endpoint
            """
            body = await request.json()
            
            # Extract parameters
            prompt = body.get("prompt", "")
            model = body.get("model", None)
            temperature = body.get("temperature", 0.7)
            max_tokens = body.get("max_tokens", None)
            stream = body.get("stream", False)
            
            # Determine provider based on model prefix
            provider = "openai"  # Default
            if model:
                if model.startswith("gemini"):
                    provider = "gemini"
                elif model.startswith("llama") or model.startswith("mixtral"):
                    provider = "groq"
            
            if stream:
                async def generate() -> AsyncIterator[str]:
                    async for chunk in self.ai_service.generate_text_completion(
                        provider=provider,
                        prompt=prompt,
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True,
                    ):
                        yield f"data: {chunk}\n\n"
                    yield "data: [DONE]\n\n"
                
                return StreamingResponse(
                    generate(),
                    media_type="text/event-stream",
                )
            else:
                response = await self.ai_service.generate_text_completion(
                    provider=provider,
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=False,
                )
                return response
        
        @self.router.post("/v1/embeddings")
        async def embeddings(request: Request) -> Dict[str, Any]:
            """
            Vercel AI SDK compatible embeddings endpoint
            """
            body = await request.json()
            
            # Extract parameters
            input_texts = body.get("input", [])
            if isinstance(input_texts, str):
                input_texts = [input_texts]
            
            model = body.get("model", None)
            
            # Determine provider based on model prefix
            provider = "openai"  # Default
            if model:
                if model.startswith("gemini"):
                    provider = "gemini"
            
            response = await self.ai_service.generate_embeddings(
                provider=provider,
                texts=input_texts,
                model=model,
            )
            return response
        
        @self.router.get("/v1/models")
        async def list_models() -> Dict[str, Any]:
            """
            List available models
            """
            models = [
                # OpenAI models
                {"id": "gpt-4o", "provider": "openai"},
                {"id": "gpt-4-turbo", "provider": "openai"},
                {"id": "gpt-3.5-turbo", "provider": "openai"},
                {"id": "text-embedding-3-small", "provider": "openai"},
                {"id": "text-embedding-3-large", "provider": "openai"},
                
                # Gemini models
                {"id": "gemini-1.5-pro", "provider": "gemini"},
                {"id": "gemini-1.5-flash", "provider": "gemini"},
                {"id": "gemini-1.0-pro", "provider": "gemini"},
                {"id": "embedding-001", "provider": "gemini"},
                
                # Groq models
                {"id": "llama3-70b-8192", "provider": "groq"},
                {"id": "llama3-8b-8192", "provider": "groq"},
                {"id": "mixtral-8x7b-32768", "provider": "groq"},
            ]
            
            return {"data": models}