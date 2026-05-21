from fastapi import FastAPI
from sqlalchemy import text

from .db.database import engine
from .db.base import Base
from .models import User, Session, RefreshToken
from .routers.auth_router import router as auth_router

app = FastAPI(title="Auth Service", version="1.0.0")


@app.on_event("startup")
def startup():
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS auth"))
        connection.commit()

    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"service": "auth_service", "status": "ok"}
