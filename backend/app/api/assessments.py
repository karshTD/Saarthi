from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from app.db.session import get_db
from app.models.sessions import Assessment
from app.schemas.schemas import AssessmentCreate, AssessmentResponse

router = APIRouter()


@router.post("/assessments", response_model=AssessmentResponse)
def create_assessment(payload: AssessmentCreate, db: DBSession = Depends(get_db)):
    assessment = Assessment(**payload.model_dump())
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment
