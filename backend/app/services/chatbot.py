"""
Chatbot service — RAG-backed. Text replies come from the LLM; structured
"actions" (resume download, email, LinkedIn) are detected server-side via
keyword matching and returned separately, so the frontend can render them as
real buttons/icons instead of plain text links.
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings
from app.models.knowledge_chunk import KnowledgeChunk
from app.models.site_content import SiteContent
from app.models.resume import Resume
from app.models.education import Education
from app.models.project import Project
from app.services.embeddings import get_embedding
from app.schemas.chatbot import ChatAction
from app.models.achievement import Achievement
from app.models.experience import Experience

FALLBACK_MESSAGE = "This is out of context. Please ask only about my portfolio."

TOP_K = 5
MAX_DISTANCE = 0.55

RESUME_KEYWORDS = ["resume", "cv", "curriculum vitae"]
CONTACT_KEYWORDS = ["contact", "email", "e-mail", "mail", "reach you", "get in touch"]
LINKEDIN_KEYWORDS = ["linkedin", "profile link", "professional profile"]


def _build_always_context(db: Session) -> dict:
    """Returns both the text context blob and the raw values needed for actions."""
    parts = []
    values = {"resume_url": None, "contact_email": None, "linkedin_url": None}

    site = db.query(SiteContent).first()
    if site:
        social = site.social_links or {}
        values["contact_email"] = site.contact_email or None

        linkedin_raw = social.get("linkedin")
        if linkedin_raw and not linkedin_raw.startswith("http"):
            linkedin_raw = f"https://{linkedin_raw}"
        values["linkedin_url"] = linkedin_raw or None

        parts.append(
            f"NAME: {site.hero_name}\nTITLE: {site.hero_title}\n"
            f"TAGLINE: {site.hero_tagline}\nABOUT: {site.about_text}"
        )

    resume = db.query(Resume).order_by(Resume.uploaded_at.desc()).first()
    if resume and resume.public_url:
        values["resume_url"] = resume.public_url

    education = db.query(Education).filter(Education.is_visible.is_(True)).all()
    if education:
        edu_lines = [
            f"- Degree: {e.degree}, Institution: {e.institution}, "
            f"Graduation: {e.end_date or 'ongoing'}, Grade/CGPA: {e.grade or 'not specified'}"
            for e in education
        ]
        parts.append("EDUCATION:\n" + "\n".join(edu_lines))
    
    experiences = db.query(Experience).filter(Experience.is_visible.is_(True)).all()
    if experiences:
        exp_lines = [
            f"- Role: {e.role}, Company: {e.company}"
            + (f", Location: {e.location}" if e.location else "")
            + f", Timeline: {e.start_date} to {e.end_date or 'present'}"
            + (f". Description: {e.description}" if e.description else "")
            for e in experiences
        ]
        parts.append("WORK_EXPERIENCE:\n" + "\n".join(exp_lines))

    achievements = db.query(Achievement).filter(Achievement.is_visible.is_(True)).all()
    if achievements:
        ach_lines = [
            f"- {a.type.value.title()}: {a.title}"
            + (f", issued by {a.issuer}" if a.issuer else "")
            + (f", {a.date}" if a.date else "")
            + (f". Description: {a.description}" if a.description else "")
            for a in achievements
        ]
        parts.append("ACHIEVEMENTS_AWARDS_CERTIFICATIONS:\n" + "\n".join(ach_lines))

    projects = db.query(Project).filter(Project.is_visible.is_(True)).all()
    if projects:
        proj_lines = [
            f"{i+1}. {p.title}: {p.summary or p.description or 'no description'} "
            f"(Tech: {', '.join(p.tech_stack or []) or 'not specified'})"
            for i, p in enumerate(projects)
        ]
        parts.append(f"ALL_PROJECTS ({len(projects)} total, numbered):\n" + "\n".join(proj_lines))

        all_tech = sorted({t for p in projects for t in (p.tech_stack or [])})
        if all_tech:
            parts.append("TECH_STACK (from projects): " + ", ".join(all_tech))

    return {"text": "\n\n".join(parts), "values": values}


def _retrieve_context(db: Session, query: str) -> str:
    query_embedding = get_embedding(query)
    results = db.execute(
        select(
            KnowledgeChunk.content,
            KnowledgeChunk.embedding.cosine_distance(query_embedding).label("distance"),
        )
        .order_by("distance")
        .limit(TOP_K)
    ).all()
    relevant = [row.content for row in results if row.distance <= MAX_DISTANCE]
    return "\n\n".join(relevant)


def _detect_actions(user_message: str, values: dict) -> list[ChatAction]:
    """Keyword-based intent detection — deliberately simple and predictable
    rather than asking the LLM to decide, so the UI never gets a button for
    something the user didn't actually ask about."""
    msg = user_message.lower()
    actions = []

    if any(kw in msg for kw in RESUME_KEYWORDS) and values["resume_url"]:
        actions.append(ChatAction(type="resume", url=values["resume_url"], label="Download Resume"))

    if any(kw in msg for kw in CONTACT_KEYWORDS) and values["contact_email"]:
        gmail_compose_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={values['contact_email']}"
        actions.append(ChatAction(type="email", url=gmail_compose_url, label="Send an Email"))

    if any(kw in msg for kw in LINKEDIN_KEYWORDS) and values["linkedin_url"]:
        actions.append(ChatAction(type="linkedin", url=values["linkedin_url"], label="LinkedIn"))

    return actions


FEW_SHOT_EXAMPLES = """\
EXAMPLE 1A
Question: Can I see your resume?
Answer: Sure! You can download my resume using the button below.

EXAMPLE 1B
Question: Tell me about your work experience.
Answer: I worked as [Role] at [Company] from [Timeline]. [Brief summary of what was done, from Description]. Repeat concisely for each entry in WORK_EXPERIENCE if the question asks generally; if asked about a specific role or company, answer only that one.

EXAMPLE 2
Question: Tell me about your education.
Answer: I hold a [Degree] in [Course/Field] from [Institution], graduating in [Year], with a CGPA of [CGPA].

EXAMPLE 3
Question: What's your name?
Answer: Hi, I'm [Name] — Excited to know about me, so go on...

EXAMPLE 4
Question: What tech stacks do you know?
Answer: My core tech stack includes [list from TECH_STACK], which I've used across all projects like and mentioned in resume.

EXAMPLE 5
Question: How can I contact you?
Answer: You can reach me using the options below.

EXAMPLE 6 
Question: What certifications or awards do you have?
Answer: I've earned [list titles only specific one if asked about it or mention all- ACHIEVEMENTS_AWARDS_CERTIFICATIONS, with issuer/numbering for each individual one in different line].

EXAMPLE 7
Question: What's the capital of France?
Answer: This is out of context. Please ask only about my portfolio.

EXAMPLE 8
Question: Tell me about your projects.
Answer: I've worked on projects like: 1) [Title] .new line 2) [Title] . (List every entry in ALL_PROJECTS, numbered, using its own summary — never skip any or merge them into one.)

EXAMPLE 9
Question: Are you a good fit for this role? / Why should we hire you?
Answer: Based on my background, yes — I bring [2-3 specific skills/technologies from TECH_STACK, WORK_EXPERIENCE, or ALL_PROJECTS relevant to typical roles in this field], demonstrated through [reference one concrete project or experience entry]. Happy to elaborate on any part of my background that's most relevant to what you're looking for.

EXAMPLE 10
Question: What are your softskills?
Answer: 1. Team Management (new line) 2. Adaptability (new line) 3. Communication

EXAMPLE 11
Question: What is the best advice you have got in your career?
Answer: There are only stupid answers, not stupid questions!
"""


def get_chat_reply(db: Session, user_message: str) -> tuple[str, bool, list[ChatAction]]:
    """Returns (reply_text, was_fallback, actions)."""
    if not settings.GROQ_API_KEY:
        return (
            "The chatbot isn't configured yet — the site owner needs to add a Groq API key.",
            True,
            [],
        )

    ctx = _build_always_context(db)
    retrieved = _retrieve_context(db, user_message)
    full_context = f"{ctx['text']}\n\n{retrieved}".strip()

    if not full_context:
        return FALLBACK_MESSAGE, True, []

    system_prompt = (
        "You are a strict Q&A assistant on a personal portfolio website. You ONLY "
        "answer questions about the portfolio owner's background, skills, experience, "
        "education, projects, achievements, awards, certifications, resume, and contact details — using ONLY the CONTEXT below.\n\n"
        "Rules, no exceptions:\n"
        "1. If the question is not about the portfolio owner, respond with exactly: "
        f'"{FALLBACK_MESSAGE}"\n'
        "2. If the question IS about the portfolio owner but CONTEXT doesn't contain the "
        f'answer, also respond with exactly: "{FALLBACK_MESSAGE}"\n'
        "3. Never use outside knowledge, even if you know the answer — only the CONTEXT.\n"
        "4. NEVER invent specific facts (years of experience, companies, degrees, "
        "universities, dates, grades) not explicitly present in the CONTEXT.\n"
        "5. Keep answers to 1-3 sentences. Be direct, no filler.\n"
        "6. For 'explain' or 'tell me more about' questions on a specific "
        "achievement/award/certification, use its Description field from "
        "ACHIEVEMENTS_AWARDS_CERTIFICATIONS. If that item has no description "
        "recorded, say the description isn't available rather than repeating "
        "just the title.\n"
        "7. For work experience questions, always include role, company, and "
        "timeline together — never give just one of these without the others. "
        "If asked generally ('tell me about your experience'), summarize each "
        "entry in WORK_EXPERIENCE briefly. If asked about a specific role or "
        "company, answer only that one in more detail using its Description.\n"
        "8. NEVER include raw URLs, email addresses, or markdown links in your answer — "
        "for resume, contact, or LinkedIn questions, just say the info is available/provided "
        "(e.g. 'using the button below') since the actual link is shown separately by the UI.\n"
        "9. If asked whether you're a 'good fit,' 'qualified,' or similar evaluative "
        "questions about suitability for a role, respond confidently and "
        "specifically — cite 2-3 real skills/technologies and at least one "
        "concrete project or experience entry from CONTEXT as evidence. Never "
        "answer with just 'yes' or a vague generality; always back it up with "
        "specifics actually present in CONTEXT.\n\n"
        f"{FEW_SHOT_EXAMPLES}\n"
        f"CONTEXT:\n{full_context}"
    )

    llm = ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.1,
        max_tokens=300,
    )

    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_message)]
    )
    reply = response.content.strip()
    was_fallback = FALLBACK_MESSAGE in reply

    actions = [] if was_fallback else _detect_actions(user_message, ctx["values"])

    return reply, was_fallback, actions