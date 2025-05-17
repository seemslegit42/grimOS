"""
Enhanced metrics implementation for the GrimOS API.
This module provides a unified way to define, register, and manage Prometheus metrics.
"""

import time
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request
import socket

# Import prometheus conditionally to handle environments without it
try:
    import prometheus_client as prom
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

# Configure logger
logger = logging.getLogger("grimos.metrics")

class MetricsManager:
    """
    Manager for application metrics.
    Handles registration, collection, and processing of Prometheus metrics.
    """
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {}
        self.initialized = False
        self.host = socket.gethostname()
        
    def initialize(self, app: FastAPI):
        """
        Initialize metrics for the application.
        
        Args:
            app: The FastAPI application
        """
        if not PROMETHEUS_AVAILABLE:
            logger.warning("Prometheus client not available. Metrics will be disabled.")
            return
            
        if self.initialized:
            return
            
        # Register core metrics
        self.metrics["app_info"] = prom.Gauge(
            "grimos_app_info", 
            "Application information", 
            ["version", "environment", "host"]
        )
        
        self.metrics["startup_time"] = prom.Gauge(
            "grimos_startup_timestamp_seconds",
            "Timestamp when the application started"
        )
        
        self.metrics["request_count"] = prom.Counter(
            "grimos_request_count",
            "Count of requests received",
            ["method", "endpoint", "status_code"]
        )
        
        self.metrics["request_latency"] = prom.Histogram(
            "grimos_request_latency_seconds",
            "Latency of requests in seconds",
            ["method", "endpoint"]
        )
        
        self.metrics["active_requests"] = prom.Gauge(
            "grimos_active_requests",
            "Number of active requests"
        )
        
        self.metrics["db_query_latency"] = prom.Histogram(
            "grimos_db_query_latency_seconds",
            "Database query latency in seconds",
            ["operation", "table"]
        )
        
        self.metrics["cache_hits"] = prom.Counter(
            "grimos_cache_hits",
            "Number of cache hits",
            ["cache_type"]
        )
        
        self.metrics["cache_misses"] = prom.Counter(
            "grimos_cache_misses",
            "Number of cache misses",
            ["cache_type"]
        )
        
        # Add additional metrics for the application
        self.metrics["oauth_login_count"] = prom.Counter(
            "grimos_oauth_login_count",
            "Count of OAuth logins",
            ["provider"]
        )

        self.metrics["error_count"] = prom.Counter(
            "grimos_error_count",
            "Count of errors",
            ["error_type"]
        )

        # Add RBAC metrics
        self.metrics["rbac_operation_count"] = prom.Counter(
            "grimos_rbac_operation_count",
            "Count of RBAC operations",
            ["operation_type", "user_id"]
        )
        
        # Set initial metric values
        self.set_app_info(app)
        self.set_startup_time()
        
        self.initialized = True
        logger.info("Metrics initialized")
    
    def set_app_info(self, app: FastAPI):
        """
        Set the application info metric.
        
        Args:
            app: The FastAPI application
        """
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            from app.core.config import settings
            
            self.metrics["app_info"].labels(
                getattr(app, "version", "unknown"),
                getattr(settings, "ENVIRONMENT", "unknown"),
                self.host
            ).set(1)
        except Exception as e:
            logger.error(f"Failed to set app_info metric: {str(e)}")
    
    def set_startup_time(self):
        """Set the application startup time metric."""
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            self.metrics["startup_time"].set(time.time())
        except Exception as e:
            logger.error(f"Failed to set startup_time metric: {str(e)}")
    
    def record_request_started(self, request: Request):
        """
        Record the start of a request.
        
        Args:
            request: The FastAPI request
        """
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            self.metrics["active_requests"].inc()
        except Exception as e:
            logger.error(f"Failed to record request start: {str(e)}")
    
    def record_request_completed(self, request: Request, status_code: int, duration: float):
        """
        Record the completion of a request.
        
        Args:
            request: The FastAPI request
            status_code: The HTTP status code of the response
            duration: The request duration in seconds
        """
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            method = request.method
            path = request.url.path
            
            self.metrics["request_count"].labels(method, path, status_code).inc()
            self.metrics["request_latency"].labels(method, path).observe(duration)
            self.metrics["active_requests"].dec()
        except Exception as e:
            logger.error(f"Failed to record request completion: {str(e)}")
    
    def record_db_query(self, operation: str, table: str, duration: float):
        """
        Record a database query execution.
        
        Args:
            operation: The query operation (select, insert, update, delete)
            table: The database table
            duration: The query duration in seconds
        """
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            self.metrics["db_query_latency"].labels(operation, table).observe(duration)
        except Exception as e:
            logger.error(f"Failed to record DB query: {str(e)}")
    
    def record_cache_access(self, cache_type: str, hit: bool):
        """
        Record a cache access.
        
        Args:
            cache_type: The type of cache (redis, memory, etc.)
            hit: Whether the cache request was a hit
        """
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            if hit:
                self.metrics["cache_hits"].labels(cache_type).inc()
            else:
                self.metrics["cache_misses"].labels(cache_type).inc()
        except Exception as e:
            logger.error(f"Failed to record cache access: {str(e)}")
    
    def record_oauth_login(self, provider: str):
        """
        Record an OAuth login.
        
        Args:
            provider: The OAuth provider name
        """
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            self.metrics["oauth_login_count"].labels(provider).inc()
        except Exception as e:
            logger.error(f"Failed to record OAuth login: {str(e)}")
    
    def record_error(self, error_type: str):
        """
        Record an application error.
        
        Args:
            error_type: The type of error
        """
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            self.metrics["error_count"].labels(error_type).inc()
        except Exception as e:
            logger.error(f"Failed to record error: {str(e)}")
    
    def record_rbac_operation(self, operation_type: str, user_id: str):
        """
        Record an RBAC operation.
        
        Args:
            operation_type: The type of RBAC operation
            user_id: The ID of the user
        """
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            self.metrics["rbac_operation_count"].labels(operation_type, user_id).inc()
        except Exception as e:
            logger.error(f"Failed to record RBAC operation: {str(e)}")
    
    def record_user_activity(self, activity_type: str, user_id: str):
        """
        Record a user activity.
        
        Args:
            activity_type: The type of user activity
            user_id: The ID of the user
        """
        if not PROMETHEUS_AVAILABLE or not self.initialized:
            return
            
        try:
            # Use the rbac_operation_count metric for now, as it has the right labels
            # In the future, we might want to create a dedicated user activity metric
            self.metrics["rbac_operation_count"].labels(activity_type, user_id).inc()
        except Exception as e:
            logger.error(f"Failed to record user activity: {str(e)}")

# Create a singleton instance
metrics_manager = MetricsManager()

def get_metrics_manager() -> MetricsManager:
    """
    Get the metrics manager instance.
    
    Returns:
        The metrics manager instance
    """
    return metrics_manager
