"""
Database connection and session management for Interoperability Engine
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import logging
from typing import AsyncGenerator

from app.core.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Create SQL async database engine
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,
    future=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for all SQL database models
Base = declarative_base()

# MongoDB client
mongo_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
mongo_db = mongo_client[settings.MONGO_DB_NAME]


async def init_db():
    """Initialize database tables and connections"""
    logger.info("Initializing SQL database...")
    async with engine.begin() as conn:
        # Uncomment for development only
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("SQL database initialized successfully!")
    
    # Initialize MongoDB indexes if needed
    logger.info("Initializing MongoDB collections and indexes...")
    try:
        # Create indexes for connector_configs collection
        await mongo_db.connector_configs.create_index("connector_id", unique=True)
        await mongo_db.connector_configs.create_index("created_at")
        
        # Create indexes for connector_logs collection
        await mongo_db.connector_logs.create_index([("connector_id", 1), ("timestamp", -1)])
        await mongo_db.connector_logs.create_index("timestamp")
        
        logger.info("MongoDB initialized successfully!")
    except Exception as e:
        logger.error(f"Error initializing MongoDB: {e}")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting a SQL database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_mongo_db() -> AsyncIOMotorDatabase:
    """
    Dependency for getting the MongoDB database
    """
    return mongo_db


async def close_db_connections():
    """Close all database connections"""
    # Close SQL connection
    await engine.dispose()
    
    # Close MongoDB connection
    if mongo_client:
        mongo_client.close()
        
    logger.info("Database connections closed")
