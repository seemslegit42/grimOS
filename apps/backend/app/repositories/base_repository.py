"""
Base Repository pattern implementation.
This provides a structured way to access data with optional caching.
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.db.models import Base
from app.core.redis.cache import get_cache, set_cache, delete_cache

# Create a TypeVar for SQLAlchemy model
T = TypeVar('T', bound=Base)

# Create logger
logger = logging.getLogger("grimos.repository")

class BaseRepository(Generic[T]):
    """
    Base repository for data access operations with caching support.
    """
    
    def __init__(self, model: Type[T], db: Session, use_cache: bool = True, cache_prefix: str = None):
        """
        Initialize the repository.
        
        Args:
            model: The SQLAlchemy model class
            db: Database session
            use_cache: Whether to use caching (default: True)
            cache_prefix: Prefix for cache keys (default: model.__tablename__)
        """
        self.model = model
        self.db = db
        self.use_cache = use_cache
        self.cache_prefix = cache_prefix or model.__tablename__
    
    def get_by_id(self, id: Any) -> Optional[T]:
        """
        Get a record by ID, with caching.
        
        Args:
            id: The record ID
            
        Returns:
            The record if found, None otherwise
        """
        # Check cache first if caching is enabled
        if self.use_cache:
            cache_key = f"{self.cache_prefix}:{id}"
            cached_record = get_cache(cache_key)
            if cached_record:
                # Note: This returns a dict, not a model instance
                # This is a limitation of the current caching system
                return cached_record
        
        # Query the database
        record = self.db.query(self.model).filter(self.model.id == id).first()
        
        # Cache the result if found and caching is enabled
        if record and self.use_cache:
            cache_key = f"{self.cache_prefix}:{id}"
            set_cache(cache_key, record.__dict__, 3600)
        
        return record
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of records
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def get_filtered(self, filter_dict: Dict[str, Any]) -> List[T]:
        """
        Get records filtered by attribute values.
        
        Args:
            filter_dict: Dictionary of attribute-value pairs to filter by
            
        Returns:
            List of matching records
        """
        query = self.db.query(self.model)
        for attr, value in filter_dict.items():
            query = query.filter(getattr(self.model, attr) == value)
        return query.all()
    
    def create(self, data: Dict[str, Any]) -> T:
        """
        Create a new record.
        
        Args:
            data: Dictionary of attribute-value pairs
            
        Returns:
            The created record
        """
        try:
            record = self.model(**data)
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            
            # Invalidate any relevant caches
            if self.use_cache:
                self._invalidate_collection_caches()
                
            return record
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise
    
    def update(self, id: Any, data: Dict[str, Any]) -> Optional[T]:
        """
        Update a record by ID.
        
        Args:
            id: The record ID
            data: Dictionary of attribute-value pairs to update
            
        Returns:
            The updated record if found, None otherwise
        """
        try:
            record = self.db.query(self.model).filter(self.model.id == id).first()
            if not record:
                return None
                
            # Update attributes
            for key, value in data.items():
                setattr(record, key, value)
                
            self.db.commit()
            self.db.refresh(record)
            
            # Invalidate caches
            if self.use_cache:
                cache_key = f"{self.cache_prefix}:{id}"
                delete_cache(cache_key)
                self._invalidate_collection_caches()
                
            return record
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error updating {self.model.__name__} with ID {id}: {str(e)}")
            raise
    
    def delete(self, id: Any) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: The record ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            record = self.db.query(self.model).filter(self.model.id == id).first()
            if not record:
                return False
                
            self.db.delete(record)
            self.db.commit()
            
            # Invalidate caches
            if self.use_cache:
                cache_key = f"{self.cache_prefix}:{id}"
                delete_cache(cache_key)
                self._invalidate_collection_caches()
                
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error deleting {self.model.__name__} with ID {id}: {str(e)}")
            raise
    
    def _invalidate_collection_caches(self):
        """Invalidate any collection caches for this model."""
        # Typically, you would clear caches for collection queries
        # This is a simplified implementation
        delete_cache(f"{self.cache_prefix}:all")
        delete_cache(f"{self.cache_prefix}:count")
