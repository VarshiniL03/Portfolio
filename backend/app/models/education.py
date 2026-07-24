import uuid

from sqlalchemy import Column, String, Text, Date, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class Education(Base):
    __tablename__ = "educations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    degree = Column(String, nullable=False)          # e.g. "B.Tech in Computer Science"
    institution = Column(String, nullable=False)
    location = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)            # null = ongoing
    grade = Column(String, nullable=True)              # e.g. "8.7 CGPA" / "First Class"
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
