import uuid

from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

from app.db.session import Base

# text-embedding-3-small produces 1536-dimensional vectors
EMBEDDING_DIM = 384


class KnowledgeChunk(Base):
    """
    One row per retrievable piece of content (one project, one experience
    entry, one FAQ answer, etc.), plus its embedding vector.

    source_type/source_id let us find-and-replace a chunk when its original
    record changes, without needing to re-embed everything else.
    """
    __tablename__ = "knowledge_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type = Column(String, nullable=False)   # "experience" | "project" | "education" | "achievement" | "faq" | "site_content"
    source_id = Column(String, nullable=False)      # the original row's id (as text), or a fixed key for site_content
    content = Column(Text, nullable=False)           # the human-readable text that was embedded
    embedding = Column(Vector(EMBEDDING_DIM), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
