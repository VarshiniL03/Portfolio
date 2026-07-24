from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field


class EducationBase(BaseModel):
    degree: str = Field(..., min_length=1, max_length=200)
    institution: str = Field(..., min_length=1, max_length=200)
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    grade: str | None = None
    description: str | None = None
    order_index: int = 0
    is_visible: bool = True


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    degree: str | None = None
    institution: str | None = None
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    grade: str | None = None
    description: str | None = None
    order_index: int | None = None
    is_visible: bool | None = None


class EducationOut(EducationBase):
    id: UUID

    class Config:
        from_attributes = True
