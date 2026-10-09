from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.db.session import get_db
from app.models.core import Student
from app.models.sessions import Activity, Assessment
from app.schemas.schemas import AssessmentCreate, AssessmentResponse

router = APIRouter()


@router.post("/assessments", response_model=AssessmentResponse, status_code=201)
def create_assessment(payload: AssessmentCreate, db: DBSession = Depends(get_db)):
    student = db.get(Student, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    activity = db.get(Activity, payload.activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if student.class_id != activity.session.class_id:
        raise HTTPException(
            status_code=422, detail="Student does not belong to this activity's class"
        )

    assessment = Assessment(**payload.model_dump())
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment
