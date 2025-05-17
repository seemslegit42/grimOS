from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models import User, Role, Permission, RolePermission
from app.api.v1.auth.rbac_schemas import (
    RoleCreate, RoleResponse, RoleUpdate,
    PermissionCreate, PermissionResponse,
    RolePermissionRequest, UserRoleRequest,
    UserWithRolesResponse
)
from app.api.v1.security.auth import get_current_user
from app.core.metrics_manager import get_metrics_manager
from app.api.v1.security.rbac import has_permission

# Get the metrics manager
metrics = get_metrics_manager()

router = APIRouter(tags=["rbac"])

# Role Management
@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role: RoleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new role (admin only)."""
    # Check if user has permission to create roles
    if not has_permission(current_user, "create_role"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create roles"
        )

    # Check if role with same name already exists
    existing_role = db.query(Role).filter(Role.name == role.name).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with name {role.name} already exists"
        )

    # Create new role
    new_role = Role(
        name=role.name,
        description=role.description
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    # Record metric for role creation
    metrics.record_rbac_operation("create_role", current_user.id)
    
    return new_role

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all roles (admin only)."""
    # Check if user has permission to view roles
    if not has_permission(current_user, "view_roles"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view roles"
        )
    
    roles = db.query(Role).all()
    return roles

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific role by ID (admin only)."""
    # Check if user has permission to view roles
    if not has_permission(current_user, "view_roles"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view roles"
        )
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    return role

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a role by ID (admin only)."""
    # Check if user has permission to update roles
    if not has_permission(current_user, "update_role"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update roles"
        )
    
    # Check if role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Update role fields if provided
    if role_update.name is not None:
        # Check if new name already exists in another role
        existing_role = db.query(Role).filter(Role.name == role_update.name, Role.id != role_id).first()
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with name {role_update.name} already exists"
            )
        role.name = role_update.name
    
    if role_update.description is not None:
        role.description = role_update.description
    
    db.commit()
    db.refresh(role)
    
    # Record metric for role update
    metrics.record_rbac_operation("update_role", current_user.id)
    
    return role

@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a role by ID (admin only)."""
    # Check if user has permission to delete roles
    if not has_permission(current_user, "delete_role"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete roles"
        )
    
    # Check if role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Prevent deletion of built-in roles like 'admin' or 'user'
    if role.name in ["admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete built-in role: {role.name}"
        )
    
    # Delete role
    db.delete(role)
    db.commit()
    
    # Record metric for role deletion
    metrics.record_rbac_operation("delete_role", current_user.id)
    
    return None

# Permission Management
@router.post("/permissions", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new permission (admin only)."""
    # Check if user has permission to create permissions
    if not has_permission(current_user, "create_permission"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create permissions"
        )
    
    # Check if permission with same name already exists
    existing_permission = db.query(Permission).filter(Permission.name == permission.name).first()
    if existing_permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Permission with name {permission.name} already exists"
        )
    
    # Create new permission
    new_permission = Permission(
        name=permission.name,
        description=permission.description
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    
    # Record metric for permission creation
    metrics.record_rbac_operation("create_permission", current_user.id)
    
    return new_permission

@router.get("/permissions", response_model=List[PermissionResponse])
async def get_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all permissions (admin only)."""
    # Check if user has permission to view permissions
    if not has_permission(current_user, "view_permissions"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view permissions"
        )
    
    permissions = db.query(Permission).all()
    return permissions

@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific permission by ID (admin only)."""
    # Check if user has permission to view permissions
    if not has_permission(current_user, "view_permissions"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view permissions"
        )
    
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission with ID {permission_id} not found"
        )
    
    return permission

@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a permission by ID (admin only)."""
    # Check if user has permission to delete permissions
    if not has_permission(current_user, "delete_permission"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete permissions"
        )
    
    # Check if permission exists
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission with ID {permission_id} not found"
        )
    
    # Prevent deletion of built-in permissions
    protected_permissions = [
        "create_role", "update_role", "delete_role", "view_roles",
        "create_permission", "view_permissions", "delete_permission",
        "assign_permission", "revoke_permission",
        "assign_role", "revoke_role", "view_users"
    ]
    if permission.name in protected_permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete built-in permission: {permission.name}"
        )
    
    # Delete permission
    db.delete(permission)
    db.commit()
    
    # Record metric for permission deletion
    metrics.record_rbac_operation("delete_permission", current_user.id)
    
    return None

# Role-Permission Management
@router.post("/roles/{role_id}/permissions", response_model=RoleResponse)
async def assign_permissions_to_role(
    role_id: int,
    permission_request: RolePermissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign permissions to a role (admin only)."""
    # Check if user has permission to assign permissions
    if not has_permission(current_user, "assign_permission"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to assign permissions"
        )
    
    # Check if role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Get current role permissions
    current_permission_ids = [p.permission_id for p in role.permissions]
    
    # Add new permissions
    for permission_id in permission_request.permission_ids:
        # Skip if already assigned
        if permission_id in current_permission_ids:
            continue
        
        # Check if permission exists
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission with ID {permission_id} not found"
            )
        
        # Create role-permission association
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        db.add(role_permission)
    
    try:
        db.commit()
        db.refresh(role)
        
        # Record metric for permission assignment
        metrics.record_rbac_operation("assign_permission", current_user.id)
        
        return role
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error assigning permissions to role"
        )

@router.delete("/roles/{role_id}/permissions", response_model=RoleResponse)
async def revoke_permissions_from_role(
    role_id: int,
    permission_request: RolePermissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Revoke permissions from a role (admin only)."""
    # Check if user has permission to revoke permissions
    if not has_permission(current_user, "revoke_permission"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to revoke permissions"
        )
    
    # Check if role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Prevent removing critical permissions from admin role
    if role.name == "admin":
        protected_permissions = [
            "create_role", "update_role", "delete_role", "view_roles",
            "create_permission", "view_permissions", "delete_permission",
            "assign_permission", "revoke_permission",
            "assign_role", "revoke_role", "view_users"
        ]
        
        # Check if trying to remove protected permissions
        for permission_id in permission_request.permission_ids:
            permission = db.query(Permission).filter(Permission.id == permission_id).first()
            if permission and permission.name in protected_permissions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot remove essential permission '{permission.name}' from admin role"
                )
    
    # Remove permissions
    for permission_id in permission_request.permission_ids:
        db.query(RolePermission).filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        ).delete()
    
    db.commit()
    db.refresh(role)
    
    # Record metric for permission revocation
    metrics.record_rbac_operation("revoke_permission", current_user.id)
    
    return role

# User-Role Management
@router.post("/users/{user_id}/roles", response_model=UserWithRolesResponse)
async def assign_roles_to_user(
    user_id: int,
    role_request: UserRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign roles to a user (admin only)."""
    # Check if user has permission to assign roles
    if not has_permission(current_user, "assign_role"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to assign roles"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Get current user roles
    current_role_ids = [r.id for r in user.roles]
    
    # Add new roles
    for role_id in role_request.role_ids:
        # Skip if already assigned
        if role_id in current_role_ids:
            continue
        
        # Check if role exists
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with ID {role_id} not found"
            )
        
        # Add role to user
        user.roles.append(role)
    
    db.commit()
    db.refresh(user)
    
    # Record metric for role assignment
    metrics.record_rbac_operation("assign_role", current_user.id)
    
    return user

@router.delete("/users/{user_id}/roles", response_model=UserWithRolesResponse)
async def revoke_roles_from_user(
    user_id: int,
    role_request: UserRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Revoke roles from a user (admin only)."""
    # Check if user has permission to revoke roles
    if not has_permission(current_user, "revoke_role"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to revoke roles"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Prevent removing admin role from the last admin user
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if admin_role and admin_role.id in role_request.role_ids:
        # Check if this is the last admin
        admin_users_count = db.query(User).join(User.roles).filter(Role.name == "admin").count()
        if admin_users_count <= 1 and admin_role in user.roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove admin role from the last admin user"
            )
    
    # Remove roles
    for role_id in role_request.role_ids:
        role = db.query(Role).filter(Role.id == role_id).first()
        if role and role in user.roles:
            user.roles.remove(role)
    
    db.commit()
    db.refresh(user)
    
    # Record metric for role revocation
    metrics.record_rbac_operation("revoke_role", current_user.id)
    
    return user

@router.get("/users", response_model=List[UserWithRolesResponse])
async def get_users_with_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all users with their roles (admin only)."""
    # Check if user has permission to view users
    if not has_permission(current_user, "view_users"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view users"
        )
    
    users = db.query(User).all()
    return users

@router.get("/users/{user_id}/roles", response_model=UserWithRolesResponse)
async def get_user_roles(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get roles assigned to a specific user (admin only)."""
    # Check if user has permission to view roles
    if not has_permission(current_user, "view_roles") and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view user roles"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return user
