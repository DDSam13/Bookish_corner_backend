import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from ..db.base import Base


class LLMRequest(Base):
    __tablename__ = "llm_requests"
    __table_args__ = {"schema": "recommendations"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    provider = Column(String(50), nullable=False, default="gigachat")
    model = Column(String(100), nullable=False)

    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=True)

    status = Column(String(50), nullable=False, default="success")
    error_message = Column(Text, nullable=True)

    tokens_used = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)