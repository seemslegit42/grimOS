"""
Health check endpoints for the Interoperability Engine
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db, get_mongo_db

router = APIRouter()


@router.get("/")
async def health_check(
    db: AsyncSession = Depends(get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Health check for Interoperability Engine"""
    # Check SQL database connection
    sql_healthy = False
    try:
        # Try to execute a simple query
        await db.execute(select(text("1")))
        sql_healthy = True
    except Exception as e:
        sql_healthy = False
    
    # Check MongoDB connection
    mongo_healthy = False
    try:
        # Try to ping MongoDB
        await mongo_db.command("ping")
        mongo_healthy = True
    except Exception as e:
        mongo_healthy = False
    
    return {
        "status": "healthy" if (sql_healthy and mongo_healthy) else "unhealthy",
        "services": {
            "sql_database": "connected" if sql_healthy else "disconnected",
            "mongodb": "connected" if mongo_healthy else "disconnected"
        },
        "service": "interoperability"
    }
