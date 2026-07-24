"""
Centralized application settings.

Everything here is loaded from environment variables (.env locally, or the
platform's secret store in production). NEVER hardcode secrets in this file.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- General ---
    ENVIRONMENT: str = "development"  # development | staging | production
    PROJECT_NAME: str = "Portfolio API"
    API_V1_PREFIX: str = "/api/v1"

    # --- Security ---
    SECRET_KEY: str  # required, set in .env — used to sign JWTs
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours
    ALGORITHM: str = "HS256"

    # --- Database ---
    DATABASE_URL: str  # e.g. postgresql://user:pass@host:5432/portfolio

    # --- CORS ---
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]

    # --- OpenAI / LangChain ---
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    # --- File storage (resume uploads) ---
    # "local" stores under /app/uploads (fine for a single container / dev).
    # "s3" stores in an S3-compatible bucket — recommended for Vercel/serverless
    # deployments since the filesystem there is ephemeral/read-only.
    STORAGE_BACKEND: str = "local"
    UPLOAD_DIR: str = "uploads"
    S3_BUCKET: str = ""
    S3_REGION: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # --- Admin bootstrap (used once by scripts/create_admin.py) ---
    FIRST_ADMIN_EMAIL: str = ""
    FIRST_ADMIN_PASSWORD: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
