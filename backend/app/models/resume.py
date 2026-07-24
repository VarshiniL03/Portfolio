import uuid

from sqlalchemy import Column, String, DateTime, Integer, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class Resume(Base):
    """
    Tracks uploaded resume files. Only the most recently uploaded row is
    considered "active" (is_active flag lets you keep history if desired).
    """
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)  # local path or S3 key
    public_url = Column(String, nullable=True)
    size_bytes = Column(Integer, nullable=True)
    is_active = Column(String, default="true")
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
