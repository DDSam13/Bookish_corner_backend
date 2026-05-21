import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.base import Base


class Author(Base):
    __tablename__ = "authors"
    __table_args__ = {"schema": "library"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False)

    books = relationship("Book", back_populates="author")


class Genre(Base):
    __tablename__ = "genres"
    __table_args__ = {"schema": "library"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(100), nullable=False)

    books = relationship("Book", back_populates="genre")


class Book(Base):
    __tablename__ = "books"
    __table_args__ = {"schema": "library"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String(255), nullable=False)

    description = Column(Text, nullable=True)

    cover_url = Column(Text, nullable=True)

    page_count = Column(Integer, nullable=True)

    language = Column(String(30), nullable=True)

    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("library.authors.id"),
    )

    genre_id = Column(
        UUID(as_uuid=True),
        ForeignKey("library.genres.id"),
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("Author", back_populates="books")

    genre = relationship("Genre", back_populates="books")