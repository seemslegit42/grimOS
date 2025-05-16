# grimOS Shared Python Package

This package contains shared utilities and functions for grimOS backend services. It provides standardized tools for configuration, error handling, testing, and more.

## Installation

```bash
pip install -e ./packages/shared-python
```

## Features

### Configuration Management

The package provides a standardized way to manage configuration across microservices:

```python
from grimos_shared import get_settings, Settings

# Get application settings
settings = get_settings()

# Access configuration values
database_url = settings.database_url
debug_mode = settings.debug
```

### Error Handling

The package provides standardized error handling for FastAPI applications:

```python
from fastapi import FastAPI
from grimos_shared import (
    AppException, 
    ErrorCode, 
    NotFoundError, 
    ValidationError,
    setup_exception_handlers
)

app = FastAPI()

# Set up exception handlers
setup_exception_handlers(app)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id < 0:
        raise ValidationError("Item ID must be positive")
    
    if item_id not in items_db:
        raise NotFoundError(f"Item with ID {item_id} not found")
    
    return {"item": items_db[item_id]}
```

### Testing Utilities

The package provides testing utilities to standardize testing across microservices:

```python
import pytest
from grimos_shared.testing import (
    test_db_session,
    async_test_db_session,
    mock_env_vars,
    MockResponse
)

# Use a test database session
def test_create_user(test_db_session):
    # Test implementation using test_db_session
    
# Mock environment variables
def test_with_env_vars():
    with mock_env_vars({"API_KEY": "test_key", "DEBUG": "true"}):
        # Test implementation with mocked environment variables

# Mock HTTP responses
def test_external_api(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(
            status_code=200,
            json_data={"id": 1, "name": "Test User"}
        )
    
    monkeypatch.setattr("requests.get", mock_get)
    # Test implementation with mocked HTTP response
```

### Health Checks

The package provides a standardized way to implement health checks:

```python
from fastapi import FastAPI
from grimos_shared import HealthCheck, HealthStatus

app = FastAPI()

# Create a health check
health_check = HealthCheck()

# Add health check components
@health_check.add_check
async def database_check():
    # Check database connection
    try:
        # Database check implementation
        return True, "Database connection is healthy"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

@app.get("/health")
async def health():
    result = await health_check.run_checks()
    status_code = 200 if result.status == HealthStatus.HEALTHY else 503
    return result
```

### Logging

The package provides a standardized way to set up logging:

```python
from grimos_shared import setup_logging, get_logger

# Set up logging
setup_logging()

# Get a logger
logger = get_logger(__name__)

# Use the logger
logger.info("Application started")
logger.error("An error occurred", exc_info=True)
```

## Available Modules

- `grimos_shared.config`: Configuration management utilities
- `grimos_shared.utils`: General utility functions
- `grimos_shared.health`: Health check utilities
- `grimos_shared.errors`: Standardized error handling
- `grimos_shared.testing`: Testing utilities

## Contributing

When adding new utilities to this package, please follow these guidelines:

1. Use snake_case for function and variable names
2. Add proper docstrings to document the utility
3. Export the utility from the appropriate __init__.py file
4. Update this README.md with documentation for the new utility
5. Add tests for the new utility

## License

MIT