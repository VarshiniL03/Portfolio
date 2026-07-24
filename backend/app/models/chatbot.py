import uuid

from sqlalchemy import Column, String, Text, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class FaqEntry(Base):
    """
    Editable knowledge base the chatbot draws on before falling back to the
    LLM's general reasoning. Admin manages these from the dashboard.
    """
    __tablename__ = "faq_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)
    is_visible = Column(Boolean, default=True)


class ChatLog(Base):
    """
    Stores each chatbot exchange for later review (helps you spot questions
    the bot answered poorly and improve the FAQ / system prompt).
    """
    __tablename__ = "chat_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String, index=True, nullable=False)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    was_fallback = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
