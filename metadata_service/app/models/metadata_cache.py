import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..db.base import Base


class MetadataCache(Base):
    __tablename__ = "metadata_cache"
    __table_args__ = {"schema": "metadata"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    query = Column(String(500), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    author = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    cover_url = Column(Text, nullable=True)
    language = Column(String(30), nullable=True)
    page_count = Column(String(30), nullable=True)

    raw_data = Column(JSONB, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)