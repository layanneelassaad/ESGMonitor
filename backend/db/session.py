from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import settings


DB_URL = (
f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}"
f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)


engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)