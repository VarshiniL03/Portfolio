from uuid import UUID
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=2000)


class ChatAction(BaseModel):
    type: str   # "resume" | "email" | "linkedin"
    url: str
    label: str


class ChatResponse(BaseModel):
    reply: str
    was_fallback: bool = False
    actions: list[ChatAction] = []


class FaqBase(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    answer: str = Field(..., min_length=1)
    is_visible: bool = True


class FaqCreate(FaqBase):
    pass


class FaqUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None
    is_visible: bool | None = None


class FaqOut(FaqBase):
    id: UUID

    class Config:
        from_attributes = True
