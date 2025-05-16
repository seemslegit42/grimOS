"""
Health check utilities for grimOS backend services.
"""

import logging
import time
from typing import Dict, List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class HealthStatus(BaseModel):
    """Health status response model."""
    status: str
    version: str
    uptime: float
    dependencies: Dict[str, str]


class HealthCheck:
    """Health check utility for grimOS services."""
    
    def __init__(
        self, 
        service_name: str, 
        version: str,
        dependencies: Optional[Dict[str, str]] = None
    ):
        """
        Initialize the health check utility.
        
        Args:
            service_name: The name of the service
            version: The version of the service
            dependencies: Optional dictionary of dependency URLs to check
        """
        self.service_name = service_name
        self.version = version
        self.dependencies = dependencies or {}
        self.start_time = time.time()
        
        # Create router
        self.router = APIRouter(tags=["health"])
        self.router.add_api_route("/health", self.check_health, methods=["GET"])
        
    async def check_health(self) -> HealthStatus:
        """
        Check the health of the service and its dependencies.
        
        Returns:
            A HealthStatus object
        """
        dependency_status = {}
        
        # Check dependencies
        for name, url in self.dependencies.items():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{url}/health", timeout=2.0)
                    if response.status_code == 200:
                        dependency_status[name] = "healthy"
                    else:
                        dependency_status[name] = f"unhealthy ({response.status_code})"
            except Exception as e:
                logger.warning(f"Health check failed for {name}: {str(e)}")
                dependency_status[name] = f"unreachable ({str(e)})"
        
        return HealthStatus(
            status="healthy",
            version=self.version,
            uptime=time.time() - self.start_time,
            dependencies=dependency_status
        )


def create_health_router(
    service_name: str, 
    version: str,
    dependencies: Optional[Dict[str, str]] = None
) -> APIRouter:
    """
    Create a health check router for a service.
    
    Args:
        service_name: The name of the service
        version: The version of the service
        dependencies: Optional dictionary of dependency URLs to check
        
    Returns:
        An APIRouter with health check endpoints
    """
    health_check = HealthCheck(service_name, version, dependencies)
    return health_check.router