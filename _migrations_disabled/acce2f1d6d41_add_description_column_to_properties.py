"""add description column to properties

Revision ID: acce2f1d6d41
Revises: 54f71be89eed
Create Date: 2026-03-30 11:23:49.576541

"""
from alembic import op
import sqlalchemy as sa

revision = "НОВЫЙ_ID"
down_revision = "54f71be89eed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("properties", sa.Column("description", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("properties", "description")