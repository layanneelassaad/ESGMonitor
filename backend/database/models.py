from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database.database_config import Base

class ESGScore(Base):
    __tablename__ = "esg_scores"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    esg_score = Column(Float)
    sentiment_score = Column(Float)
    benchmark_score = Column(Float)
    violations = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
