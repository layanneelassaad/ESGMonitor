from sqlalchemy.orm import Session
from .models import Document, ESGScore


def create_document(db: Session, filename: str, content: str) -> Document:
    doc = Document(filename=filename, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def save_score(db: Session, document_id: int, e: float, s: float, g: float, total: float, contrib: dict) -> ESGScore:
    rec = ESGScore(
        document_id=document_id,
        e_score=e, s_score=s, g_score=g,
        total_score=total, contributions=contrib,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec