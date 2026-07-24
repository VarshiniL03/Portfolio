"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-07-05

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String, unique=True, index=True, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("full_name", sa.String, nullable=True),
        sa.Column("role", sa.Enum("admin", "editor", name="userrole"), nullable=False),
        sa.Column("is_active", sa.String, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "experiences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company", sa.String, nullable=False),
        sa.Column("role", sa.String, nullable=False),
        sa.Column("location", sa.String, nullable=True),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("order_index", sa.Integer, server_default="0"),
        sa.Column("is_visible", sa.Boolean, server_default=sa.true()),
    )

    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("summary", sa.String, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("tech_stack", postgresql.ARRAY(sa.String), server_default="{}"),
        sa.Column("image_url", sa.String, nullable=True),
        sa.Column("repo_url", sa.String, nullable=True),
        sa.Column("live_url", sa.String, nullable=True),
        sa.Column("featured", sa.Boolean, server_default=sa.false()),
        sa.Column("order_index", sa.Integer, server_default="0"),
        sa.Column("is_visible", sa.Boolean, server_default=sa.true()),
    )

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

    op.create_table(
        "site_content",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("hero_name", sa.String, server_default=""),
        sa.Column("hero_title", sa.String, server_default=""),
        sa.Column("hero_tagline", sa.Text, server_default=""),
        sa.Column("hero_image_url", sa.String, nullable=True),
        sa.Column("about_text", sa.Text, server_default=""),
        sa.Column("contact_email", sa.String, server_default=""),
        sa.Column("contact_phone", sa.String, nullable=True),
        sa.Column("contact_location", sa.String, nullable=True),
        sa.Column("social_links", sa.JSON, server_default="{}"),
        sa.Column("meta_description", sa.Text, nullable=True),
    )

    op.create_table(
        "resumes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("file_name", sa.String, nullable=False),
        sa.Column("storage_path", sa.String, nullable=False),
        sa.Column("public_url", sa.String, nullable=True),
        sa.Column("size_bytes", sa.Integer, nullable=True),
        sa.Column("is_active", sa.String, server_default="true"),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "faq_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("question", sa.String, nullable=False),
        sa.Column("answer", sa.Text, nullable=False),
        sa.Column("is_visible", sa.Boolean, server_default=sa.true()),
    )

    op.create_table(
        "chat_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", sa.String, index=True, nullable=False),
        sa.Column("user_message", sa.Text, nullable=False),
        sa.Column("bot_response", sa.Text, nullable=False),
        sa.Column("was_fallback", sa.Boolean, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("chat_logs")
    op.drop_table("faq_entries")
    op.drop_table("resumes")
    op.drop_table("site_content")
    op.drop_table("qualifications")
    op.drop_table("projects")
    op.drop_table("experiences")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS qualificationtype")
