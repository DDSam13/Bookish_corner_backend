from fastapi import FastAPI
from sqlalchemy import text

from .db.base import Base
from .db.database import engine

from .models import Book, Author, Genre, UserBook

from .routers.book_router import router as book_router

app = FastAPI(
    title="Library Service",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    with engine.connect() as connection:
        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS library")
        )
        connection.commit()

    Base.metadata.create_all(bind=engine)


app.include_router(book_router)


@app.get("/health")
def health():
    return {
        "service": "library_service",
        "status": "ok",
    }