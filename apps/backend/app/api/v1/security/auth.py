"""
Auth middleware for RBAC
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from typing import List, Set

from app.core.security import verify_token
from app.db.session import get_db
from app.db.models import User, Role, Permission

# OAuth2 scheme for token extraction from request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user from the JWT token.
    
    This dependency extracts the user ID from the JWT token and fetches the user
    from the database, making it available to route handlers.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify token and extract user_id (sub)
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

def has_role(required_roles: List[str]):
    """
    Dependency factory that checks if the user has any of the required roles.
    
    Usage:
        @router.get("/admin-only")
        async def admin_only(user: User = Depends(has_role(["admin"]))):
            return {"message": "You are an admin!"}
    """
    async def _has_role(current_user: User = Depends(get_current_user)):
        # Get role names from user.roles
        user_roles: List[str] = []
        for role in current_user.roles:
            role_name = str(role.name)
            if role_name:
                user_roles.append(role_name)
        
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required role(s): {', '.join(required_roles)}"
            )
        
        return current_user
    
    return _has_role

def has_permission(required_permissions: List[str]):
    """
    Dependency factory that checks if the user has all the required permissions.
    
    Usage:
        @router.delete("/items/{item_id}")
        async def delete_item(item_id: int, user: User = Depends(has_permission(["delete"]))):
            return {"message": "Item deleted"}
    """
    async def _has_permission(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        user_permissions: Set[str] = set()
        
        for role in current_user.roles:
            role_perms = db.query(Permission.name).join(
                Role.permissions
            ).filter(
                Role.id == role.id
            ).all()
            
            for perm in role_perms:
                perm_name = str(perm[0])
                if perm_name:
                    user_permissions.add(perm_name)
        
        # Check if user has all required permissions
        if not all(perm in user_permissions for perm in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required permission(s): {', '.join(required_permissions)}"
            )
        
        return current_user
    
    return _has_permission
