"""
Small storage abstraction so the rest of the app doesn't care whether files
land on local disk (fine for a traditional server/Docker deployment) or S3
(recommended when the backend runs on serverless infra with an ephemeral
filesystem). Controlled by STORAGE_BACKEND in .env.
"""
import os
import uuid
from pathlib import Path

from app.core.config import settings


class StorageService:
    def save(self, file_bytes: bytes, filename: str, content_type: str) -> tuple[str, str]:
        """Returns (storage_path_or_key, public_url)."""
        raise NotImplementedError


class LocalStorageService(StorageService):
    def __init__(self):
        self.base_dir = Path(settings.UPLOAD_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, file_bytes: bytes, filename: str, content_type: str) -> tuple[str, str]:
        safe_name = f"{uuid.uuid4().hex}_{filename}"
        path = self.base_dir / safe_name
        with open(path, "wb") as f:
            f.write(file_bytes)
        # Served by the /resume/download static route (see routes/resume.py)
        public_url = f"/api/v1/resume/download/{safe_name}"
        return str(path), public_url


class S3StorageService(StorageService):
    def __init__(self):
        import boto3

        self.client = boto3.client(
            "s3",
            region_name=settings.S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.bucket = settings.S3_BUCKET

    def save(self, file_bytes: bytes, filename: str, content_type: str) -> tuple[str, str]:
        key = f"resumes/{uuid.uuid4().hex}_{filename}"
        self.client.put_object(
            Bucket=self.bucket, Key=key, Body=file_bytes, ContentType=content_type, ACL="public-read"
        )
        public_url = f"https://{self.bucket}.s3.{settings.S3_REGION}.amazonaws.com/{key}"
        return key, public_url


def get_storage_service() -> StorageService:
    if settings.STORAGE_BACKEND == "s3":
        return S3StorageService()
    return LocalStorageService()
