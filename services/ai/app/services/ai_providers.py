from typing import Dict, Any, Optional, List, AsyncIterator, Literal
import time
import json
import os
from app.core.config import settings

# Provider status cache to avoid repeated API calls
provider_status_cache = {
    "openai": {"status": "unknown", "last_checked": 0},
    "gemini": {"status": "unknown", "last_checked": 0},
    "groq": {"status": "unknown", "last_checked": 0},
}

# Cache expiration time in seconds
CACHE_EXPIRATION = 300  # 5 minutes


def check_provider_status(provider: Literal["openai", "gemini", "groq"]) -> Dict[str, Any]:
    """
    Check if the provider is configured and available
    Returns cached status if checked recently
    """
    current_time = time.time()
    
    # Return cached status if still valid
    if current_time - provider_status_cache[provider]["last_checked"] < CACHE_EXPIRATION:
        return {
            "status": provider_status_cache[provider]["status"],
            "last_checked": provider_status_cache[provider]["last_checked"]
        }
    
    # Check if API key is configured
    api_key = None
    if provider == "openai":
        api_key = settings.OPENAI_API_KEY
    elif provider == "gemini":
        api_key = settings.GEMINI_API_KEY
    elif provider == "groq":
        api_key = settings.GROQ_API_KEY
    
    status = "configured" if api_key else "not_configured"
    
    # Update cache
    provider_status_cache[provider] = {
        "status": status,
        "last_checked": current_time
    }
    
    return {
        "status": status,
        "last_checked": current_time
    }


class OpenAIProvider:
    """
    OpenAI provider implementation using Vercel AI SDK
    """
    def __init__(self):
        from openai import AsyncOpenAI
        
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.default_model = settings.DEFAULT_OPENAI_MODEL
    
    async def generate_chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Any:
        """
        Generate a chat completion using OpenAI
        """
        model = model or self.default_model
        
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        )
        
        return response
    
    async def generate_text_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Any:
        """
        Generate a text completion using OpenAI
        """
        model = model or self.default_model
        
        # Convert to chat format since OpenAI deprecated the completions endpoint
        messages = [{"role": "user", "content": prompt}]
        
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        )
        
        return response
    
    async def generate_embeddings(
        self,
        texts: List[str],
        model: Optional[str] = None,
    ) -> Any:
        """
        Generate embeddings using OpenAI
        """
        model = model or "text-embedding-3-small"
        
        response = await self.client.embeddings.create(
            model=model,
            input=texts,
        )
        
        return response


class GeminiProvider:
    """
    Google Gemini provider implementation using Vercel AI SDK
    """
    def __init__(self):
        import google.generativeai as genai
        
        if not settings.GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.genai = genai
        self.default_model = settings.DEFAULT_GEMINI_MODEL
    
    async def generate_chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Any:
        """
        Generate a chat completion using Gemini
        """
        model = model or self.default_model
        
        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model" if msg["role"] == "assistant" else msg["role"]
            gemini_messages.append({"role": role, "parts": [msg["content"]]})
        
        # Initialize the model
        gemini_model = self.genai.GenerativeModel(model)
        
        # Create a chat session
        chat = gemini_model.start_chat(history=gemini_messages)
        
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens if max_tokens else 1024,
        }
        
        # Generate response
        if stream:
            response = await chat.send_message_async(
                "",
                generation_config=generation_config,
                stream=True
            )
            return response
        else:
            response = await chat.send_message_async(
                "",
                generation_config=generation_config,
            )
            return response
    
    async def generate_text_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Any:
        """
        Generate a text completion using Gemini
        """
        model = model or self.default_model
        
        # Initialize the model
        gemini_model = self.genai.GenerativeModel(model)
        
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens if max_tokens else 1024,
        }
        
        # Generate response
        if stream:
            response = await gemini_model.generate_content_async(
                prompt,
                generation_config=generation_config,
                stream=True
            )
            return response
        else:
            response = await gemini_model.generate_content_async(
                prompt,
                generation_config=generation_config,
            )
            return response
    
    async def generate_embeddings(
        self,
        texts: List[str],
        model: Optional[str] = None,
    ) -> Any:
        """
        Generate embeddings using Gemini
        """
        model = model or "embedding-001"
        
        embedding_model = self.genai.GenerativeModel(model)
        
        # Process each text and get embeddings
        embeddings = []
        for text in texts:
            result = await embedding_model.embed_content_async(text)
            embeddings.append(result.embedding)
        
        # Create a response similar to OpenAI format
        response = {
            "id": f"gemini-{int(time.time())}",
            "model": model,
            "embeddings": embeddings,
            "usage": {
                "prompt_tokens": sum(len(text.split()) for text in texts),
                "total_tokens": sum(len(text.split()) for text in texts),
            }
        }
        
        return response


class GroqProvider:
    """
    Groq provider implementation using Vercel AI SDK
    """
    def __init__(self):
        from groq import AsyncGroq
        
        if not settings.GROQ_API_KEY:
            raise ValueError("Groq API key not configured")
        
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.default_model = settings.DEFAULT_GROQ_MODEL
    
    async def generate_chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Any:
        """
        Generate a chat completion using Groq
        """
        model = model or self.default_model
        
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        )
        
        return response
    
    async def generate_text_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Any:
        """
        Generate a text completion using Groq
        """
        model = model or self.default_model
        
        # Convert to chat format
        messages = [{"role": "user", "content": prompt}]
        
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        )
        
        return response
    
    # Note: Groq doesn't support embeddings yet, so we don't implement generate_embeddings