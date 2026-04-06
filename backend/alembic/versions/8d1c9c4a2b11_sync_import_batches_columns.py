"""sync import_batches columns with ORM model

Revision ID: 8d1c9c4a2b11
Revises: 573d50d9ff0e
Create Date: 2026-04-06
"""

from alembic import op
import sqlalchemy as sa


revision = "8d1c9c4a2b11"
down_revision = "573d50d9ff0e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "import_batches",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.add_column(
        "import_batches",
        sa.Column("error_message", sa.String(length=1000), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("import_batches", "error_message")
    op.drop_column("import_batches", "updated_at")