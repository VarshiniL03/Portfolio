from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.resources import project_crud
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.api.deps import require_editor_or_admin

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectOut])
def list_projects(include_hidden: bool = False, db: Session = Depends(get_db)):
    items = project_crud.list(db)
    return items if include_hidden else [p for p in items if p.is_visible]


@router.post("", response_model=ProjectOut, dependencies=[Depends(require_editor_or_admin)])
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    return project_crud.create(db, payload)


@router.put("/{item_id}", response_model=ProjectOut, dependencies=[Depends(require_editor_or_admin)])
def update_project(item_id: UUID, payload: ProjectUpdate, db: Session = Depends(get_db)):
    db_obj = project_crud.get(db, item_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_crud.update(db, db_obj, payload)


@router.delete("/{item_id}", status_code=204, dependencies=[Depends(require_editor_or_admin)])
def delete_project(item_id: UUID, db: Session = Depends(get_db)):
    if not project_crud.delete(db, item_id):
        raise HTTPException(status_code=404, detail="Project not found")
