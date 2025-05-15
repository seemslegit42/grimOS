"""
Database connection and session management for Composable Runes
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.config import settings

# Create async database engine
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

# Base class for all database models
Base = declarative_base()


async def init_db():
    """Initialize database tables and connections"""
    async with engine.begin() as conn:
        # Uncomment for development only
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """
    Dependency for getting a database session
    
    Usage:
    ```
    @app.get("/items/")
    async def get_items(db: AsyncSession = Depends(get_db)):
        items = await db.execute(select(Item))
        return items.scalars().all()
    ```
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
