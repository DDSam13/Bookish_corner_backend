import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from ..db.base import Base


class ReadingProgress(Base):
    __tablename__ = "reading_progress"
    __table_args__ = {"schema": "progress"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), nullable=False)
    book_id = Column(UUID(as_uuid=True), nullable=False)

    progress_type = Column(String(20), nullable=False, default="text")
    current_chapter = Column(String(255), nullable=True)
    current_position = Column(String(255), nullable=True)

    percent = Column(Float, nullable=False, default=0.0)
    total_pages = Column(Integer, nullable=True)
    current_page = Column(Integer, nullable=True)

    is_completed = Column(Boolean, nullable=False, default=False)

    last_opened_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)