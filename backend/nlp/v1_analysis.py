from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import chardet, pdfplumber
from backend.schemas import AnalyzeTextIn, AnalyzeTextOut, UploadOut
from backend.db.session import SessionLocal
from backend.db import crud
from backend.nlp.analysis import summarize_long, classify_esg_topics, analyze_sentiment, branch_summaries
from backend.nlp.scoring import compute_scores


router = APIRouter(prefix="/analysis", tags=["analysis"])




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def _extract_text(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        with open("/tmp/_doc.pdf", "wb") as f:
            f.write(file_bytes)
        with pdfplumber.open("/tmp/_doc.pdf") as pdf:
            return "".join(page.extract_text() or "" for page in pdf.pages)
    else:
        enc = chardet.detect(file_bytes).get("encoding", "utf-8")
        return file_bytes.decode(enc, errors="replace")




@router.post("/text", response_model=AnalyzeTextOut)
def analyze_text(payload: AnalyzeTextIn):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")

    summary = summarize_long(text)
    topics = classify_esg_topics(text)
    sent = analyze_sentiment(text)
    e, s, g, total, contrib = compute_scores(topics, sent["pos_score"])
    branches = branch_summaries(text)

    return AnalyzeTextOut(
        summary=summary, topics=topics, sentiment=sent,
        e_score=e, s_score=s, g_score=g, total_score=total,
        contributions=contrib, branches=branches,
    )




@router.post("/upload", response_model=UploadOut)
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = await file.read()
    text = _extract_text(data, file.filename)
    if not text.strip():
        raise HTTPException(status_code=400, detail="File empty or unreadable")

    doc = crud.create_document(db, filename=file.filename, content=text)
    res: AnalyzeTextOut = analyze_text(AnalyzeTextIn(text=text))  # reuse logic

    return UploadOut(document_id=doc.id, result=res)