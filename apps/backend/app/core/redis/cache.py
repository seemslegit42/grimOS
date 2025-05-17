"""
Redis implementation for caching
"""
from redis import Redis
from typing import Any, Optional, Union, Callable
import json
import time
from functools import wraps

from app.core.config import settings

# Initialize Redis client
redis_client = Redis.from_url(
    url=settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=5,
)

def get_cache(key: str) -> Optional[Any]:
    """
    Get a value from the cache.
    
    Args:
        key: The cache key
        
    Returns:
        The cached value if exists, None otherwise
    """
    from app.core.metrics_manager import get_metrics_manager
    metrics = get_metrics_manager()
    
    value = redis_client.get(key)
    if value:
        try:
            metrics.record_cache_access("redis", True)
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            metrics.record_cache_access("redis", True)
            return value
    
    metrics.record_cache_access("redis", False)
    return None

def set_cache(key: str, value: Any, expire: int = 3600) -> bool:
    """
    Set a value in the cache.
    
    Args:
        key: The cache key
        value: The value to cache
        expire: Expiration time in seconds (default: 1 hour)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        value_str = json.dumps(value) if not isinstance(value, str) else value
        return redis_client.setex(key, expire, value_str)
    except (TypeError, json.JSONDecodeError):
        return False

def delete_cache(key: str) -> bool:
    """
    Delete a value from the cache.
    
    Args:
        key: The cache key
        
    Returns:
        True if successful, False otherwise
    """
    return bool(redis_client.delete(key))

def clear_cache_pattern(pattern: str) -> int:
    """
    Clear all keys matching a pattern.
    
    Args:
        pattern: The pattern to match (e.g., "user:*")
        
    Returns:
        Number of keys deleted
    """
    keys = redis_client.keys(pattern)
    if keys:
        return redis_client.delete(*keys)
    return 0

def cache_decorator(expire: int = 3600, key_prefix: str = ""):
    """
    Decorator to cache function results.
    
    Args:
        expire: Cache expiration time in seconds
        key_prefix: Prefix for the cache key
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate a cache key based on function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache first
            cached_result = get_cache(cache_key)
            if cached_result is not None:
                return cached_result
                
            # If not cached, execute function
            result = await func(*args, **kwargs)
            
            # Cache the result
            set_cache(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator
