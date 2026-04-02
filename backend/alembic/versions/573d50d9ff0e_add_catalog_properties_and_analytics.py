"""add catalog properties and analytics

Revision ID: 573d50d9ff0e
Revises: 54f71be89eed
Create Date: 2026-04-02
"""

from alembic import op
import sqlalchemy as sa

revision = "573d50d9ff0e"
down_revision = "54f71be89eed"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "catalog_properties",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(length=100), nullable=True),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("address_full", sa.String(length=500), nullable=True),
        sa.Column("project_name", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("street", sa.String(length=150), nullable=True),
        sa.Column("house", sa.String(length=50), nullable=True),
        sa.Column("building", sa.String(length=50), nullable=True),
        sa.Column("property_type", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="built"),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("external_id", name="uq_catalog_properties_external_id"),
    )
    op.create_index("ix_catalog_properties_display_name", "catalog_properties", ["display_name"])
    op.create_index("ix_catalog_properties_address_full", "catalog_properties", ["address_full"])
    op.create_index("ix_catalog_properties_project_name", "catalog_properties", ["project_name"])
    op.create_index("ix_catalog_properties_city", "catalog_properties", ["city"])
    op.create_index("ix_catalog_properties_is_active", "catalog_properties", ["is_active"])

    op.create_table(
        "property_analytics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("catalog_property_id", sa.Integer(), nullable=False),
        sa.Column("infrastructure", sa.Integer(), nullable=False),
        sa.Column("lighting", sa.Integer(), nullable=False),
        sa.Column("noise", sa.Integer(), nullable=False),
        sa.Column("insolation", sa.Integer(), nullable=False),
        sa.Column("development", sa.Integer(), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False, server_default="csv"),
        sa.Column("source_label", sa.String(length=255), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(
            ["catalog_property_id"],
            ["catalog_properties.id"],
            name="fk_property_analytics_catalog_property_id",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_property_analytics_catalog_property_id", "property_analytics", ["catalog_property_id"])
    op.create_index("ix_property_analytics_is_published", "property_analytics", ["is_published"])
    op.create_index("ix_property_analytics_source_type", "property_analytics", ["source_type"])

    op.create_table(
        "import_batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False, server_default="csv"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("rows_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rows_created", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rows_updated", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rows_failed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_import_batches_status", "import_batches", ["status"])
    op.create_index("ix_import_batches_created_at", "import_batches", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_import_batches_created_at", table_name="import_batches")
    op.drop_index("ix_import_batches_status", table_name="import_batches")
    op.drop_table("import_batches")

    op.drop_index("ix_property_analytics_source_type", table_name="property_analytics")
    op.drop_index("ix_property_analytics_is_published", table_name="property_analytics")
    op.drop_index("ix_property_analytics_catalog_property_id", table_name="property_analytics")
    op.drop_table("property_analytics")

    op.drop_index("ix_catalog_properties_is_active", table_name="catalog_properties")
    op.drop_index("ix_catalog_properties_city", table_name="catalog_properties")
    op.drop_index("ix_catalog_properties_project_name", table_name="catalog_properties")
    op.drop_index("ix_catalog_properties_address_full", table_name="catalog_properties")
    op.drop_index("ix_catalog_properties_display_name", table_name="catalog_properties")
    op.drop_table("catalog_properties")