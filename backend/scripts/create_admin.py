"""
Run once after migrations to create the first admin user, using
FIRST_ADMIN_EMAIL / FIRST_ADMIN_PASSWORD from .env.

Usage:
    cd backend
    python -m scripts.create_admin
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.core.security import hash_password
from app.core.config import settings
from app.models.user import User, UserRole


def main():
    if not settings.FIRST_ADMIN_EMAIL or not settings.FIRST_ADMIN_PASSWORD:
        print("Set FIRST_ADMIN_EMAIL and FIRST_ADMIN_PASSWORD in .env first.")
        return

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
        if existing:
            print(f"Admin {settings.FIRST_ADMIN_EMAIL} already exists.")
            return

        user = User(
            email=settings.FIRST_ADMIN_EMAIL,
            hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
            full_name="Admin",
            role=UserRole.admin,
        )
        db.add(user)
        db.commit()
        print(f"Created admin user: {settings.FIRST_ADMIN_EMAIL}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
