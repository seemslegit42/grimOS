"""RBAC tables creation

Revision ID: 001_rbac_tables
Revises: 
Create Date: 2025-05-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_rbac_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create role_permissions table
    op.create_table(
        'role_permissions',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    
    # Create user_role table
    op.create_table(
        'user_role',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    
    # Insert default roles
    op.execute("INSERT INTO roles (name) VALUES ('admin'), ('user')")
    
    # Insert default permissions
    op.execute("INSERT INTO permissions (name, description) VALUES ('read', 'Read access'), ('write', 'Write access'), ('delete', 'Delete access')")
    
    # Assign permissions to admin role
    op.execute("""
    INSERT INTO role_permissions (role_id, permission_id)
    SELECT r.id, p.id FROM roles r, permissions p
    WHERE r.name = 'admin'
    """)
    
    # Assign read permission to user role
    op.execute("""
    INSERT INTO role_permissions (role_id, permission_id)
    SELECT r.id, p.id FROM roles r, permissions p
    WHERE r.name = 'user' AND p.name = 'read'
    """)


def downgrade():
    op.drop_table('user_role')
    op.drop_table('role_permissions')
    op.drop_table('permissions')
    op.drop_table('roles')
