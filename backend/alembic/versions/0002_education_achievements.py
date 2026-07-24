"""replace qualifications with education and achievements

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "educations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("degree", sa.String, nullable=False),
        sa.Column("institution", sa.String, nullable=False),
        sa.Column("location", sa.String, nullable=True),
        sa.Column("start_date", sa.Date, nullable=True),
        sa.Column("end_date", sa.Date, nullable=True),
        sa.Column("grade", sa.String, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("order_index", sa.Integer, server_default="0"),
        sa.Column("is_visible", sa.Boolean, server_default=sa.true()),
    )

    op.create_table(
        "achievements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "type",
            sa.Enum("certification", "award", "publication", "other", name="achievementtype"),
            server_default="other",
        ),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("issuer", sa.String, nullable=True),
        sa.Column("date", sa.Date, nullable=True),
        sa.Column("credential_url", sa.String, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("order_index", sa.Integer, server_default="0"),
        sa.Column("is_visible", sa.Boolean, server_default=sa.true()),
    )

    op.drop_table("qualifications")
    op.execute("DROP TYPE IF EXISTS qualificationtype")


def downgrade():
    op.create_table(
        "qualifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "type",
            sa.Enum("degree", "certification", "award", name="qualificationtype"),
            server_default="certification",
        ),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("issuer", sa.String, nullable=True),
        sa.Column("issue_date", sa.Date, nullable=True),
        sa.Column("expiry_date", sa.Date, nullable=True),
        sa.Column("credential_url", sa.String, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("order_index", sa.Integer, server_default="0"),
        sa.Column("is_visible", sa.Boolean, server_default=sa.true()),
    )
    op.drop_table("achievements")
    op.drop_table("educations")
    op.execute("DROP TYPE IF EXISTS achievementtype")
