"""reduce embedding dimension for local sentence-transformers model

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-14
"""
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("TRUNCATE knowledge_chunks")  # old 1536-dim embeddings are incompatible, clear them
    op.execute("ALTER TABLE knowledge_chunks ALTER COLUMN embedding TYPE vector(384)")


def downgrade():
    op.execute("TRUNCATE knowledge_chunks")
    op.execute("ALTER TABLE knowledge_chunks ALTER COLUMN embedding TYPE vector(1536)")