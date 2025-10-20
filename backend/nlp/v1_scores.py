from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.db.models import ESGScore
from backend.schemas import ScoreOut


router = APIRouter(prefix="/scores", tags=["scores"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{document_id}", response_model=ScoreOut)
def get_score(document_id: int, db: Session = Depends(get_db)):
    row = db.query(ESGScore).filter(ESGScore.document_id == document_id).order_by(ESGScore.created_at.desc()).first()
    if not row:
        raise HTTPException(status_code=404, detail="No score for document")
    return ScoreOut(
        document_id=document_id,
        e_score=row.e_score, s_score=row.s_score, g_score=row.g_score,
        total_score=row.total_score, contributions=row.contributions,
    )