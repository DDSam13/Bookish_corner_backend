import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from ..db.base import Base


class UserBook(Base):
    __tablename__ = "user_books"
    __table_args__ = {"schema": "library"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), nullable=False)

    book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("library.books.id"),
        nullable=False,
    )

    is_favorite = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)