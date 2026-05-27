import re
from difflib import SequenceMatcher

import httpx
from fastapi import HTTPException

from ..core.config import settings


def normalize_isbn(isbn: str | None) -> str | None:
    if not isbn:
        return None

    cleaned = isbn.replace("-", "").replace(" ", "").strip()

    if cleaned.isdigit() and len(cleaned) in (10, 13):
        return cleaned

    return None


def normalize_text(value: str | None) -> str:
    if not value:
        return ""

    value = value.lower().strip()
    value = value.replace("ё", "е")
    value = re.sub(r"[^a-zа-я0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value)

    return value


def similarity(left: str | None, right: str | None) -> float:
    left_norm = normalize_text(left)
    right_norm = normalize_text(right)

    if not left_norm or not right_norm:
        return 0.0

    return SequenceMatcher(None, left_norm, right_norm).ratio()


def authors_to_string(authors: list[str] | None) -> str | None:
    if not authors:
        return None

    return ", ".join(authors)


def is_relevant_result(
    requested_title: str | None,
    requested_author: str | None,
    found_title: str | None,
    found_authors: list[str] | None,
) -> bool:
    found_author = authors_to_string(found_authors)

    title_score = similarity(requested_title, found_title)
    author_score = similarity(requested_author, found_author)

    # Если пользователь указал и название, и автора — проверяем оба.
    if requested_title and requested_author:
        return title_score >= 0.45 and author_score >= 0.35

    # Если указан только title.
    if requested_title:
        return title_score >= 0.45

    # Если указан только author.
    if requested_author:
        return author_score >= 0.35

    return True


class GoogleBooksService:
    async def search_book(
        self,
        title: str | None,
        author: str | None,
        isbn: str | None,
    ):
        valid_isbn = normalize_isbn(isbn)

        queries = []

        # 1. Сначала пробуем точный ISBN, если он валидный.
        if valid_isbn:
            queries.append(f"isbn:{valid_isbn}")

        # 2. Потом fallback по названию и автору.
        text_query_parts = []

        if title:
            text_query_parts.append(f'intitle:"{title}"')

        if author:
            text_query_parts.append(f'inauthor:"{author}"')

        if text_query_parts:
            queries.append(" ".join(text_query_parts))

        # 3. Ещё один более мягкий fallback без операторов.
        if title and author:
            queries.append(f"{title} {author}")
        elif title:
            queries.append(title)

        if not queries:
            raise HTTPException(
                status_code=400,
                detail="Нужно указать хотя бы title, author или isbn",
            )

        async with httpx.AsyncClient(timeout=10) as client:
            for query in queries:
                params = {
                    "q": query,
                    "maxResults": 10,
                }

                if settings.google_books_api_key:
                    params["key"] = settings.google_books_api_key

                response = await client.get(
                    settings.google_books_api_url,
                    params=params,
                )

                if response.status_code == 429:
                    raise HTTPException(
                        status_code=503,
                        detail="Google Books API временно ограничил количество запросов. Попробуйте позже.",
                    )

                if response.status_code >= 400:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Ошибка Google Books API: {response.text}",
                    )

                data = response.json()
                items = data.get("items", [])

                best_result = None
                best_score = -1

                for item in items:
                    volume_info = item.get("volumeInfo", {})
                    found_title = volume_info.get("title")
                    found_authors = volume_info.get("authors", [])

                    if not is_relevant_result(
                            requested_title=title,
                            requested_author=author,
                            found_title=found_title,
                            found_authors=found_authors,
                    ):
                        continue

                    image_links = volume_info.get("imageLinks", {})

                    score = 0

                    if volume_info.get("description"):
                        score += 3

                    if image_links.get("thumbnail"):
                        score += 2

                    if volume_info.get("pageCount"):
                        score += 1

                    if volume_info.get("language"):
                        score += 1

                    candidate = {
                        "title": found_title,
                        "author": authors_to_string(found_authors),
                        "description": volume_info.get("description"),
                        "cover_url": image_links.get("thumbnail"),
                        "language": volume_info.get("language"),
                        "page_count": volume_info.get("pageCount"),
                        "raw_data": volume_info,
                    }

                    if score > best_score:
                        best_score = score
                        best_result = candidate

                if best_result:
                    return best_result

        return None