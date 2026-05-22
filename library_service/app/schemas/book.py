from uuid import UUID

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    description: str | None = None
    cover_url: str | None = None
    page_count: int | None = None
    language: str | None = None

    author_name: str
    genre_name: str

class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    cover_url: str | None = None
    page_count: int | None = None
    language: str | None = None

    author_name: str | None = None
    genre_name: str | None = None

class BookResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    cover_url: str | None
    page_count: int | None
    language: str | None
    author_name: str | None = None
    genre_name: str | None = None

    class Config:
        from_attributes = True