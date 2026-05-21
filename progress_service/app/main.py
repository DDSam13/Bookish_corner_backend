from fastapi import FastAPI
from sqlalchemy import text

from .db.base import Base
from .db.database import engine

from .models import ReadingProgress
from .routers.progress_router import router as progress_router

app = FastAPI(
    title="Progress & Sync Service",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    with engine.connect() as connection:
        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS progress")
        )
        connection.commit()

    Base.metadata.create_all(bind=engine)


app.include_router(progress_router)


@app.get("/health")
def health():
    return {
        "service": "progress_service",
        "status": "ok",
    }