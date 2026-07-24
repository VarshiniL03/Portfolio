"""
SiteContent is a "singleton" table: exactly one row holds all the editable
homepage text (hero, about, contact, social links). This is simpler than
having many tiny tables for text that only ever has one value.
"""
import uuid

from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class SiteContent(Base):
    __tablename__ = "site_content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Hero section
    hero_name = Column(String, default="")
    hero_title = Column(String, default="")  # e.g. "Full-Stack Engineer"
    hero_tagline = Column(Text, default="")
    hero_image_url = Column(String, nullable=True)

    # About / intro
    about_text = Column(Text, default="")

    # Contact
    contact_email = Column(String, default="")
    contact_phone = Column(String, nullable=True)
    contact_location = Column(String, nullable=True)

    # Social links stored as JSON: {"github": "...", "linkedin": "...", "twitter": "..."}
    social_links = Column(JSON, default=dict)

    # SEO
    meta_description = Column(Text, nullable=True)
