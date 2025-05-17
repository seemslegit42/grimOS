from typing import List, Set
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User, Role, Permission, RolePermission
from app.api.v1.security.auth import get_current_user
from app.core.redis.permission_cache import get_cached_user_permissions, cache_user_permissions, invalidate_user_cache

async def get_user_permissions(user: User, db: Session) -> Set[str]:
    """
    Get all permissions assigned to a user based on their roles.
    First tries to retrieve from cache, then falls back to DB lookup.
    
    Args:
        user: The user for which to retrieve permissions
        db: Database session
        
    Returns:
        Set of permission names the user has
    """
    # Try to get from cache first
    cached_permissions = await get_cached_user_permissions(user.id)
    if cached_permissions:
        return set(cached_permissions)
    
    # Cache miss, need to query the database
    permissions = set()
    
    # Collect all permissions from all roles
    for role in user.roles:
        for role_permission in role.permissions:
            # Get the permission name from the database
            permission = db.query(Permission).filter(
                Permission.id == role_permission.permission_id
            ).first()
            if permission:
                permissions.add(permission.name)
    
    # Cache the permissions for future requests
    await cache_user_permissions(user.id, list(permissions))
    
    return permissions

async def has_permission(user: User, permission_name: str, db: Session) -> bool:
    """
    Check if a user has a specific permission.
    
    Args:
        user: The user to check
        permission_name: The name of the permission to check for
        db: Database session
        
    Returns:
        True if the user has the permission, False otherwise
    """
    # Check if user is admin (automatic access to everything)
    for role in user.roles:
        if role.name == "admin":
            return True
    
    # Get all user permissions and check if the specific permission is included
    user_permissions = await get_user_permissions(user, db)
    return permission_name in user_permissions

async def has_any_permission(user: User, permission_names: List[str], db: Session) -> bool:
    """
    Check if a user has any of the specified permissions.
    
    Args:
        user: The user to check
        permission_names: List of permission names to check for
        db: Database session
        
    Returns:
        True if the user has any of the permissions, False otherwise
    """
    # Check if user is admin (automatic access to everything)
    for role in user.roles:
        if role.name == "admin":
            return True
    
    # Get all user permissions and check if any of the specified permissions are included
    user_permissions = await get_user_permissions(user, db)
    return any(permission in user_permissions for permission in permission_names)

class PermissionChecker:
    """Permission checker dependency for FastAPI endpoints."""
    
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
        
    async def __call__(self, 
                 current_user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
        if not await has_permission(current_user, self.required_permission, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized. Missing permission: {self.required_permission}"
            )
        return current_user

def require_permission(permission_name: str):
    """
    Dependency factory for requiring a specific permission.
    
    Usage:
        @router.get("/endpoint")
        async def protected_endpoint(user = Depends(require_permission("view_data"))):
            # Only users with "view_data" permission can access this endpoint
            return {"message": "You have access!"}
    """
    return PermissionChecker(permission_name)
