from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import assessments, classes, health, students
from app.api import sessions as sessions_api
from app.core.config import settings
from app.core.security import require_access_code
from app.models import core, sessions  # noqa: F401 - ensures models are registered with Base

app = FastAPI(title="Saarthi API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health stays open for platform health checks; everything else needs the access code (if set).
app.include_router(health.router, prefix="/api", tags=["health"])
protected = [Depends(require_access_code)]
app.include_router(classes.router, prefix="/api", tags=["classes"], dependencies=protected)
app.include_router(students.router, prefix="/api", tags=["students"], dependencies=protected)
app.include_router(sessions_api.router, prefix="/api", tags=["sessions"], dependencies=protected)
app.include_router(assessments.router, prefix="/api", tags=["assessments"], dependencies=protected)


@app.get("/")
def root():
    return {"message": "Saarthi API is running"}
