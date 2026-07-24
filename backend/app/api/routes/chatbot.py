from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.db.session import get_db
from app.models.chatbot import ChatLog
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.services.chat_graph import get_chat_reply_graph

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/message", response_model=ChatResponse)
@limiter.limit("20/minute")  # keeps OpenAI costs predictable
def send_message(request: Request, payload: ChatRequest, db: Session = Depends(get_db)):
    reply, was_fallback, actions = get_chat_reply_graph(db, payload.session_id, payload.message)

    db.add(
    ChatLog(
        session_id=payload.session_id,
        user_message=payload.message,
        bot_response=reply,
        was_fallback=was_fallback,
    )
)
    db.commit()

    return ChatResponse(reply=reply, was_fallback=was_fallback, actions=actions)