portfolio-app/
├── backend/
│   ├── app/
│   │   ├── main.py                          # FastAPI entrypoint, CORS, routers
│   │   │
│   │   ├── core/
│   │   │   ├── config.py                    # Settings (.env values) — now includes GROQ_API_KEY/GROQ_MODEL
│   │   │   ├── security.py                  # Password hashing, JWT create/decode
│   │   │   └── limiter.py                   # Rate limiting (slowapi)
│   │   │
│   │   ├── db/
│   │   │   └── session.py                   # SQLAlchemy engine, session, Base
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py                  # Imports all models for Base.metadata
│   │   │   ├── user.py                      # Admin/editor accounts
│   │   │   ├── experience.py
│   │   │   ├── project.py
│   │   │   ├── education.py                 # Replaced "qualification"
│   │   │   ├── achievement.py                # Replaced "qualification"
│   │   │   ├── site_content.py               # Hero/about/contact/social links
│   │   │   ├── resume.py
│   │   │   ├── chatbot.py                    # FaqEntry, ChatLog
│   │   │   └── knowledge_chunk.py            # RAG: text chunk + embedding vector
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── experience.py
│   │   │   ├── project.py
│   │   │   ├── education.py
│   │   │   ├── achievement.py
│   │   │   ├── site_content.py
│   │   │   ├── resume.py
│   │   │   └── chatbot.py                    # ChatRequest/Response, ChatAction, FAQ schemas
│   │   │
│   │   ├── crud/
│   │   │   ├── base.py                       # Generic CRUD class
│   │   │   └── resources.py                  # CRUD instances per resource
│   │   │
│   │   ├── api/
│   │   │   ├── deps.py                       # get_current_user, role checks
│   │   │   └── routes/
│   │   │       ├── auth.py
│   │   │       ├── experience.py
│   │   │       ├── project.py
│   │   │       ├── education.py
│   │   │       ├── achievement.py
│   │   │       ├── site_content.py
│   │   │       ├── resume.py
│   │   │       ├── chatbot.py                # /chatbot/message
│   │   │       ├── faq.py
│   │   │       ├── admin_users.py
│   │   │       └── admin_reindex.py          # /admin/reindex — rebuilds knowledge_chunks
│   │   │
│   │   └── services/
│   │       ├── storage.py                    # Resume upload (local or S3)
│   │       ├── embeddings.py                 # sentence-transformers (local, free)
│   │       ├── indexer.py                    # Builds knowledge_chunks for RAG
│   │       └── chatbot.py                    # RAG retrieval + Groq LLM + few-shot prompt + action detection
│   │
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── 0001_initial_schema.py
│   │       ├── 0002_education_achievements.py   # Dropped qualifications, added education/achievements
│   │       ├── 0003_pgvector_knowledge_chunks.py # Enabled pgvector, created knowledge_chunks
│   │       └── 0004_reduce_embedding_dim.py      # 1536 → 384 dims (switch to local embeddings)
│   │
│   ├── scripts/
│   │   └── create_admin.py                   # One-time admin bootstrap
│   │
│   ├── tests/
│   │   └── test_health.py
│   │
│   ├── requirements.txt                       # Now includes pgvector, sentence-transformers, langchain-groq
│   ├── alembic.ini
│   ├── Dockerfile
│   └── .env / .env.example
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx                            # Routes — /admin/education, /admin/achievements, etc.
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx                       # Renders all public sections
│   │   │   └── admin/
│   │   │       ├── Login.jsx
│   │   │       ├── Dashboard.jsx              # Includes "Reindex Knowledge Base" button
│   │   │       ├── Experiences.jsx
│   │   │       ├── Projects.jsx
│   │   │       ├── Education.jsx              # Replaced Qualifications.jsx
│   │   │       ├── Achievements.jsx           # Replaced Qualifications.jsx
│   │   │       ├── SiteContentEditor.jsx
│   │   │       ├── ResumeManager.jsx
│   │   │       └── Faqs.jsx
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.jsx                     # No dark/light toggle now
│   │   │   ├── Hero.jsx
│   │   │   ├── About.jsx                      # Added — renders about_text
│   │   │   ├── Experience.jsx
│   │   │   ├── Projects.jsx
│   │   │   ├── Education.jsx                  # Replaced Qualifications.jsx
│   │   │   ├── Achievements.jsx                # Replaced Qualifications.jsx
│   │   │   ├── ResumeSection.jsx
│   │   │   ├── Contact.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── ChatbotWidget.jsx              # Renders action buttons (resume/email/linkedin)
│   │   │   ├── AdminLayout.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── api/
│   │   │   ├── client.js                      # Axios instance, JWT interceptor
│   │   │   └── resources.js                   # All API call functions, incl. triggerReindex
│   │   │
│   │   └── styles/
│   │       └── index.css                       # signal-line now display:none
│   │
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── vercel.json
│   └── .env / .env.example
│
├── docker-compose.yml                          # Now uses pgvector/pgvector:pg16
├── .gitignore
├── README.md
└── .github/workflows/
    ├── ci.yml
    └── deploy.yml