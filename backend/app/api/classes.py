from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DBSession

from app.db.session import get_db
from app.models.core import Class, Student, Volunteer
from app.schemas.schemas import ClassAnalysisResponse, ClassCreate, ClassResponse
from app.services.class_analysis import analyze_class

router = APIRouter()


def _to_response(klass: Class, student_count: int) -> ClassResponse:
    resp = ClassResponse.model_validate(klass)
    resp.student_count = student_count
    return resp


@router.get("/classes", response_model=list[ClassResponse])
def list_classes(db: DBSession = Depends(get_db)):
    counts = dict(
        db.query(Student.class_id, func.count(Student.id)).group_by(Student.class_id).all()
    )
    classes = db.query(Class).order_by(Class.id).all()
    return [_to_response(c, counts.get(c.id, 0)) for c in classes]


@router.post("/classes", response_model=ClassResponse, status_code=201)
def create_class(payload: ClassCreate, db: DBSession = Depends(get_db)):
    if payload.volunteer_id is not None and not db.get(Volunteer, payload.volunteer_id):
        raise HTTPException(status_code=404, detail="Volunteer not found")
    klass = Class(**payload.model_dump())
    db.add(klass)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="A class with this code already exists"
        ) from None
    db.refresh(klass)
    return _to_response(klass, 0)


@router.get("/classes/{class_id}/analysis", response_model=ClassAnalysisResponse)
def get_class_analysis(class_id: int, db: DBSession = Depends(get_db)):
    if not db.get(Class, class_id):
        raise HTTPException(status_code=404, detail="Class not found")
    return analyze_class(db, class_id)
