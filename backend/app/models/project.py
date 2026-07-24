import uuid

from sqlalchemy import Column, String, Text, Boolean, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    tech_stack = Column(ARRAY(String), default=list)
    image_url = Column(String, nullable=True)
    repo_url = Column(String, nullable=True)
    live_url = Column(String, nullable=True)
    featured = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
