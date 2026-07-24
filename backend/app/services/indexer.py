"""
Builds the RAG knowledge base: turns every piece of portfolio content into
one "chunk" of text, embeds all of them in a single batch API call, and
replaces whatever was previously stored in knowledge_chunks.

This is a full rebuild rather than incremental updates — simpler to reason
about, and cheap enough at personal-portfolio scale (dozens of chunks, not
thousands). Triggered manually via POST /api/v1/admin/reindex, or you can
call reindex_all() automatically after any content save if you prefer
always-fresh results (see chatbot.py's routes for where you'd hook that in).
"""
from sqlalchemy.orm import Session

from app.models.experience import Experience
from app.models.project import Project
from app.models.education import Education
from app.models.achievement import Achievement
from app.models.chatbot import FaqEntry
from app.models.site_content import SiteContent
from app.models.knowledge_chunk import KnowledgeChunk
from app.services.embeddings import get_embeddings_batch


def _build_chunks(db: Session) -> list[tuple[str, str, str]]:
    """Returns a list of (source_type, source_id, content) tuples — one per chunk."""
    chunks = []

    site = db.query(SiteContent).first()
    if site and (site.about_text or site.hero_tagline):
        text = f"About {site.hero_name}, {site.hero_title}. {site.hero_tagline} {site.about_text}"
        chunks.append(("site_content", str(site.id), text.strip()))

    for e in db.query(Experience).filter(Experience.is_visible.is_(True)).all():
        text = (
            f"Work experience: {e.role} at {e.company} "
            f"({e.start_date} to {e.end_date or 'present'}). {e.description or ''}"
        )
        chunks.append(("experience", str(e.id), text.strip()))

    for p in db.query(Project).filter(Project.is_visible.is_(True)).all():
        text = (
            f"Project: {p.title}. {p.summary or ''} {p.description or ''} "
            f"Technologies used: {', '.join(p.tech_stack or [])}."
        )
        chunks.append(("project", str(p.id), text.strip()))

    for ed in db.query(Education).filter(Education.is_visible.is_(True)).all():
        text = (
            f"Education: {ed.degree} from {ed.institution} "
            f"({ed.start_date or ''} to {ed.end_date or 'present'}). {ed.description or ''}"
        )
        chunks.append(("education", str(ed.id), text.strip()))

    for a in db.query(Achievement).filter(Achievement.is_visible.is_(True)).all():
        text = f"{a.type.value.title()}: {a.title}, issued by {a.issuer or 'N/A'}. {a.description or ''}"
        chunks.append(("achievement", str(a.id), text.strip()))

    for f in db.query(FaqEntry).filter(FaqEntry.is_visible.is_(True)).all():
        text = f"Q: {f.question}\nA: {f.answer}"
        chunks.append(("faq", str(f.id), text.strip()))

    return chunks


def reindex_all(db: Session) -> int:
    """Rebuilds the entire knowledge base. Returns the number of chunks indexed."""
    chunks = _build_chunks(db)
    if not chunks:
        db.query(KnowledgeChunk).delete()
        db.commit()
        return 0

    texts = [c[2] for c in chunks]
    embeddings = get_embeddings_batch(texts)

    # Full replace: simplest correct behavior, avoids stale/orphaned chunks
    # when content is deleted or edited.
    db.query(KnowledgeChunk).delete()
    for (source_type, source_id, content), embedding in zip(chunks, embeddings):
        db.add(
            KnowledgeChunk(
                source_type=source_type,
                source_id=source_id,
                content=content,
                embedding=embedding,
            )
        )
    db.commit()
    return len(chunks)
