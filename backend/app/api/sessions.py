from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DBSession

from app.ai.lesson_generator import generate_lesson
from app.ai.recommender import generate_recommendation
from app.core.security import rate_limit_ai
from app.db.session import get_db
from app.models.core import Class
from app.models.sessions import Activity, Assessment, AssessmentItem
from app.models.sessions import Session as SessionModel
from app.schemas.lesson import LessonPlan
from app.schemas.schemas import (
    ActivityResponse,
    LessonGenerateResponse,
    RecommendationResponse,
    SessionCreate,
    SessionResponse,
)
from app.services.class_analysis import analyze_class

router = APIRouter()


def _get_session_or_404(db: DBSession, session_id: int) -> SessionModel:
    session = db.get(SessionModel, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


def _stored_plan(session: SessionModel) -> LessonPlan | None:
    if not session.lesson_plan:
        return None
    try:
        return LessonPlan.model_validate(session.lesson_plan)
    except ValueError:
        return None


def _reused_response(session: SessionModel, activities: list[Activity]) -> LessonGenerateResponse:
    origin = (activities[0].content or {}).get("generated_by", "seed") if activities else "seed"
    return LessonGenerateResponse(
        session=session,
        activities=activities,
        plan=_stored_plan(session),
        generated_by=origin,
        reused=True,
    )


@router.post("/sessions", response_model=SessionResponse, status_code=201)
def create_session(payload: SessionCreate, db: DBSession = Depends(get_db)):
    if not db.get(Class, payload.class_id):
        raise HTTPException(status_code=404, detail="Class not found")
    session = SessionModel(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions", response_model=list[SessionResponse])
def list_sessions(class_id: int | None = None, db: DBSession = Depends(get_db)):
    query = db.query(SessionModel)
    if class_id is not None:
        query = query.filter(SessionModel.class_id == class_id)
    return query.order_by(SessionModel.id.desc()).all()


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: DBSession = Depends(get_db)):
    return _get_session_or_404(db, session_id)


@router.get("/sessions/{session_id}/activities", response_model=list[ActivityResponse])
def list_activities(session_id: int, db: DBSession = Depends(get_db)):
    return _get_session_or_404(db, session_id).activities


@router.post(
    "/sessions/{session_id}/generate-lesson",
    response_model=LessonGenerateResponse,
    dependencies=[Depends(rate_limit_ai)],
)
def generate_session_lesson(
    session_id: int, regenerate: bool = False, db: DBSession = Depends(get_db)
):
    """Idempotent: if the session already has activities they are returned (reused=true).

    Pass ?regenerate=true to replace them; this is refused (409) once any assessment
    has been recorded against them, so collected data is never silently destroyed.
    """
    session = _get_session_or_404(db, session_id)
    existing = list(session.activities)

    if existing and not regenerate:
        return _reused_response(session, existing)

    if existing:
        activity_ids = [a.id for a in existing]
        has_data = (
            db.query(Assessment.id).filter(Assessment.activity_id.in_(activity_ids)).first()
            or db.query(AssessmentItem.id)
            .filter(AssessmentItem.activity_id.in_(activity_ids))
            .first()
        )
        if has_data:
            raise HTTPException(
                status_code=409,
                detail="Assessments already recorded for this lesson; it can't be regenerated.",
            )
        for activity in existing:
            db.delete(activity)
        db.flush()

    result = generate_lesson(
        session.subject, session.topic, session.duration_minutes, session.language or "en"
    )
    plan: LessonPlan = result["plan"]

    new_activities = [
        Activity(
            session_id=session.id,
            title=a.title,
            difficulty_level=a.level,
            content={**a.model_dump(), "generated_by": result["generated_by"]},
            order_index=i,
        )
        for i, a in enumerate(plan.activities)
    ]
    db.add_all(new_activities)
    session.lesson_plan = plan.model_dump()

    try:
        db.commit()
    except IntegrityError:
        # A concurrent request generated this lesson first; return theirs instead of duplicating.
        db.rollback()
        db.expire_all()
        session = _get_session_or_404(db, session_id)
        return _reused_response(session, list(session.activities))

    db.refresh(session)
    return LessonGenerateResponse(
        session=session,
        activities=list(session.activities),
        plan=plan,
        generated_by=result["generated_by"],
        ai_error=result["ai_error"],
    )


@router.post(
    "/sessions/{session_id}/recommendation",
    response_model=RecommendationResponse,
    dependencies=[Depends(rate_limit_ai)],
)
def get_session_recommendation(session_id: int, db: DBSession = Depends(get_db)):
    session = _get_session_or_404(db, session_id)
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
