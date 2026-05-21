import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..db.base import Base


class RecommendationCache(Base):
    __tablename__ = "recommendation_cache"
    __table_args__ = {"schema": "recommendations"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), nullable=False)

    source_title = Column(String(255), nullable=False)
    source_author = Column(String(255), nullable=True)
    mode = Column(String(50), nullable=False)

    prompt = Column(Text, nullable=False)
    recommendations = Column(JSONB, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)