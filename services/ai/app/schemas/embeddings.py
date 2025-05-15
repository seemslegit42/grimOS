from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal


class EmbeddingUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class EmbeddingRequest(BaseModel):
    provider: Literal["openai", "gemini"] = Field(...)  # Note: Groq doesn't support embeddings yet
    texts: List[str] = Field(...)
    model: Optional[str] = Field(None)


class EmbeddingResponse(BaseModel):
    id: str
    model: str
    embeddings: List[List[float]]
    usage: EmbeddingUsage