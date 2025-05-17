from pydantic import BaseModel
from typing import List, Optional

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int
    permissions: List[PermissionResponse] = []

    class Config:
        orm_mode = True

class RolePermissionRequest(BaseModel):
    permission_ids: List[int]

class UserRoleRequest(BaseModel):
    role_ids: List[int]

class UserWithRolesResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    active: bool
    roles: List[RoleResponse] = []

    class Config:
        orm_mode = True
