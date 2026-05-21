from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class ReadingGoalCreate(BaseModel):
    user_id: UUID
    year: int
    books_target: int
    books_completed: int = 0


class ReadingGoalUpdate(BaseModel):
    books_target: int | None = None
    books_completed: int | None = None


class ReadingGoalResponse(BaseModel):
    id: UUID
    user_id: UUID
    year: int
    books_target: int
    books_completed: int

    class Config:
        from_attributes = True


class ReadingSessionCreate(BaseModel):
    user_id: UUID
    book_id: UUID
    duration_minutes: int
    pages_read: int | None = None


class ReadingSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    duration_minutes: int
    pages_read: int | None
    started_at: datetime
    finished_at: datetime | None

    class Config:
        from_attributes = True