"""
Prometheus metrics collection for grimOS
"""
from typing import Callable
from fastapi import FastAPI, Request, Response
import time
from functools import wraps

# Import these conditionally to handle environments where they might not be available
try:
    import prometheus_client as prom
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False


# Define metrics if Prometheus is available
if PROMETHEUS_AVAILABLE:
    REQUEST_COUNT = prom.Counter(
        "grimos_request_count",
        "Count of requests received",
        ["method", "endpoint", "status_code"]
    )

    REQUEST_LATENCY = prom.Histogram(
        "grimos_request_latency_seconds",
        "Latency of requests in seconds",
        ["method", "endpoint"]
    )

    ACTIVE_REQUESTS = prom.Gauge(
        "grimos_active_requests",
        "Number of active requests"
    )

    DB_QUERY_LATENCY = prom.Histogram(
        "grimos_db_query_latency_seconds",
        "Database query latency in seconds",
        ["operation", "table"]
    )

    CACHE_HITS = prom.Counter(
        "grimos_cache_hits",
        "Number of cache hits",
        ["cache_type"]
    )

    CACHE_MISSES = prom.Counter(
        "grimos_cache_misses",
        "Number of cache misses",
        ["cache_type"]
    )
else:
    # Define dummy metrics for environments without Prometheus
    class DummyMetric:
        def __init__(self, *args, **kwargs):
            pass
            
        def labels(self, *args, **kwargs):
            return self
            
        def inc(self, *args, **kwargs):
            pass
            
        def dec(self, *args, **kwargs):
            pass
            
        def observe(self, *args, **kwargs):
            pass
            
        def set(self, *args, **kwargs):
            pass
    
    REQUEST_COUNT = DummyMetric()
    REQUEST_LATENCY = DummyMetric()
    ACTIVE_REQUESTS = DummyMetric()
    DB_QUERY_LATENCY = DummyMetric()
    CACHE_HITS = DummyMetric()
    CACHE_MISSES = DummyMetric()


def setup_metrics(app: FastAPI) -> None:
    """
    Set up metrics for the FastAPI application.
    
    Args:
        app: The FastAPI application
    """
    if not PROMETHEUS_AVAILABLE:
        return
    
    # Add Prometheus metrics endpoint
    @app.get("/metrics")
    async def metrics():
        return Response(
            content=prom.generate_latest(),
            media_type="text/plain"
        )
    
    # Add middleware to track request metrics
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        ACTIVE_REQUESTS.inc()
        request_start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Record request metrics
            request_time = time.time() - request_start_time
            REQUEST_COUNT.labels(
                request.method, 
                request.url.path, 
                response.status_code
            ).inc()
            REQUEST_LATENCY.labels(
                request.method, 
                request.url.path
            ).observe(request_time)
            
            return response
        finally:
            ACTIVE_REQUESTS.dec()


def track_db_query(operation: str, table: str):
    """
    Decorator to track database query latency.
    
    Args:
        operation: The query operation (select, insert, update, delete)
        table: The database table being queried
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                query_time = time.time() - start_time
                DB_QUERY_LATENCY.labels(operation, table).observe(query_time)
        return wrapper
    return decorator


def track_cache(cache_type: str):
    """
    Track cache hits and misses.
    
    Args:
        cache_type: The type of cache (redis, memory, etc.)
        hit: Whether the cache request was a hit
    """
    def record_hit():
        CACHE_HITS.labels(cache_type).inc()
        
    def record_miss():
        CACHE_MISSES.labels(cache_type).inc()
        
    return record_hit, record_miss
