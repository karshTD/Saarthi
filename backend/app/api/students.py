from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DBSession

from app.db.session import get_db
from app.models.core import Class, Student
from app.schemas.schemas import StudentCreate, StudentResponse

router = APIRouter()


@router.post("/students", response_model=StudentResponse, status_code=201)
def create_student(payload: StudentCreate, db: DBSession = Depends(get_db)):
    if not db.get(Class, payload.class_id):
        raise HTTPException(status_code=404, detail="Class not found")
    student = Student(**payload.model_dump())
    db.add(student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="This student code already exists in the class"
        ) from None
    db.refresh(student)
    return student
