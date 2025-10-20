from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    API_PREFIX: str = "/api/v1"
    APP_NAME: str = "ESG Monitor"


    # DB
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "esg"
    DB_PASSWORD: str = "esg"
    DB_NAME: str = "esg_monitor"


    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


    # Inference limits
    MAX_UPLOAD_MB: int = 20
    MAX_TOKENS: int = 6000


class Config:
    env_file = ".env"


settings = Settings()