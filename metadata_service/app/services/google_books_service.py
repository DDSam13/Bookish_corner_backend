import httpx

from ..core.config import settings


class GoogleBooksService:
    async def search_book(self, title: str | None, author: str | None, isbn: str | None):
        query_parts = []

        if isbn:
            query_parts.append(f"isbn:{isbn}")

        if title:
            query_parts.append(f"intitle:{title}")

        if author:
            query_parts.append(f"inauthor:{author}")

        query = "+".join(query_parts)

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                settings.google_books_api_url,
                params={
                    "q": query,
                    "maxResults": 1,
                },
            )

        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])

        if not items:
            return None

        volume_info = items[0].get("volumeInfo", {})

        image_links = volume_info.get("imageLinks", {})

        authors = volume_info.get("authors", [])

        return {
            "title": volume_info.get("title"),
            "author": ", ".join(authors) if authors else None,
            "description": volume_info.get("description"),
            "cover_url": image_links.get("thumbnail"),
            "language": volume_info.get("language"),
            "page_count": volume_info.get("pageCount"),
            "raw_data": volume_info,
        }