from fastapi import FastAPI
from sqlalchemy import text

from .db.base import Base
from .db.database import engine
from .models import MetadataCache
from .routers.metadata_router import router as metadata_router

app = FastAPI(
    title="Metadata Service",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS metadata"))
        connection.commit()

    Base.metadata.create_all(bind=engine)


app.include_router(metadata_router)


@app.get("/health")
def health():
    return {
        "service": "metadata_service",
        "status": "ok",
    }