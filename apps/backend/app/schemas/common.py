from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

# Common models
class PaginationMeta(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    next_page: Optional[str] = None
    prev_page: Optional[str] = None

class PaginatedResponse(BaseModel):
    data: List[Any]
    pagination: PaginationMeta

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    issue: str

class ErrorResponse(BaseModel):
    error: Dict[str, Any]
