"""Add OAuth fields to User model

Revision ID: 002_oauth_user_fields
Revises: 001_rbac_tables
Create Date: 2025-05-16 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_oauth_user_fields'
down_revision = '001_rbac_tables'
branch_labels = None
depends_on = None


def upgrade():
    # Add OAuth-related fields to User model
    op.add_column('users', sa.Column('oauth_provider', sa.String(), nullable=True))
    op.add_column('users', sa.Column('oauth_id', sa.String(), nullable=True))
    op.add_column('users', sa.Column('avatar_url', sa.String(), nullable=True))
    
    # Alter hashed_password to be nullable (for OAuth users)
    op.alter_column('users', 'hashed_password', existing_type=sa.String(), nullable=True)
    
    # Add description to Role model
    op.add_column('roles', sa.Column('description', sa.Text(), nullable=True))
    
    # Update the existing roles with descriptions
    op.execute("UPDATE roles SET description = 'Administrator with full system access' WHERE name = 'admin'")
    op.execute("UPDATE roles SET description = 'Regular user with limited access' WHERE name = 'user'")


def downgrade():
    # Remove the fields
    op.drop_column('users', 'oauth_provider')
    op.drop_column('users', 'oauth_id')
    op.drop_column('users', 'avatar_url')
    
    # Make hashed_password required again
    op.alter_column('users', 'hashed_password', existing_type=sa.String(), nullable=False)
    
    # Remove description from Role model
    op.drop_column('roles', 'description')
