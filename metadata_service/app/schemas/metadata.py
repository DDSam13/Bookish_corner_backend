from uuid import UUID

from pydantic import BaseModel


class MetadataRequest(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None


class MetadataResponse(BaseModel):
    id: UUID | None = None
    title: str | None = None
    author: str | None = None
    description: str | None = None
    cover_url: str | None = None
    language: str | None = None
    page_count: int | None = None
    source: str = "google_books"