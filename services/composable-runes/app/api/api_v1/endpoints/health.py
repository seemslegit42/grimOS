"""
Health check endpoints for the Composable Runes service
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from app.core.database import get_db

router = APIRouter()


@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Service health check"""
    # Check database connection
    db_healthy = False
    try:
        # Try to execute a simple query
        await db.execute(select(text("1")))
        db_healthy = True
    except Exception as e:
        db_healthy = False
    
    # Add more health checks as needed (Redis, Kafka, etc.)
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "service": "composable-runes"
    }
