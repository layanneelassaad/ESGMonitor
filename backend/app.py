from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routes import v1_analysis, v1_scores, v1_health


app = FastAPI(title=settings.APP_NAME)


app.add_middleware(
CORSMiddleware,
allow_origins=settings.CORS_ORIGINS,
allow_methods=["*"],
allow_headers=["*"],
)


API = settings.API_PREFIX
app.include_router(v1_health.router, prefix=API)
app.include_router(v1_analysis.router, prefix=API)
app.include_router(v1_scores.router, prefix=API)


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} API. See {API}/docs"}