import httpx
from fastapi import HTTPException, status

from ..core.config import settings
from ..schemas.recommendation import SourceBook


class LibraryClient:
    async def get_book_by_id(
        self,
        book_id: str,
        authorization: str | None = None,
    ) -> SourceBook:
        headers = {}

        if authorization:
            headers["Authorization"] = authorization

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                f"{settings.api_gateway_url}/api/library/books/{book_id}",
                headers=headers,
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Не удалось получить книгу из Library Service: {response.text}",
            )

        data = response.json()

        return SourceBook(
            title=data.get("title"),
            author=data.get("author_name"),
            genre=data.get("genre_name"),
            description=data.get("description"),
        )