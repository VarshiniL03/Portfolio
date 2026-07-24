from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.models.resume import Resume
from app.schemas.resume import ResumeOut
from app.services.storage import get_storage_service
from app.api.deps import require_editor_or_admin

router = APIRouter(prefix="/resume", tags=["resume"])

ALLOWED_CONTENT_TYPES = {"application/pdf"}
MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


@router.get("/active", response_model=ResumeOut | None)
def get_active_resume(db: Session = Depends(get_db)):
    """Public — homepage 'Download Resume' button calls this."""
    return db.query(Resume).order_by(Resume.uploaded_at.desc()).first()


@router.post("/upload", response_model=ResumeOut, dependencies=[Depends(require_editor_or_admin)])
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    contents = await file.read()
    if len(contents) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    storage = get_storage_service()
    storage_path, public_url = storage.save(contents, file.filename, file.content_type)

    resume = Resume(
        file_name=file.filename,
        storage_path=storage_path,
        public_url=public_url,
        size_bytes=len(contents),
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


@router.get("/download/{filename}")
def download_resume_local(filename: str):
    """Only used when STORAGE_BACKEND=local. With S3, public_url points directly to the bucket."""
    path = Path(settings.UPLOAD_DIR) / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/pdf", filename=filename)
