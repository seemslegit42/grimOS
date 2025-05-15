"""
MongoDB database connector for Interoperability Engine
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import logging

from app.core.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# MongoDB client instance
mongo_client: Optional[AsyncIOMotorClient] = None
mongo_db: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo() -> AsyncIOMotorDatabase:
    """
    Connect to MongoDB and return the database connection
    """
    global mongo_client, mongo_db
    
    try:
        # Create MongoDB client
        logger.info("Connecting to MongoDB...")
        mongo_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
        
        # Get the database
        mongo_db = mongo_client[settings.MONGO_DB_NAME]
        
        # Ping to check connection
        await mongo_db.command('ping')
        logger.info("Connected to MongoDB successfully!")
        
        # Create indexes if needed
        await create_indexes()
        
        return mongo_db
    
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def create_indexes():
    """
    Create necessary indexes for MongoDB collections
    """
    if mongo_db is None:
        return
    
    try:
        # Create indexes for connector_configs collection
        await mongo_db.connector_configs.create_index("connector_id", unique=True)
        await mongo_db.connector_configs.create_index("created_at")
        
        # Create indexes for connector_logs collection
        if "connector_logs" in await mongo_db.list_collection_names():
            await mongo_db.connector_logs.create_index([("connector_id", 1), ("timestamp", -1)])
            await mongo_db.connector_logs.create_index("timestamp")
            
        # Create indexes for integration_data collection
        if "integration_data" in await mongo_db.list_collection_names():
            await mongo_db.integration_data.create_index([("connector_id", 1), ("entity_type", 1)])
            await mongo_db.integration_data.create_index("last_updated")
        
        logger.info("MongoDB indexes created successfully")
    
    except Exception as e:
        logger.error(f"Error creating MongoDB indexes: {e}")


async def disconnect_from_mongo():
    """
    Close MongoDB connection
    """
    global mongo_client
    if mongo_client:
        logger.info("Closing MongoDB connection...")
        mongo_client.close()
        logger.info("MongoDB connection closed")


async def get_mongo_db() -> AsyncIOMotorDatabase:
    """
    Get MongoDB database connection
    For dependency injection
    """
    if mongo_db is None:
        await connect_to_mongo()
    return mongo_db
