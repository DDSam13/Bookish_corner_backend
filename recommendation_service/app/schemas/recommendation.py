from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class RecommendationMode(str, Enum):
    SAME_GENRE = "same_genre"
    AUTHOR_STYLE = "author_style"
    PLOT_ATMOSPHERE = "plot_atmosphere"


class SourceBook(BaseModel):
    title: str
    author: str | None = None
    genre: str | None = None
    description: str | None = None


class RecommendationRequest(BaseModel):
    user_id: UUID
    source_book: SourceBook
    mode: RecommendationMode
    count: int = Field(default=5, ge=1, le=10)


class RecommendedBook(BaseModel):
    title: str
    author: str
    reason: str
    similarity_type: str
    confidence: float = Field(ge=0, le=1)
    search_query: str


class RecommendationResponse(BaseModel):
    source_book: SourceBook
    mode: RecommendationMode
    recommendations: list[RecommendedBook]