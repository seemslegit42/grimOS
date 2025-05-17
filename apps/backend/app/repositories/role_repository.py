"""
Role repository implementation.
"""
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
import logging

from app.db.models import Role, Permission, RolePermission
from app.repositories.base_repository import BaseRepository
from app.core.metrics_manager import get_metrics_manager
from app.core.redis.timed_cache import TimedCache

# Configure logger
logger = logging.getLogger("grimos.role_repository")

# Get metrics manager
metrics = get_metrics_manager()

class RoleRepository(BaseRepository[Role]):
    """
    Repository for Role model operations.
    """
    
    def __init__(self, db: Session, use_cache: bool = True):
        """
        Initialize the role repository.
        
        Args:
            db: The database session
            use_cache: Whether to use caching
        """
        super().__init__(Role, db, use_cache, "role")
        self.permissions_cache = TimedCache("role_permissions", 300, 3600)
    
    def get_by_name(self, name: str) -> Optional[Role]:
        """
        Get a role by name.
        
        Args:
            name: The role name
            
        Returns:
            The role if found, None otherwise
        """
        try:
            start_time = metrics.start_timer()
            role = self.db.query(Role).filter(Role.name == name).first()
            metrics.record_db_query("select", "roles", metrics.end_timer(start_time))
            return role
        except Exception as e:
            logger.error(f"Error getting role by name: {str(e)}")
            metrics.record_error("database_error")
            return None
    
    async def get_role_permissions(self, role_id: int) -> List[Permission]:
        """
        Get permissions for a role.
        
        Args:
            role_id: The role ID
            
        Returns:
            List of permissions
        """
        try:
            async def fetch_permissions():
                role = self.get_by_id(role_id)
                if not role:
                    return []
                    
                permissions = []
                for role_permission in role.permissions:
                    permission = self.db.query(Permission).filter(
                        Permission.id == role_permission.permission_id
                    ).first()
                    if permission:
                        permissions.append(permission)
                        
                return permissions
            
            # Use timed cache to avoid frequent database queries
            return await self.permissions_cache.get_or_set(
                f"role:{role_id}:permissions", 
                fetch_permissions
            )
        except Exception as e:
            logger.error(f"Error getting permissions for role {role_id}: {str(e)}")
            metrics.record_error("database_error")
            return []
    
    def assign_permission(self, role_id: int, permission_name: str) -> bool:
        """
        Assign a permission to a role.
        
        Args:
            role_id: The role ID
            permission_name: The permission name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the role
            role = self.get_by_id(role_id)
            if not role:
                return False
            
            # Get or create the permission
            permission = self.db.query(Permission).filter(
                Permission.name == permission_name
            ).first()
            
            if not permission:
                permission = Permission(name=permission_name)
                self.db.add(permission)
                self.db.flush()
            
            # Check if the role already has this permission
            existing = self.db.query(RolePermission).filter(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission.id
            ).first()
            
            if existing:
                # Already assigned
                return True
            
            # Create role-permission association
            role_permission = RolePermission(
                role_id=role_id,
                permission_id=permission.id
            )
            self.db.add(role_permission)
            self.db.commit()
            
            # Invalidate cache
            self.permissions_cache.invalidate(f"role:{role_id}:permissions")
            
            # Track metric
            metrics.record_rbac_operation("assign_permission", str(role_id))
            
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error assigning permission {permission_name} to role {role_id}: {str(e)}")
            metrics.record_error("database_error")
            return False
    
    def remove_permission(self, role_id: int, permission_name: str) -> bool:
        """
        Remove a permission from a role.
        
        Args:
            role_id: The role ID
            permission_name: The permission name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the permission
            permission = self.db.query(Permission).filter(
                Permission.name == permission_name
            ).first()
            
            if not permission:
                # Permission doesn't exist, so it's not assigned
                return True
            
            # Delete the role-permission association
            deleted = self.db.query(RolePermission).filter(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission.id
            ).delete()
            
            self.db.commit()
            
            # Invalidate cache
            self.permissions_cache.invalidate(f"role:{role_id}:permissions")
            
            # Track metric
            if deleted:
                metrics.record_rbac_operation("remove_permission", str(role_id))
            
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error removing permission {permission_name} from role {role_id}: {str(e)}")
            metrics.record_error("database_error")
            return False
