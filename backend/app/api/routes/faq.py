from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.resources import faq_crud
from app.schemas.chatbot import FaqCreate, FaqOut, FaqUpdate
from app.api.deps import require_editor_or_admin

router = APIRouter(prefix="/faqs", tags=["faqs"])


@router.get("", response_model=list[FaqOut], dependencies=[Depends(require_editor_or_admin)])
def list_faqs(db: Session = Depends(get_db)):
    return faq_crud.list(db)


@router.post("", response_model=FaqOut, dependencies=[Depends(require_editor_or_admin)])
def create_faq(payload: FaqCreate, db: Session = Depends(get_db)):
    return faq_crud.create(db, payload)


@router.put("/{item_id}", response_model=FaqOut, dependencies=[Depends(require_editor_or_admin)])
def update_faq(item_id: UUID, payload: FaqUpdate, db: Session = Depends(get_db)):
    db_obj = faq_crud.get(db, item_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq_crud.update(db, db_obj, payload)


@router.delete("/{item_id}", status_code=204, dependencies=[Depends(require_editor_or_admin)])
def delete_faq(item_id: UUID, db: Session = Depends(get_db)):
    if not faq_crud.delete(db, item_id):
        raise HTTPException(status_code=404, detail="FAQ not found")
