from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer, DateTime, JSON, Text


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(256), index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ESGScore(Base):
    __tablename__ = "esg_scores"
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(index=True)
    e_score: Mapped[float] = mapped_column(Float)
    s_score: Mapped[float] = mapped_column(Float)
    g_score: Mapped[float] = mapped_column(Float)
    total_score: Mapped[float] = mapped_column(Float, index=True)
    contributions: Mapped[dict] = mapped_column(JSON) # feature -> weight
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)