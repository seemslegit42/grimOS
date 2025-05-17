"""
Initial schema for User Authentication service.

Revision ID: 20230516_user_auth
Revises: 
Create Date: 2025-05-16
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20230516_user_auth'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True)
    )

    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True)
    )

    # Create user_role mapping table
    op.create_table(
        'user_role',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    )

    # Create role_permission mapping table
    op.create_table(
        'role_permission',
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('permission_id', sa.Integer, sa.ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
    )

def downgrade():
    op.drop_table('role_permission')
    op.drop_table('user_role')
    op.drop_table('permissions')
    op.drop_table('roles')
    op.drop_table('users')
