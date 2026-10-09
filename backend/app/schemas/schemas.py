from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.schemas.lesson import LessonPlan

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
OptText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
LANG_PATTERN = r"^[a-z]{2,3}(-[A-Za-z]{2,4})?$"
LEVEL_PATTERN = r"^(struggling|on_track|advanced|unassessed)$"


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---- analysis ----
class StudentAnalysis(BaseModel):
    student_id: int
    name: str
    avg_score: float | None
    level: str


class ClassAnalysisResponse(BaseModel):
    class_id: int
    student_count: int
    level_counts: dict[str, int]
    students: list[StudentAnalysis]


# ---- classes & students ----
class ClassCreate(BaseModel):
    name: Text
    code: OptText | None = None
    grade: OptText | None = None
    location: OptText | None = None
    volunteer_id: int | None = Field(default=None, gt=0)


class ClassResponse(ORMModel):
    id: int
    name: str
    code: str | None
    grade: str | None
    location: str | None
    volunteer_id: int | None
    student_count: int = 0


class StudentCreate(BaseModel):
    name: Text
    class_id: int = Field(gt=0)
    student_code: OptText | None = None
    age: int | None = Field(default=None, ge=3, le=25)
    home_language: OptText | None = None
    level: str = Field(default="unassessed", pattern=LEVEL_PATTERN)


class StudentResponse(ORMModel):
    id: int
    name: str
    student_code: str | None
    class_id: int
    level: str
    age: int | None
    home_language: str | None


# ---- sessions ----
class SessionCreate(BaseModel):
    class_id: int = Field(gt=0)
    subject: Text
    topic: Text
    language: str = Field(default="en", pattern=LANG_PATTERN)
    duration_minutes: int = Field(ge=10, le=180)
    session_date: date | None = None


class SessionResponse(ORMModel):
    id: int
    code: str | None = None
    class_id: int
    subject: str
    topic: str
    language: str
    duration_minutes: int
    status: str
    session_date: date | None = None
    lesson_plan: dict | None = None
    created_at: datetime


class ActivityResponse(ORMModel):
    id: int
    session_id: int
    title: str
    difficulty_level: str
    content: dict
    order_index: int


class LessonGenerateResponse(BaseModel):
    session: SessionResponse
    activities: list[ActivityResponse]
    plan: LessonPlan | None = None
    generated_by: str
    reused: bool = False  # True when existing activities were returned instead of regenerated
    ai_error: str | None = None


# ---- assessments ----
class AssessmentCreate(BaseModel):
    activity_id: int = Field(gt=0)
    student_id: int = Field(gt=0)
    score: float = Field(ge=0.0, le=1.0)
    time_taken_seconds: int = Field(ge=0, le=7200)
    attempt_count: int = Field(default=1, ge=1, le=20)


class AssessmentResponse(ORMModel):
    id: int
    activity_id: int
    student_id: int
    score: float
    time_taken_seconds: int
    attempt_count: int
    created_at: datetime


class RecommendationResponse(BaseModel):
    session_id: int
    topic: str
    recommendation: str
    generated_by: str
    ai_error: str | None = None
    analysis: ClassAnalysisResponse
