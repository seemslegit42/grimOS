"""
grimOS Shared Python Package

This package contains shared utilities and functions for grimOS backend services.
It provides standardized tools for configuration, error handling, testing, and more.
"""

__version__ = "0.1.0"

# Import main modules for easier access
from . import config
from . import utils
from . import health
from . import errors
from . import testing

# Export commonly used functions and classes for direct import
from .config import get_settings, Settings
from .utils import setup_logging, get_logger
from .health import HealthCheck, HealthStatus
from .errors import (
    AppException,
    ErrorCode,
    ErrorResponse,
    NotFoundError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    DatabaseError,
    setup_exception_handlers
)
from .testing import (
    get_test_db_url,
    get_async_test_db_url,
    mock_env_vars,
    MockResponse
)