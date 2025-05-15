"""
Initial migration for GrimOS backend

Revision ID: 0001
Revises: None
Create Date: 2025-05-15
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create threat_indicators table
    op.create_table('threat_indicators',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('indicator_value', sa.String(), nullable=False, index=True),
        sa.Column('indicator_type', sa.String(), nullable=False, index=True),
        sa.Column('source', sa.String(), nullable=False, index=True),
        sa.Column('severity', sa.String(), nullable=True, index=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('tags', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('first_seen', sa.DateTime(), nullable=True),
        sa.Column('last_seen', sa.DateTime(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    
    # Create uba_login_anomaly_alerts table
    op.create_table('uba_login_anomaly_alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('username', sa.String(), nullable=False, index=True),
        sa.Column('alert_type', sa.String(), nullable=False, index=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False, index=True),
        sa.Column('status', sa.String(), nullable=False, index=True, server_default='new'),
        sa.Column('severity', sa.String(), nullable=False, index=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    
    # Create workflow_definitions table
    op.create_table('workflow_definitions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(), nullable=False, index=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False, index=True),
    )
    
    # Create runes table
    op.create_table('runes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('workflow_definition_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('workflow_definitions.id'), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('next_step_id', sa.String(), nullable=True),
        sa.Column('condition_true_next_step_id', sa.String(), nullable=True),
        sa.Column('condition_false_next_step_id', sa.String(), nullable=True),
    )
    
    # Create workflow_instances table
    op.create_table('workflow_instances',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('definition_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('workflow_definitions.id'), nullable=False, index=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, index=True, server_default='pending'),
        sa.Column('current_step_id', sa.String(), nullable=True),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('result', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('error', sa.String(), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('execution_log', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    
    # Create scrollweaver_requests table
    op.create_table('scrollweaver_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('natural_language_input', sa.Text(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('response', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('processing_status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('error', sa.String(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
    )
    
    # Create analysis_trends table
    op.create_table('analysis_trends',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('trend_type', sa.String(), nullable=False, index=True),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('resource_type', sa.String(), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False, index=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('analysis_trends')
    op.drop_table('scrollweaver_requests')
    op.drop_table('workflow_instances')
    op.drop_table('runes')
    op.drop_table('workflow_definitions')
    op.drop_table('uba_login_anomaly_alerts')
    op.drop_table('threat_indicators')
