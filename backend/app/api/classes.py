from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from app.db.session import get_db
from app.services.class_analysis import analyze_class
from app.schemas.schemas import ClassAnalysisResponse

router = APIRouter()


@router.get("/classes/{class_id}/analysis", response_model=ClassAnalysisResponse)
def get_class_analysis(class_id: int, db: DBSession = Depends(get_db)):
    return analyze_class(db, class_id)
