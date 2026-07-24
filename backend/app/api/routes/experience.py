from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.resources import experience_crud
from app.schemas.experience import ExperienceCreate, ExperienceOut, ExperienceUpdate
from app.api.deps import require_editor_or_admin

router = APIRouter(prefix="/experiences", tags=["experiences"])


@router.get("", response_model=list[ExperienceOut])
def list_experiences(include_hidden: bool = False, db: Session = Depends(get_db)):
    """Public homepage calls this with no params (only visible items).
    The admin dashboard calls it with ?include_hidden=true to edit everything."""
    items = experience_crud.list(db)
    return items if include_hidden else [e for e in items if e.is_visible]


@router.post("", response_model=ExperienceOut, dependencies=[Depends(require_editor_or_admin)])
def create_experience(payload: ExperienceCreate, db: Session = Depends(get_db)):
    return experience_crud.create(db, payload)


@router.put("/{item_id}", response_model=ExperienceOut, dependencies=[Depends(require_editor_or_admin)])
def update_experience(item_id: UUID, payload: ExperienceUpdate, db: Session = Depends(get_db)):
    db_obj = experience_crud.get(db, item_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience_crud.update(db, db_obj, payload)


@router.delete("/{item_id}", status_code=204, dependencies=[Depends(require_editor_or_admin)])
def delete_experience(item_id: UUID, db: Session = Depends(get_db)):
    if not experience_crud.delete(db, item_id):
        raise HTTPException(status_code=404, detail="Experience not found")
