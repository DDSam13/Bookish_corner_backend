import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID

from ..db.base import Base


class ReadingGoal(Base):
    __tablename__ = "reading_goals"
    __table_args__ = {"schema": "tracker"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), nullable=False)

    year = Column(Integer, nullable=False)
    target_books_count = Column(Integer, nullable=False)
    completed_books_count = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)