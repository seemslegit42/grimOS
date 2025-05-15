from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal


class CompletionChoice(BaseModel):
    index: int
    text: str
    finish_reason: Optional[str] = None


class CompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionRequest(BaseModel):
    provider: Literal["openai", "gemini", "groq"] = Field(...)
    prompt: str = Field(...)
    model: Optional[str] = Field(None)
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None)
    stream: Optional[bool] = Field(False)


class CompletionResponse(BaseModel):
    id: str
    model: str
    created: int
    choices: List[CompletionChoice]
    usage: CompletionUsage