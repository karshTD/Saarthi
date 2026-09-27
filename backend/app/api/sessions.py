from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.db.session import get_db
from app.models.sessions import Session as SessionModel, Activity
from app.services.class_analysis import analyze_class
from app.ai.lesson_generator import generate_lesson
from app.ai.recommender import generate_recommendation
from app.schemas.schemas import (
    SessionCreate,
    SessionResponse,
    LessonGenerateResponse,
    RecommendationResponse,
)

router = APIRouter()


@router.post("/sessions", response_model=SessionResponse)
def create_session(payload: SessionCreate, db: DBSession = Depends(get_db)):
    session = SessionModel(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: DBSession = Depends(get_db)):
    session = db.get(SessionModel, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/sessions/{session_id}/generate-lesson", response_model=LessonGenerateResponse)
def generate_session_lesson(session_id: int, db: DBSession = Depends(get_db)):
    session = db.get(SessionModel, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = generate_lesson(session.subject, session.topic)

    activities = []
    for i, activity_data in enumerate(result["activities"]):
        activity = Activity(
            session_id=session.id,
            title=activity_data["title"],
            difficulty_level=activity_data["level"],
            content=activity_data,
            order_index=i,
        )
        db.add(activity)
        activities.append(activity)

    db.commit()
    for a in activities:
        db.refresh(a)

    return LessonGenerateResponse(
        session=session,
        activities=activities,
        generated_by=result["generated_by"],
        ai_error=result.get("ai_error"),
    )


@router.post("/sessions/{session_id}/recommendation", response_model=RecommendationResponse)
def get_session_recommendation(session_id: int, db: DBSession = Depends(get_db)):
    session = db.get(SessionModel, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    analysis = analyze_class(db, session.class_id)
    result = generate_recommendation(analysis, session.topic)

    return RecommendationResponse(
        session_id=session.id,
        topic=session.topic,
        recommendation=result["recommendation"],
        generated_by=result["generated_by"],
        ai_error=result.get("ai_error"),
        analysis=analysis,
    )
