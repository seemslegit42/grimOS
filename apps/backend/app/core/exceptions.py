from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """
    Base exception for API errors with additional context
    """
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: str = "error",
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code = code


class NotFoundError(BaseAPIException):
    """
    Raised when a requested resource is not found
    """
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND,
            code="not_found",
        )


class ValidationError(BaseAPIException):
    """
    Raised when validation fails on input data
    """
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="validation_error",
        )


class AuthorizationError(BaseAPIException):
    """
    Raised when a user is not authorized to perform an action
    """
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN,
            code="not_authorized",
        )


class AuthenticationError(BaseAPIException):
    """
    Raised when authentication fails
    """
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="not_authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


class RateLimitError(BaseAPIException):
    """
    Raised when a rate limit is exceeded
    """
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="rate_limit_exceeded",
        )


class ServiceUnavailableError(BaseAPIException):
    """
    Raised when a dependent service is unavailable
    """
    def __init__(self, detail: str = "Service unavailable"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="service_unavailable",
        )
