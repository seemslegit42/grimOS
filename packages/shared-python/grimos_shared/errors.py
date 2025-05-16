"""
Error handling utilities for grimOS backend services.

This module provides standardized error handling utilities for backend microservices.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class ErrorCode(str, Enum):
    """Standard error codes used across the application."""
    
    # Authentication and authorization errors
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    
    # Resource errors
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    CONFLICT = "CONFLICT"
    
    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_FIELD = "MISSING_FIELD"
    
    # Server errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    DATABASE_ERROR = "DATABASE_ERROR"
    
    # External service errors
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    INTEGRATION_ERROR = "INTEGRATION_ERROR"
    
    # Rate limiting
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    
    # Business logic errors
    BUSINESS_LOGIC_ERROR = "BUSINESS_LOGIC_ERROR"


class ErrorDetail(BaseModel):
    """Detailed error information."""
    
    loc: List[str] = Field(..., description="Location of the error")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")


class ErrorResponse(BaseModel):
    """Standardized error response format."""
    
    code: ErrorCode = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[List[ErrorDetail]] = Field(None, description="Detailed error information")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")


class AppException(Exception):
    """Base exception for application-specific errors."""
    
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[List[ErrorDetail]] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class NotFoundError(AppException):
    """Resource not found error."""
    
    def __init__(
        self,
        message: str = "Resource not found",
        details: Optional[List[ErrorDetail]] = None
    ):
        super().__init__(
            code=ErrorCode.NOT_FOUND,
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class ValidationError(AppException):
    """Validation error."""
    
    def __init__(
        self,
        message: str = "Validation error",
        details: Optional[List[ErrorDetail]] = None
    ):
        super().__init__(
            code=ErrorCode.VALIDATION_ERROR,
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class AuthenticationError(AppException):
    """Authentication error."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[List[ErrorDetail]] = None
    ):
        super().__init__(
            code=ErrorCode.UNAUTHORIZED,
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class AuthorizationError(AppException):
    """Authorization error."""
    
    def __init__(
        self,
        message: str = "Not authorized to perform this action",
        details: Optional[List[ErrorDetail]] = None
    ):
        super().__init__(
            code=ErrorCode.FORBIDDEN,
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class DatabaseError(AppException):
    """Database error."""
    
    def __init__(
        self,
        message: str = "Database error occurred",
        details: Optional[List[ErrorDetail]] = None
    ):
        super().__init__(
            code=ErrorCode.DATABASE_ERROR,
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class ExternalServiceError(AppException):
    """External service error."""
    
    def __init__(
        self,
        message: str = "External service error",
        details: Optional[List[ErrorDetail]] = None
    ):
        super().__init__(
            code=ErrorCode.EXTERNAL_SERVICE_ERROR,
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=details
        )


class RateLimitError(AppException):
    """Rate limit exceeded error."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        details: Optional[List[ErrorDetail]] = None
    ):
        super().__init__(
            code=ErrorCode.RATE_LIMIT_EXCEEDED,
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details
        )


class BusinessLogicError(AppException):
    """Business logic error."""
    
    def __init__(
        self,
        message: str = "Business logic error",
        details: Optional[List[ErrorDetail]] = None
    ):
        super().__init__(
            code=ErrorCode.BUSINESS_LOGIC_ERROR,
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


def create_error_detail(loc: List[str], msg: str, type_: str) -> ErrorDetail:
    """Create an error detail object."""
    return ErrorDetail(loc=loc, msg=msg, type=type_)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application-specific exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            code=exc.code,
            message=exc.message,
            details=exc.details,
            request_id=request.headers.get("X-Request-ID")
        ).dict(exclude_none=True)
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation exceptions."""
    details = []
    for error in exc.errors():
        details.append(
            ErrorDetail(
                loc=[str(loc) for loc in error["loc"]],
                msg=error["msg"],
                type=error["type"]
            )
        )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            code=ErrorCode.VALIDATION_ERROR,
            message="Validation error",
            details=details,
            request_id=request.headers.get("X-Request-ID")
        ).dict(exclude_none=True)
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    error_code = ErrorCode.INTERNAL_ERROR
    
    # Map status codes to error codes
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        error_code = ErrorCode.NOT_FOUND
    elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
        error_code = ErrorCode.UNAUTHORIZED
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        error_code = ErrorCode.FORBIDDEN
    elif exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        error_code = ErrorCode.RATE_LIMIT_EXCEEDED
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            code=error_code,
            message=exc.detail,
            request_id=request.headers.get("X-Request-ID")
        ).dict(exclude_none=True)
    )


def setup_exception_handlers(app: Any) -> None:
    """Set up exception handlers for a FastAPI application."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
"""