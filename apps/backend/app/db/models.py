from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# User-Role association table for many-to-many relationship
user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Can be null for OAuth users
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    oauth_provider = Column(String, nullable=True)  # google, github, microsoft, etc.
    oauth_id = Column(String, nullable=True)  # Provider-specific user ID
    avatar_url = Column(String, nullable=True)  # Profile picture URL
    
    # Relationship to roles
    roles = relationship("Role", secondary=user_role, back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationship to users
    users = relationship("User", secondary=user_role, back_populates="roles")
    # Relationship to permissions
    permissions = relationship("RolePermission", back_populates="role")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Relationship to roles through RolePermission
    roles = relationship("RolePermission", back_populates="permission")

class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)
    
    # Relationships
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")
