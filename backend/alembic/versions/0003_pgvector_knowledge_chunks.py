"""add pgvector extension and knowledge_chunks table

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-14

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

EMBEDDING_DIM = 1536


def upgrade():
    # Enable the pgvector extension (requires it to be installed on the
    # Postgres server — the official postgres:16 Docker image does NOT have
    # it by default, see the setup instructions for the pgvector Docker image).
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "knowledge_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_type", sa.String, nullable=False),
        sa.Column("source_id", sa.String, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # IVFFlat index for fast approximate nearest-neighbor search.
    # Fine to create even on an empty table; pgvector will use it once populated.
    op.execute(
        "CREATE INDEX knowledge_chunks_embedding_idx ON knowledge_chunks "
        "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )


def downgrade():
    op.drop_index("knowledge_chunks_embedding_idx", table_name="knowledge_chunks")
    op.drop_table("knowledge_chunks")
    op.execute("DROP EXTENSION IF EXISTS vector")
