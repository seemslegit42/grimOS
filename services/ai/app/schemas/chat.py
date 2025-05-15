from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "function"] = Field(...)
    content: str = Field(...)
    name: Optional[str] = Field(None)


class ChatChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = None


class ChatUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatRequest(BaseModel):
    provider: Literal["openai", "gemini", "groq"] = Field(...)
    messages: List[ChatMessage] = Field(...)
    model: Optional[str] = Field(None)
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None)
    stream: Optional[bool] = Field(False)


class ChatResponse(BaseModel):
    id: str
    model: str
    created: int
    choices: List[ChatChoice]
    usage: ChatUsage