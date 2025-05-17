from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Role, User, Permission, RolePermission

router = APIRouter(
    prefix="/rbac",
    tags=["rbac"],
)

class RolePermissionRequest(BaseModel):
    role: str
    permissions: List[str]

class UserRoleRequest(BaseModel):
    user_id: int
    role: str

class RoleResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

class PermissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles(db: Session = Depends(get_db)):
    """Fetch all roles."""
    return db.query(Role).all()

@router.post("/roles", status_code=status.HTTP_201_CREATED, response_model=RoleResponse)
async def create_role(role_request: RolePermissionRequest, db: Session = Depends(get_db)):
    """Create a new role with permissions."""
    # Check if role already exists
    existing_role = db.query(Role).filter(Role.name == role_request.role).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists."
        )
    
    # Create new role
    new_role = Role(name=role_request.role)
    db.add(new_role)
    db.flush()
    
    # Add permissions to role
    for perm_name in role_request.permissions:
        # Get or create permission
        permission = db.query(Permission).filter(Permission.name == perm_name).first()
        if not permission:
            permission = Permission(name=perm_name)
            db.add(permission)
            db.flush()
        
        # Create role-permission association
        role_perm = RolePermission(role_id=new_role.id, permission_id=permission.id)
        db.add(role_perm)
    
    db.commit()
    db.refresh(new_role)
    return new_role

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role_request: RolePermissionRequest, db: Session = Depends(get_db)):
    """Update permissions for an existing role."""
    # Find role by ID
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found."
        )
    
    # Update role name if provided
    if str(role.name) != role_request.role:
        role.name = role_request.role
    
    # Clear existing permissions
    db.query(RolePermission).filter(RolePermission.role_id == role.id).delete()
    
    # Add new permissions
    for perm_name in role_request.permissions:
        # Get or create permission
        permission = db.query(Permission).filter(Permission.name == perm_name).first()
        if not permission:
            permission = Permission(name=perm_name)
            db.add(permission)
            db.flush()
        
        # Create role-permission association
        role_perm = RolePermission(role_id=role.id, permission_id=permission.id)
        db.add(role_perm)
    
    db.commit()
    db.refresh(role)
    return role

@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Delete a role."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found."
        )
    
    # Delete associated role permissions
    db.query(RolePermission).filter(RolePermission.role_id == role.id).delete()
    
    # Delete role
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully."}

@router.post("/users/{user_id}/roles", status_code=status.HTTP_201_CREATED)
async def assign_role_to_user(user_role: UserRoleRequest, db: Session = Depends(get_db)):
    """Assign a role to a user."""
    # Check if user exists
    user = db.query(User).filter(User.id == user_role.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    # Check if role exists
    role = db.query(Role).filter(Role.name == user_role.role).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found."
        )
    
    # Check if user already has this role
    if role in user.roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has this role."
        )
    
    # Assign role to user
    user.roles.append(role)
    db.commit()
    
    return {"message": f"Role '{role.name}' assigned to user with ID {user.id}"}

@router.delete("/users/{user_id}/roles/{role_name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_user(user_id: int, role_name: str, db: Session = Depends(get_db)):
    """Remove a role from a user."""
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    # Check if role exists
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found."
        )
    
    # Check if user has this role
    if role not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have this role."
        )
    
    # Remove role from user
    user.roles.remove(role)
    db.commit()
    
    return {"message": f"Role '{role.name}' removed from user with ID {user.id}"}

@router.get("/users/{user_id}/roles", response_model=List[RoleResponse])
async def get_user_roles(user_id: int, db: Session = Depends(get_db)):
    """Get all roles assigned to a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    return user.roles
