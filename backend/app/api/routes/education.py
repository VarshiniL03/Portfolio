from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.resources import education_crud
from app.schemas.education import EducationCreate, EducationOut, EducationUpdate
from app.api.deps import require_editor_or_admin

router = APIRouter(prefix="/education", tags=["education"])


@router.get("", response_model=list[EducationOut])
def list_education(include_hidden: bool = False, db: Session = Depends(get_db)):
    items = education_crud.list(db)
    return items if include_hidden else [e for e in items if e.is_visible]


@router.post("", response_model=EducationOut, dependencies=[Depends(require_editor_or_admin)])
def create_education(payload: EducationCreate, db: Session = Depends(get_db)):
    return education_crud.create(db, payload)


@router.put("/{item_id}", response_model=EducationOut, dependencies=[Depends(require_editor_or_admin)])
def update_education(item_id: UUID, payload: EducationUpdate, db: Session = Depends(get_db)):
    db_obj = education_crud.get(db, item_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Education entry not found")
    return education_crud.update(db, db_obj, payload)


@router.delete("/{item_id}", status_code=204, dependencies=[Depends(require_editor_or_admin)])
def delete_education(item_id: UUID, db: Session = Depends(get_db)):
    if not education_crud.delete(db, item_id):
        raise HTTPException(status_code=404, detail="Education entry not found")
