from typing import Dict, Any, Optional, List, AsyncIterator, Literal, Union
import time
import json
import uuid
from fastapi import Depends, HTTPException

from app.core.config import settings
from app.services.ai_providers import OpenAIProvider, GeminiProvider, GroqProvider


class AIService:
    """
    Main AI service that handles integration with all providers
    """
    def __init__(self):
        self.providers = {}
    
    def _get_provider(self, provider_name: Literal["openai", "gemini", "groq"]):
        """
        Get or initialize the requested provider
        """
        if provider_name not in self.providers:
            try:
                if provider_name == "openai":
                    self.providers[provider_name] = OpenAIProvider()
                elif provider_name == "gemini":
                    self.providers[provider_name] = GeminiProvider()
                elif provider_name == "groq":
                    self.providers[provider_name] = GroqProvider()
                else:
                    raise ValueError(f"Unsupported provider: {provider_name}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to initialize {provider_name} provider: {str(e)}")
        
        return self.providers[provider_name]
    
    async def generate_chat_completion(
        self,
        provider: Literal["openai", "gemini", "groq"],
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Union[Dict[str, Any], AsyncIterator[str]]:
        """
        Generate a chat completion using the specified provider
        """
        provider_instance = self._get_provider(provider)
        
        try:
            response = await provider_instance.generate_chat_completion(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )
            
            if stream:
                # Return a streaming response
                async def process_stream():
                    async for chunk in response:
                        # Format the chunk based on the provider
                        if provider == "openai":
                            yield json.dumps(chunk.model_dump())
                        elif provider == "gemini":
                            # Format Gemini chunk to match OpenAI format
                            gemini_chunk = {
                                "id": f"gemini-{uuid.uuid4()}",
                                "object": "chat.completion.chunk",
                                "created": int(time.time()),
                                "model": model or settings.DEFAULT_GEMINI_MODEL,
                                "choices": [
                                    {
                                        "index": 0,
                                        "delta": {
                                            "content": chunk.text
                                        },
                                        "finish_reason": None if not chunk.done else "stop"
                                    }
                                ]
                            }
                            yield json.dumps(gemini_chunk)
                        elif provider == "groq":
                            yield json.dumps(chunk.model_dump())
                
                return process_stream()
            else:
                # Format the response based on the provider
                if provider == "openai":
                    return response.model_dump()
                elif provider == "gemini":
                    # Format Gemini response to match OpenAI format
                    return {
                        "id": f"gemini-{uuid.uuid4()}",
                        "object": "chat.completion",
                        "created": int(time.time()),
                        "model": model or settings.DEFAULT_GEMINI_MODEL,
                        "choices": [
                            {
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": response.text
                                },
                                "finish_reason": "stop"
                            }
                        ],
                        "usage": {
                            "prompt_tokens": response.prompt_token_count if hasattr(response, "prompt_token_count") else 0,
                            "completion_tokens": response.candidates[0].token_count if hasattr(response, "candidates") and response.candidates else 0,
                            "total_tokens": (response.prompt_token_count if hasattr(response, "prompt_token_count") else 0) + 
                                           (response.candidates[0].token_count if hasattr(response, "candidates") and response.candidates else 0)
                        }
                    }
                elif provider == "groq":
                    return response.model_dump()
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating chat completion with {provider}: {str(e)}")
    
    async def generate_text_completion(
        self,
        provider: Literal["openai", "gemini", "groq"],
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Union[Dict[str, Any], AsyncIterator[str]]:
        """
        Generate a text completion using the specified provider
        """
        provider_instance = self._get_provider(provider)
        
        try:
            response = await provider_instance.generate_text_completion(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )
            
            if stream:
                # Return a streaming response
                async def process_stream():
                    async for chunk in response:
                        # Format the chunk based on the provider
                        if provider == "openai":
                            yield json.dumps(chunk.model_dump())
                        elif provider == "gemini":
                            # Format Gemini chunk to match OpenAI format
                            gemini_chunk = {
                                "id": f"gemini-{uuid.uuid4()}",
                                "object": "text_completion.chunk",
                                "created": int(time.time()),
                                "model": model or settings.DEFAULT_GEMINI_MODEL,
                                "choices": [
                                    {
                                        "index": 0,
                                        "text": chunk.text,
                                        "finish_reason": None if not chunk.done else "stop"
                                    }
                                ]
                            }
                            yield json.dumps(gemini_chunk)
                        elif provider == "groq":
                            yield json.dumps(chunk.model_dump())
                
                return process_stream()
            else:
                # Format the response based on the provider
                if provider == "openai":
                    return response.model_dump()
                elif provider == "gemini":
                    # Format Gemini response to match OpenAI format
                    return {
                        "id": f"gemini-{uuid.uuid4()}",
                        "object": "text_completion",
                        "created": int(time.time()),
                        "model": model or settings.DEFAULT_GEMINI_MODEL,
                        "choices": [
                            {
                                "index": 0,
                                "text": response.text,
                                "finish_reason": "stop"
                            }
                        ],
                        "usage": {
                            "prompt_tokens": response.prompt_token_count if hasattr(response, "prompt_token_count") else 0,
                            "completion_tokens": response.candidates[0].token_count if hasattr(response, "candidates") and response.candidates else 0,
                            "total_tokens": (response.prompt_token_count if hasattr(response, "prompt_token_count") else 0) + 
                                           (response.candidates[0].token_count if hasattr(response, "candidates") and response.candidates else 0)
                        }
                    }
                elif provider == "groq":
                    return response.model_dump()
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating text completion with {provider}: {str(e)}")
    
    async def generate_embeddings(
        self,
        provider: Literal["openai", "gemini"],
        texts: List[str],
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate embeddings using the specified provider
        Note: Groq doesn't support embeddings yet
        """
        if provider == "groq":
            raise HTTPException(status_code=400, detail="Groq does not support embeddings yet")
        
        provider_instance = self._get_provider(provider)
        
        try:
            response = await provider_instance.generate_embeddings(
                texts=texts,
                model=model,
            )
            
            # Format the response based on the provider
            if provider == "openai":
                # Extract embeddings from OpenAI response
                embeddings = [item.embedding for item in response.data]
                
                return {
                    "id": response.id,
                    "model": response.model,
                    "embeddings": embeddings,
                    "usage": response.usage.model_dump()
                }
            elif provider == "gemini":
                # Gemini response is already formatted in the provider
                return response
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating embeddings with {provider}: {str(e)}")