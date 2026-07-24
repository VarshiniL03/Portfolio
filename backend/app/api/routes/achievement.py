from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.resources import achievement_crud
from app.schemas.achievement import AchievementCreate, AchievementOut, AchievementUpdate
from app.api.deps import require_editor_or_admin

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("", response_model=list[AchievementOut])
def list_achievements(include_hidden: bool = False, db: Session = Depends(get_db)):
    items = achievement_crud.list(db)
    return items if include_hidden else [a for a in items if a.is_visible]


@router.post("", response_model=AchievementOut, dependencies=[Depends(require_editor_or_admin)])
def create_achievement(payload: AchievementCreate, db: Session = Depends(get_db)):
    return achievement_crud.create(db, payload)


@router.put("/{item_id}", response_model=AchievementOut, dependencies=[Depends(require_editor_or_admin)])
def update_achievement(item_id: UUID, payload: AchievementUpdate, db: Session = Depends(get_db)):
    db_obj = achievement_crud.get(db, item_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return achievement_crud.update(db, db_obj, payload)


@router.delete("/{item_id}", status_code=204, dependencies=[Depends(require_editor_or_admin)])
def delete_achievement(item_id: UUID, db: Session = Depends(get_db)):
    if not achievement_crud.delete(db, item_id):
        raise HTTPException(status_code=404, detail="Achievement not found")
