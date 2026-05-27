from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repositories.metadata_repository import MetadataRepository
from ..schemas.metadata import MetadataRequest, MetadataResponse
from .google_books_service import GoogleBooksService
from .open_library_service import OpenLibraryService


class MetadataService:
    def __init__(self, db: Session):
        self.repository = MetadataRepository(db)
        self.google_books = GoogleBooksService()
        self.open_library = OpenLibraryService()

    def _build_query(self, data: MetadataRequest):
        return f"title={data.title};author={data.author};isbn={data.isbn}"

    async def enrich_book(self, data: MetadataRequest):
        query = self._build_query(data)

        cached = self.repository.get_by_query(query)

        if cached:
            return MetadataResponse(
                id=cached.id,
                title=cached.title,
                author=cached.author,
                description=cached.description,
                cover_url=cached.cover_url,
                language=cached.language,
                page_count=int(cached.page_count) if cached.page_count else None,
                source="metadata_cache",
            )

        metadata = await self.google_books.search_book(
            title=data.title,
            author=data.author,
            isbn=data.isbn,
        )

        open_library_metadata = None

        if (
                not metadata
                or not metadata.get("description")
                or len(metadata.get("description") or "") < 120
                or not metadata.get("cover_url")
        ):
            open_library_metadata = await self.open_library.search_book(
                title=data.title,
                author=data.author,
            )

        open_library_metadata = None

        if (
                not metadata
                or not metadata.get("description")
                or len(metadata.get("description") or "") < 120
                or not metadata.get("cover_url")
        ):
            open_library_metadata = await self.open_library.search_book(
                title=data.title,
                author=data.author,
            )

        if not metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Метаданные книги не найдены",
            )

        saved = self.repository.save_metadata(query, metadata)

        return MetadataResponse(
            id=saved.id,
            title=saved.title,
            author=saved.author,
            description=saved.description,
            cover_url=saved.cover_url,
            language=saved.language,
            page_count=int(saved.page_count) if saved.page_count else None,
            source="google_books",
        )