from app.crud.base import CRUDBase
from app.models.experience import Experience
from app.models.project import Project
from app.models.education import Education
from app.models.achievement import Achievement
from app.models.chatbot import FaqEntry
from app.schemas.experience import ExperienceCreate, ExperienceUpdate
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.education import EducationCreate, EducationUpdate
from app.schemas.achievement import AchievementCreate, AchievementUpdate
from app.schemas.chatbot import FaqCreate, FaqUpdate

experience_crud = CRUDBase[Experience, ExperienceCreate, ExperienceUpdate](Experience)
project_crud = CRUDBase[Project, ProjectCreate, ProjectUpdate](Project)
education_crud = CRUDBase[Education, EducationCreate, EducationUpdate](Education)
achievement_crud = CRUDBase[Achievement, AchievementCreate, AchievementUpdate](Achievement)
faq_crud = CRUDBase[FaqEntry, FaqCreate, FaqUpdate](FaqEntry)
