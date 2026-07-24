import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.core.config import settings
from app.core.limiter import limiter
from app.api.routes import (
    auth,
    experience,
    project,
    education,
    achievement,
    site_content,
    resume,
    chatbot,
    faq,
    admin_users,
    admin_reindex,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("portfolio_api")

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0", docs_url=None, redoc_url=None)

# --- Rate limiting (protects /auth/login and /chatbot from abuse) ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS: only allow the configured frontend origin(s) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


PREFIX = settings.API_V1_PREFIX
app.include_router(auth.router, prefix=PREFIX)
app.include_router(experience.router, prefix=PREFIX)
app.include_router(project.router, prefix=PREFIX)
app.include_router(education.router, prefix=PREFIX)
app.include_router(achievement.router, prefix=PREFIX)
app.include_router(site_content.router, prefix=PREFIX)
app.include_router(resume.router, prefix=PREFIX)
app.include_router(chatbot.router, prefix=PREFIX)
app.include_router(faq.router, prefix=PREFIX)
app.include_router(admin_users.router, prefix=PREFIX)
app.include_router(admin_reindex.router, prefix=PREFIX)