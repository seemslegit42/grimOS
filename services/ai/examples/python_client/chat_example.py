import asyncio
import httpx
import json
from typing import List, Dict, Any, AsyncIterator


class AIServiceClient:
    """
    Python client for the grimOS AI Service
    """
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def close(self):
        await self.client.aclose()
    
    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        provider: str = "openai",
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = None,
        stream: bool = False,
    ) -> Any:
        """
        Generate a chat completion
        """
        url = f"{self.base_url}/api/v1/chat"
        if stream:
            url = f"{self.base_url}/api/v1/chat/stream"
        
        payload = {
            "provider": provider,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }
        
        if model:
            payload["model"] = model
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        if stream:
            async with self.client.stream("POST", url, json=payload) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        yield json.loads(data)
        else:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            return response.json()


async def main():
    # Initialize the client
    client = AIServiceClient()
    
    try:
        # Example 1: Non-streaming chat with OpenAI
        print("\n=== Example 1: OpenAI Chat ===")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
        
        response = await client.chat_completion(
            messages=messages,
            provider="openai",
            model="gpt-3.5-turbo",  # Use a smaller model for quick testing
        )
        
        print(f"OpenAI Response: {response['choices'][0]['message']['content']}")
        
        # Example 2: Streaming chat with Gemini
        print("\n=== Example 2: Gemini Streaming Chat ===")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a short poem about AI."}
        ]
        
        print("Gemini Streaming Response:")
        async for chunk in client.chat_completion(
            messages=messages,
            provider="gemini",
            model="gemini-1.5-flash",  # Use a smaller model for quick testing
            stream=True,
        ):
            content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
            if content:
                print(content, end="", flush=True)
        print("\n")
        
        # Example 3: Chat with Groq
        print("\n=== Example 3: Groq Chat ===")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain quantum computing in simple terms."}
        ]
        
        response = await client.chat_completion(
            messages=messages,
            provider="groq",
            model="llama3-8b-8192",  # Use a smaller model for quick testing
        )
        
        print(f"Groq Response: {response['choices'][0]['message']['content']}")
        
    finally:
        # Close the client
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())