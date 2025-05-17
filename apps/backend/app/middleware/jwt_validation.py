from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import verify_token

class JWTValidationMiddleware(BaseHTTPMiddleware):
    """Middleware to validate JWT access tokens."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/auth") or request.url.path == "/":
            # Skip validation for auth routes and root
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Missing or invalid Authorization header."
            )

        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            request.state.user = payload  # Attach user info to request state
        except ValueError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )

        return await call_next(request)
