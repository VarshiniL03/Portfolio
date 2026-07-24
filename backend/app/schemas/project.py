from uuid import UUID
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    summary: str | None = None
    description: str | None = None
    tech_stack: list[str] = []
    image_url: str | None = None
    repo_url: str | None = None
    live_url: str | None = None
    featured: bool = False
    order_index: int = 0
    is_visible: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    description: str | None = None
    tech_stack: list[str] | None = None
    image_url: str | None = None
    repo_url: str | None = None
    live_url: str | None = None
    featured: bool | None = None
    order_index: int | None = None
    is_visible: bool | None = None


class ProjectOut(ProjectBase):
    id: UUID

    class Config:
        from_attributes = True
