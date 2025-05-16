"""
Testing utilities for grimOS backend services.

This module provides shared testing utilities to standardize testing across
backend microservices.
"""

import asyncio
import contextlib
import os
import random
import string
from typing import Any, AsyncGenerator, Callable, Dict, Generator, List, Optional, Type, TypeVar, Union

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

T = TypeVar('T')

def get_random_string(length: int = 10) -> str:
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def get_test_db_url() -> str:
    """Get the database URL for testing."""
    # Default to SQLite in-memory database
    return os.environ.get("TEST_DATABASE_URL", "sqlite:///./test.db")

def get_async_test_db_url() -> str:
    """Get the async database URL for testing."""
    # Default to SQLite in-memory database
    return os.environ.get("TEST_ASYNC_DATABASE_URL", "sqlite+aiosqlite:///./test.db")

@pytest.fixture
def test_db_session() -> Generator[Session, None, None]:
    """Create a new database session for a test."""
    engine = create_engine(get_test_db_url(), connect_args={"check_same_thread": False})
    
    # Create the tables
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop the tables
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
async def async_test_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a new async database session for a test."""
    engine = create_async_engine(get_async_test_db_url())
    
    # Create the tables
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create a new session
    TestingSessionLocal = sessionmaker(
        class_=AsyncSession, autocommit=False, autoflush=False, bind=engine
    )
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            # Drop the tables
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def test_app(app: FastAPI) -> Generator[TestClient, None, None]:
    """Create a FastAPI TestClient."""
    with TestClient(app) as client:
        yield client

@contextlib.contextmanager
def mock_env_vars(env_vars: Dict[str, str]) -> Generator[None, None, None]:
    """Temporarily set environment variables for testing."""
    original_env = os.environ.copy()
    os.environ.update(env_vars)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original_env)

def create_test_model(model_class: Type[T], **kwargs: Any) -> T:
    """Create a test model instance with random data for required fields."""
    model_fields = model_class.__annotations__ if hasattr(model_class, '__annotations__') else {}
    
    # Generate random data for required fields
    data = {}
    for field_name, field_type in model_fields.items():
        if field_name not in kwargs:
            # Generate random data based on field type
            if field_type == str:
                data[field_name] = get_random_string()
            elif field_type == int:
                data[field_name] = random.randint(1, 1000)
            elif field_type == bool:
                data[field_name] = random.choice([True, False])
            elif field_type == float:
                data[field_name] = random.uniform(1.0, 100.0)
            # Add more type handling as needed
    
    # Override with provided kwargs
    data.update(kwargs)
    
    return model_class(**data)

class MockResponse:
    """Mock HTTP response for testing external API calls."""
    
    def __init__(
        self, 
        status_code: int = 200, 
        json_data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        text: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text or ""
        self.headers = headers or {}
        
    def json(self) -> Union[Dict[str, Any], List[Any]]:
        """Return JSON data."""
        return self._json_data
        
    async def __aenter__(self):
        """Async context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        pass

def async_return(result: Any) -> Any:
    """Convert a synchronous result to an asynchronous one."""
    f = asyncio.Future()
    f.set_result(result)
    return f

def patch_async_method(monkeypatch, obj, method_name: str, return_value: Any) -> None:
    """Patch an async method for testing."""
    async def mock_method(*args, **kwargs):
        return return_value
    
    monkeypatch.setattr(obj, method_name, mock_method)
"""