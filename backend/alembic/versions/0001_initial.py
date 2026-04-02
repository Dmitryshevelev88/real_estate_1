"""initial schema

Revision ID: 0001_initial
Revises: None
Create Date: 2026-03-30 00:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

assessment_status = sa.Enum("draft", "submitted", name="assessmentstatus")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "score_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("infrastructure_weight", sa.Float(), nullable=False, server_default="0.2"),
        sa.Column("lighting_weight", sa.Float(), nullable=False, server_default="0.2"),
        sa.Column("noise_weight", sa.Float(), nullable=False, server_default="0.2"),
        sa.Column("insolation_weight", sa.Float(), nullable=False, server_default="0.2"),
        sa.Column("development_weight", sa.Float(), nullable=False, server_default="0.2"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "properties",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=500), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("property_type", sa.String(length=50), nullable=True),
        sa.Column("created_by_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "assessments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("property_id", sa.Integer(), sa.ForeignKey("properties.id"), nullable=False),
        sa.Column("assessor_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("score_profile_id", sa.Integer(), sa.ForeignKey("score_profiles.id"), nullable=False),
        sa.Column("infrastructure", sa.Float(), nullable=False),
        sa.Column("lighting", sa.Float(), nullable=False),
        sa.Column("noise", sa.Float(), nullable=False),
        sa.Column("insolation", sa.Float(), nullable=False),
        sa.Column("development", sa.Float(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("status", assessment_status, nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "computed_scores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("assessment_id", sa.Integer(), sa.ForeignKey("assessments.id"), nullable=False, unique=True),
        sa.Column("total_score", sa.Float(), nullable=False),
        sa.Column("calculation_version", sa.String(length=50), nullable=False, server_default="v1"),
        sa.Column("details_json", sa.JSON(), nullable=True),
        sa.Column("computed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "attachments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("assessment_id", sa.Integer(), sa.ForeignKey("assessments.id"), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("storage_path", sa.String(length=500), nullable=False),
        sa.Column("content_type", sa.String(length=100), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.execute(
        """
        INSERT INTO score_profiles (
            name, infrastructure_weight, lighting_weight, noise_weight, insolation_weight, development_weight
        ) VALUES (
            'default_mvp', 0.2, 0.2, 0.2, 0.2, 0.2
        );
        """
    )


def downgrade() -> None:
    op.drop_table("attachments")
    op.drop_table("computed_scores")
    op.drop_table("assessments")
    op.drop_table("properties")
    op.drop_table("score_profiles")
    op.drop_table("users")
    assessment_status.drop(op.get_bind(), checkfirst=False)
