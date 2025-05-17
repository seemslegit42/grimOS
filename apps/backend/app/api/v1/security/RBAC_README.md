# Role-Based Access Control (RBAC) in grimOS

This document describes the RBAC implementation in grimOS.

## Overview

The RBAC system in grimOS provides a flexible and secure way to control access to resources based on user roles and permissions. It consists of:

1. **Users**: Individual accounts that authenticate with the system
2. **Roles**: Named collections of permissions (e.g., admin, user)
3. **Permissions**: Granular access controls for specific actions (e.g., read, write, delete)

## Database Schema

The RBAC system uses the following database tables:

- `users`: Stores user account information
- `roles`: Defines available roles in the system
- `permissions`: Lists available permissions
- `role_permissions`: Maps which permissions belong to which roles
- `user_role`: Maps which users have which roles

## Default Roles and Permissions

By default, the system includes:

- **Roles**:
  - `admin`: Full system access
  - `user`: Limited access for regular users

- **Permissions**:
  - `read`: Ability to view resources
  - `write`: Ability to create and modify resources
  - `delete`: Ability to remove resources

## API Endpoints

### Role Management

- `GET /api/v1/rbac/roles`: List all roles
- `POST /api/v1/rbac/roles`: Create a new role
- `PUT /api/v1/rbac/roles/{role_id}`: Update role permissions
- `DELETE /api/v1/rbac/roles/{role_id}`: Delete a role

### User-Role Management

- `POST /api/v1/rbac/users/{user_id}/roles`: Assign a role to a user
- `DELETE /api/v1/rbac/users/{user_id}/roles/{role_name}`: Remove a role from a user
- `GET /api/v1/rbac/users/{user_id}/roles`: Get all roles for a user

## Usage in Code

To protect routes based on roles or permissions, use the provided dependency factories:

```python
from app.api.v1.security.auth import has_role, has_permission

# Require admin role
@router.get("/admin-only")
async def admin_only(user: User = Depends(has_role(["admin"]))):
    return {"message": "You are an admin!"}

# Require delete permission
@router.delete("/items/{item_id}")
async def delete_item(item_id: int, user: User = Depends(has_permission(["delete"]))):
    return {"message": "Item deleted"}
```

## Future Improvements

1. Add role hierarchies (role inheritance)
2. Implement resource-specific permissions
3. Support for custom permission validators
4. Audit logging for permission checks
