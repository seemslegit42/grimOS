from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Custom logic before request
        response = await call_next(request)
        # Custom logic after request
        return response
