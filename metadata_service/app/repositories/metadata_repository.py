from sqlalchemy.orm import Session

from ..models.metadata_cache import MetadataCache


class MetadataRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_query(self, query: str):
        return (
            self.db.query(MetadataCache)
            .filter(MetadataCache.query == query)
            .first()
        )

    def save_metadata(self, query: str, data: dict):
        cache = MetadataCache(
            query=query,
            title=data.get("title"),
            author=data.get("author"),
            description=data.get("description"),
            cover_url=data.get("cover_url"),
            language=data.get("language"),
            page_count=str(data.get("page_count")) if data.get("page_count") else None,
            raw_data=data.get("raw_data"),
        )

        self.db.add(cache)
        self.db.commit()
        self.db.refresh(cache)

        return cache