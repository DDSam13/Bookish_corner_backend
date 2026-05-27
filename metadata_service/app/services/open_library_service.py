import httpx


class OpenLibraryService:
    async def search_book(self, title: str | None, author: str | None):
        if not title:
            return None

        query_parts = [title]

        if author:
            query_parts.append(author)

        query = " ".join(query_parts)

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                "https://openlibrary.org/search.json",
                params={
                    "q": query,
                    "limit": 5,
                    "language": "rus",
                },
            )

        if response.status_code >= 400:
            return None

        data = response.json()
        docs = data.get("docs", [])

        if not docs:
            return None

        best = docs[0]

        cover_id = best.get("cover_i")

        cover_url = None
        if cover_id:
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

        authors = best.get("author_name", [])

        return {
            "title": best.get("title"),
            "author": ", ".join(authors) if authors else author,
            "description": None,
            "cover_url": cover_url,
            "language": best.get("language", [None])[0] if best.get("language") else None,
            "page_count": best.get("number_of_pages_median"),
            "raw_data": best,
        }