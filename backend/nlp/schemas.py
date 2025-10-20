from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class AnalyzeTextIn(BaseModel):
    text: str


class AnalyzeTextOut(BaseModel):
    summary: str
    topics: Dict
    sentiment: Dict
    e_score: float
    s_score: float
    g_score: float
    total_score: float
    contributions: Dict
    branches: Dict[str, str]
    contributions: Dict


class UploadOut(BaseModel):
    document_id: int
    result: AnalyzeTextOut


class ScoreOut(BaseModel):
    document_id: int
    e_score: float
    s_score: float
    g_score: float
    total_score: float
    contributions: Dict