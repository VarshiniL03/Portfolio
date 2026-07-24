from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field


class ExperienceBase(BaseModel):
    company: str = Field(..., min_length=1, max_length=200)
    role: str = Field(..., min_length=1, max_length=200)
    location: str | None = None
    start_date: date
    end_date: date | None = None
    description: str | None = None
    order_index: int = 0
    is_visible: bool = True


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    order_index: int | None = None
    is_visible: bool | None = None


class ExperienceOut(ExperienceBase):
    id: UUID

    class Config:
        from_attributes = True
