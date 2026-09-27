from datetime import datetime
from pydantic import BaseModel


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


class SessionCreate(BaseModel):
    class_id: int
    subject: str
    topic: str
    language: str = "en"
    duration_minutes: int


class SessionResponse(BaseModel):
    id: int
    class_id: int
    subject: str
    topic: str
    language: str
    duration_minutes: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityResponse(BaseModel):
    id: int
    session_id: int
    title: str
    difficulty_level: str
    content: dict
    order_index: int

    class Config:
        from_attributes = True


class LessonGenerateResponse(BaseModel):
    session: SessionResponse
    activities: list[ActivityResponse]
    generated_by: str
    ai_error: str | None = None


class AssessmentCreate(BaseModel):
    activity_id: int
    student_id: int
    score: float
    time_taken_seconds: int
    attempt_count: int = 1


class AssessmentResponse(BaseModel):
    id: int
    activity_id: int
    student_id: int
    score: float
    time_taken_seconds: int
    attempt_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    session_id: int
    topic: str
    recommendation: str
    generated_by: str
    ai_error: str | None = None
    analysis: ClassAnalysisResponse
