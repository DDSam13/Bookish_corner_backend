from uuid import UUID

from pydantic import BaseModel, Field


class ProgressCreate(BaseModel):
    user_id: UUID
    book_id: UUID
    progress_type: str = "text"
    current_chapter: str | None = None
    current_position: str | None = None
    percent: float = Field(ge=0, le=100)
    total_pages: int | None = None
    current_page: int | None = None


class ProgressUpdate(BaseModel):
    current_chapter: str | None = None
    current_position: str | None = None
    percent: float | None = Field(default=None, ge=0, le=100)
    total_pages: int | None = None
    current_page: int | None = None
    is_completed: bool | None = None


class ProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    progress_type: str
    current_chapter: str | None
    current_position: str | None
    percent: float
    total_pages: int | None
    current_page: int | None
    is_completed: bool

    class Config:
        from_attributes = True