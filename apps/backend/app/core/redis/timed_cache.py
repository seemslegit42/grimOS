"""
TimedCache implementation for caching with automatic refresh
"""
from typing import Any, Optional, Callable, Dict, Union
import asyncio
import time
import logging
from functools import wraps

from app.core.redis.cache import get_cache, set_cache, delete_cache
from app.core.metrics_manager import get_metrics_manager

# Configure logger
logger = logging.getLogger("grimos.timed_cache")

# Get metrics manager
metrics = get_metrics_manager()

class TimedCache:
    """
    A class for managing cached values with automatic refresh.
    
    This is useful for data that needs to be frequently accessed but is
    relatively expensive to compute or fetch from the database.
    
    The cache will automatically refresh in the background after a specified 
    refresh interval, ensuring the cached data stays relatively fresh while 
    still providing fast access.
    """
    
    def __init__(self, 
                 name: str, 
                 refresh_seconds: int = 300,
                 expire_seconds: int = 3600):
        """
        Initialize a new TimedCache.
        
        Args:
            name: A unique name for this cache instance
            refresh_seconds: How often to refresh the cache in seconds (default: 5 minutes)
            expire_seconds: When the cache should expire if refresh fails (default: 1 hour)
        """
        self.name = name
        self.refresh_seconds = refresh_seconds
        self.expire_seconds = expire_seconds
        self.is_refreshing = False
        self.last_refresh_time = 0
    
    async def get_or_set(self, 
                    key: str, 
                    refresh_func: Callable[[], Any],
                    force_refresh: bool = False) -> Any:
        """
        Get a value from cache or compute and store it if not present.
        
        Args:
            key: The cache key
            refresh_func: Function to call to compute/fetch the value
            force_refresh: Whether to force a refresh regardless of time
            
        Returns:
            The cached or computed value
        """
        cache_key = f"{self.name}:{key}"
        
        # Try to get from cache first
        cached_value = get_cache(cache_key)
        
        # If we have a cached value and don't need to refresh yet
        current_time = time.time()
        needs_refresh = (
            force_refresh or 
            cached_value is None or 
            current_time - self.last_refresh_time > self.refresh_seconds
        )
        
        if cached_value is not None and not needs_refresh:
            metrics.record_cache_access("timed_cache", True)
            return cached_value
        
        # If cache is empty or stale, but someone else is already refreshing
        if self.is_refreshing and cached_value is not None:
            metrics.record_cache_access("timed_cache", True)
            return cached_value
        
        # We need to refresh the cache
        try:
            self.is_refreshing = True
            metrics.record_cache_access("timed_cache", False)
            
            # Get new value
            new_value = await refresh_func() if asyncio.iscoroutinefunction(refresh_func) else refresh_func()
            
            # Cache the new value
            set_cache(cache_key, new_value, self.expire_seconds)
            
            # Update last refresh time
            self.last_refresh_time = current_time
            
            return new_value
        except Exception as e:
            logger.error(f"Error refreshing timed cache '{self.name}:{key}': {str(e)}")
            # If we have a cached value, return it even though it's stale
            if cached_value is not None:
                metrics.record_cache_access("timed_cache", True)
                return cached_value
            # Otherwise, raise the error
            raise
        finally:
            self.is_refreshing = False
    
    def invalidate(self, key: str) -> bool:
        """
        Invalidate a cache entry.
        
        Args:
            key: The cache key
            
        Returns:
            True if successful, False otherwise
        """
        cache_key = f"{self.name}:{key}"
        return delete_cache(cache_key)


def timed_cache_decorator(name: str,
                          refresh_seconds: int = 300,
                          expire_seconds: int = 3600,
                          key_builder: Optional[Callable] = None):
    """
    Decorator for functions that should use timed cache.
    
    Args:
        name: A unique name for this cache
        refresh_seconds: How often to refresh the cache (default: 5 minutes)
        expire_seconds: When the cache should expire (default: 1 hour)
        key_builder: Function to build cache key from function args
        
    Returns:
        Decorated function
    """
    cache = TimedCache(name, refresh_seconds, expire_seconds)
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                # Default: use function name and arguments
                cache_key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            
            # Get value from cache or compute it
            return await cache.get_or_set(
                cache_key, 
                lambda: func(*args, **kwargs)
            )
        
        # Attach the cache instance to the wrapper for direct access
        wrapper.cache = cache
        
        return wrapper
    
    return decorator
