"""
Redis initialization and connection management
"""
from redis import Redis
from contextlib import contextmanager
from typing import Generator

from app.core.config import settings

def create_redis_pool() -> Redis:
    """
    Create a Redis connection pool.
    
    Returns:
        Redis client instance
    """
    return Redis.from_url(
        url=settings.REDIS_URL,
        decode_responses=True,
        socket_timeout=5,
        socket_connect_timeout=5,
        socket_keepalive=True,
    )

@contextmanager
def get_redis_connection() -> Generator[Redis, None, None]:
    """
    Get a Redis connection from the pool.
    
    Yields:
        Redis client instance
    """
    client = create_redis_pool()
    try:
        yield client
    finally:
        client.close()

# Create a global Redis client for convenience
redis_client = create_redis_pool()
