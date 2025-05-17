"""
Repository factory and initialization.
"""
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository

def get_user_repository(db: Session) -> UserRepository:
    """
    Get a UserRepository instance.
    
    Args:
        db: The database session
    
    Returns:
        UserRepository instance
    """
    return UserRepository(db)

def get_role_repository(db: Session) -> RoleRepository:
    """
    Get a RoleRepository instance.
    
    Args:
        db: The database session
    
    Returns:
        RoleRepository instance
    """
    return RoleRepository(db)
