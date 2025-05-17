"""
Permission caching for RBAC
"""
from app.core.redis.cache import get_cache, set_cache, delete_cache, clear_cache_pattern

# Cache key patterns
USER_ROLES_KEY = "user:{user_id}:roles"
USER_PERMISSIONS_KEY = "user:{user_id}:permissions"
ROLE_PERMISSIONS_KEY = "role:{role_id}:permissions"

# Cache expiration times (in seconds)
USER_CACHE_EXPIRE = 3600  # 1 hour
ROLE_CACHE_EXPIRE = 86400  # 24 hours

async def cache_user_roles(user_id: int, roles: list) -> bool:
    """
    Cache user roles.
    
    Args:
        user_id: The user ID
        roles: List of role objects or role names
        
    Returns:
        True if successful, False otherwise
    """
    # If roles are objects with a 'name' attribute, extract names
    role_names = [role.name if hasattr(role, 'name') else role for role in roles]
    return set_cache(
        USER_ROLES_KEY.format(user_id=user_id),
        role_names,
        USER_CACHE_EXPIRE
    )

async def get_cached_user_roles(user_id: int) -> list:
    """
    Get cached user roles.
    
    Args:
        user_id: The user ID
        
    Returns:
        List of role names or empty list if not cached
    """
    roles = get_cache(USER_ROLES_KEY.format(user_id=user_id))
    return roles if roles else []

async def cache_user_permissions(user_id: int, permissions: list) -> bool:
    """
    Cache user permissions.
    
    Args:
        user_id: The user ID
        permissions: List of permission strings
        
    Returns:
        True if successful, False otherwise
    """
    return set_cache(
        USER_PERMISSIONS_KEY.format(user_id=user_id),
        permissions,
        USER_CACHE_EXPIRE
    )

async def get_cached_user_permissions(user_id: int) -> list:
    """
    Get cached user permissions.
    
    Args:
        user_id: The user ID
        
    Returns:
        List of permission strings or empty list if not cached
    """
    permissions = get_cache(USER_PERMISSIONS_KEY.format(user_id=user_id))
    return permissions if permissions else []

async def cache_role_permissions(role_id: int, permissions: list) -> bool:
    """
    Cache role permissions.
    
    Args:
        role_id: The role ID
        permissions: List of permission strings
        
    Returns:
        True if successful, False otherwise
    """
    return set_cache(
        ROLE_PERMISSIONS_KEY.format(role_id=role_id),
        permissions,
        ROLE_CACHE_EXPIRE
    )

async def get_cached_role_permissions(role_id: int) -> list:
    """
    Get cached role permissions.
    
    Args:
        role_id: The role ID
        
    Returns:
        List of permission strings or empty list if not cached
    """
    permissions = get_cache(ROLE_PERMISSIONS_KEY.format(role_id=role_id))
    return permissions if permissions else []

async def invalidate_user_cache(user_id: int) -> int:
    """
    Invalidate all cache for a user.
    
    Args:
        user_id: The user ID
        
    Returns:
        Number of keys deleted
    """
    return clear_cache_pattern(f"user:{user_id}:*")

async def invalidate_role_cache(role_id: int) -> int:
    """
    Invalidate role cache and all users with that role.
    
    Args:
        role_id: The role ID
        
    Returns:
        Number of keys deleted
    """
    # First clear the role permissions
    delete_cache(ROLE_PERMISSIONS_KEY.format(role_id=role_id))
    
    # Then clear all user permissions (since they might have this role)
    # This is a broad invalidation that will force recalculation of permissions
    return clear_cache_pattern("user:*:permissions")
