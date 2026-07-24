import enum
import uuid

from sqlalchemy import Column, String, Text, Date, Enum, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class AchievementType(str, enum.Enum):
    certification = "certification"
    award = "award"
    publication = "publication"
    other = "other"


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(AchievementType), default=AchievementType.other)
    title = Column(String, nullable=False)
    issuer = Column(String, nullable=True)             # certifying body / awarding org
    date = Column(Date, nullable=True)
    credential_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
