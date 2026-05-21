import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID

from ..db.base import Base


class ReadingSession(Base):
    __tablename__ = "reading_sessions"
    __table_args__ = {"schema": "tracker"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), nullable=False)
    book_id = Column(UUID(as_uuid=True), nullable=False)

    duration_minutes = Column(Integer, nullable=False, default=0)
    pages_read = Column(Integer, nullable=True)

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)