"""
User repository implementation.
"""
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
import logging

from app.db.models import User, Role
from app.repositories.base_repository import BaseRepository
from app.core.metrics_manager import get_metrics_manager
from app.core.redis.timed_cache import TimedCache

# Configure logger
logger = logging.getLogger("grimos.user_repository")

# Get metrics manager
metrics = get_metrics_manager()

class UserRepository(BaseRepository[User]):
    """
    Repository for User model operations.
    """
    
    def __init__(self, db: Session, use_cache: bool = True):
        """
        Initialize the user repository.
        
        Args:
            db: The database session
            use_cache: Whether to use caching
        """
        super().__init__(User, db, use_cache, "user")
        self.role_cache = TimedCache("role", 300, 3600)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: The user's email
            
        Returns:
            The user if found, None otherwise
        """
        try:
            start_time = metrics.start_timer()
            user = self.db.query(User).filter(User.email == email).first()
            metrics.record_db_query("select", "users", metrics.end_timer(start_time))
            return user
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            metrics.record_error("database_error")
            return None
    
    def get_user_roles(self, user_id: int) -> List[Role]:
        """
        Get roles for a user.
        
        Args:
            user_id: The user ID
            
        Returns:
            List of roles
        """
        try:
            user = self.get_by_id(user_id)
            if not user:
                return []
            return user.roles
        except Exception as e:
            logger.error(f"Error getting roles for user {user_id}: {str(e)}")
            metrics.record_error("database_error")
            return []
    
    def get_users_with_role(self, role_name: str) -> List[User]:
        """
        Get all users with a specific role.
        
        Args:
            role_name: The role name
            
        Returns:
            List of users with the role
        """
        try:
            async def get_users():
                role = self.db.query(Role).filter(Role.name == role_name).first()
                if not role:
                    return []
                
                users = self.db.query(User).filter(User.roles.contains(role)).all()
                return users
            
            # Use the timed cache to avoid frequent database queries
            return await self.role_cache.get_or_set(f"users_with_role:{role_name}", get_users)
        except Exception as e:
            logger.error(f"Error getting users with role {role_name}: {str(e)}")
            metrics.record_error("database_error")
            return []
    
    def assign_role(self, user_id: int, role_name: str) -> bool:
        """
        Assign a role to a user.
        
        Args:
            user_id: The user ID
            role_name: The role name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = self.get_by_id(user_id)
            if not user:
                return False
                
            role = self.db.query(Role).filter(Role.name == role_name).first()
            if not role:
                return False
                
            if role in user.roles:
                # Role already assigned
                return True
                
            user.roles.append(role)
            self.db.commit()
            
            # Invalidate role cache
            self.role_cache.invalidate(f"users_with_role:{role_name}")
            
            # Track metric
            metrics.record_rbac_operation("assign_role", str(user_id))
            
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error assigning role {role_name} to user {user_id}: {str(e)}")
            metrics.record_error("database_error")
            return False
    
    def remove_role(self, user_id: int, role_name: str) -> bool:
        """
        Remove a role from a user.
        
        Args:
            user_id: The user ID
            role_name: The role name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = self.get_by_id(user_id)
            if not user:
                return False
                
            role = self.db.query(Role).filter(Role.name == role_name).first()
            if not role:
                return False
                
            if role not in user.roles:
                # Role not assigned
                return True
                
            user.roles.remove(role)
            self.db.commit()
            
            # Invalidate role cache
            self.role_cache.invalidate(f"users_with_role:{role_name}")
            
            # Track metric
            metrics.record_rbac_operation("remove_role", str(user_id))
            
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error removing role {role_name} from user {user_id}: {str(e)}")
            metrics.record_error("database_error")
            return False
