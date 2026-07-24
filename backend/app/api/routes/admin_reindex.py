from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.services.indexer import reindex_all
from app.api.deps import require_editor_or_admin

router = APIRouter(prefix="/admin", tags=["admin"])


class ReindexResponse(BaseModel):
    chunks_indexed: int


@router.post("/reindex", response_model=ReindexResponse, dependencies=[Depends(require_editor_or_admin)])
def trigger_reindex(db: Session = Depends(get_db)):
    """
    Rebuilds the chatbot's knowledge base from current portfolio content.
    Call this after adding/editing/deleting experience, projects, education,
    achievements, FAQs, or homepage content, so the chatbot's answers stay current.
    """
    count = reindex_all(db)
    return ReindexResponse(chunks_indexed=count)
