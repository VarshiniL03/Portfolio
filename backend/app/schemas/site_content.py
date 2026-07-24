from uuid import UUID
from pydantic import BaseModel


class SiteContentBase(BaseModel):
    hero_name: str = ""
    hero_title: str = ""
    hero_tagline: str = ""
    hero_image_url: str | None = None
    about_text: str = ""
    contact_email: str = ""
    contact_phone: str | None = None
    contact_location: str | None = None
    social_links: dict = {}
    meta_description: str | None = None


class SiteContentUpdate(SiteContentBase):
    pass


class SiteContentOut(SiteContentBase):
    id: UUID

    class Config:
        from_attributes = True
