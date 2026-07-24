import uuid

from sqlalchemy import Column, String, Text, Date, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    location = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # null = current role
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)  # controls display order in admin UI
    is_visible = Column(Boolean, default=True)
