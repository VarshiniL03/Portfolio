from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ResumeOut(BaseModel):
    id: UUID
    file_name: str
    public_url: str | None = None
    uploaded_at: datetime

    class Config:
        from_attributes = True
