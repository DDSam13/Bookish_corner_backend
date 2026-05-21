from fastapi import FastAPI
from sqlalchemy import text

from .db.base import Base
from .db.database import engine
from .models import ReadingGoal, ReadingSession
from .routers.tracker_router import router as tracker_router

app = FastAPI(
    title="Tracker Service",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS tracker"))
        connection.commit()

    Base.metadata.create_all(bind=engine)


app.include_router(tracker_router)


@app.get("/health")
def health():
    return {
        "service": "tracker_service",
        "status": "ok",
    }