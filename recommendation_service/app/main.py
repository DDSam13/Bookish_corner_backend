from fastapi import FastAPI
from sqlalchemy import text

from .db.base import Base
from .db.database import engine
from .models import RecommendationCache, LLMRequest
from .routers.recommendation_router import router as recommendation_router

app = FastAPI(
    title="Recommendation Service",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS recommendations"))
        connection.commit()

    Base.metadata.create_all(bind=engine)


app.include_router(recommendation_router)


@app.get("/health")
def health():
    return {
        "service": "recommendation_service",
        "status": "ok",
    }