from datetime import date as date_type
from uuid import UUID
from pydantic import BaseModel, Field

from app.models.achievement import AchievementType


class AchievementBase(BaseModel):
    type: AchievementType = AchievementType.other
    title: str = Field(..., min_length=1, max_length=200)
    issuer: str | None = None
    date: date_type | None = None
    credential_url: str | None = None
    description: str | None = None
    order_index: int = 0
    is_visible: bool = True


class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(BaseModel):
    type: AchievementType | None = None
    title: str | None = None
    issuer: str | None = None
    date: date_type | None = None
    credential_url: str | None = None
    description: str | None = None
    order_index: int | None = None
    is_visible: bool | None = None


class AchievementOut(AchievementBase):
    id: UUID

    class Config:
        from_attributes = True
