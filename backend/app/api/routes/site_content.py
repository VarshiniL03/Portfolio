from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.site_content import SiteContent
from app.schemas.site_content import SiteContentOut, SiteContentUpdate
from app.api.deps import require_editor_or_admin

router = APIRouter(prefix="/site-content", tags=["site-content"])


def _get_or_create(db: Session) -> SiteContent:
    obj = db.query(SiteContent).first()
    if not obj:
        obj = SiteContent()
        db.add(obj)
        db.commit()
        db.refresh(obj)
    return obj


@router.get("", response_model=SiteContentOut)
def get_site_content(db: Session = Depends(get_db)):
    """Public — powers hero/about/contact sections and social links on the homepage."""
    return _get_or_create(db)


@router.put("", response_model=SiteContentOut, dependencies=[Depends(require_editor_or_admin)])
def update_site_content(payload: SiteContentUpdate, db: Session = Depends(get_db)):
    obj = _get_or_create(db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
