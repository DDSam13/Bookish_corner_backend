import json
import asyncio
import re
from difflib import SequenceMatcher

import httpx
from fastapi import HTTPException, status
from pydantic import ValidationError
from json_repair import repair_json

from ..schemas.recommendation import RecommendedBook


class LLMResponseValidator:
    @staticmethod
    def _normalize_text(value: str | None) -> str:
        if not value:
            return ""

        value = value.lower().strip()
        value = value.replace("ё", "е")
        value = re.sub(r"[^a-zа-я0-9\s]", " ", value)
        value = re.sub(r"\s+", " ", value)

        return value

    @staticmethod
    def _similarity(left: str | None, right: str | None) -> float:
        left_norm = LLMResponseValidator._normalize_text(left)
        right_norm = LLMResponseValidator._normalize_text(right)

        if not left_norm or not right_norm:
            return 0.0

        return SequenceMatcher(None, left_norm, right_norm).ratio()

    @staticmethod
    def _parse_json(content: str) -> dict:
        cleaned = content.strip()

        # Убираем markdown-обёртку, если модель вернула ```json ... ```
        if cleaned.startswith("```"):
            cleaned = (
                cleaned
                .replace("```json", "")
                .replace("```JSON", "")
                .replace("```", "")
                .strip()
            )

        # 1. Сначала пробуем распарсить как обычный JSON
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            # 2. Если не получилось — вырезаем JSON-объект из текста
            start = cleaned.find("{")
            end = cleaned.rfind("}")

            if start != -1 and end != -1 and end > start:
                cleaned = cleaned[start:end + 1]

            # 3. Пробуем автоматически починить "почти JSON"
            try:
                repaired = repair_json(cleaned)
                parsed = json.loads(repaired)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="GigaChat вернул невалидный JSON",
                )

        if not isinstance(parsed, dict):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Ответ GigaChat должен быть JSON-объектом",
            )

        return parsed

    @staticmethod
    def validate(content: str) -> list[RecommendedBook]:
        """
        Базовая проверка структуры ответа GigaChat.
        Оставляем этот метод, чтобы не сломать старый код.
        """
        parsed = LLMResponseValidator._parse_json(content)

        recommendations = parsed.get("recommendations")

        if not isinstance(recommendations, list) or len(recommendations) == 0:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="GigaChat не вернул список рекомендаций",
            )

        try:
            return [
                RecommendedBook(**item)
                for item in recommendations
            ]
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Список рекомендаций имеет неверную структуру",
            )

    @staticmethod
    def _is_metadata_match(
            generated_title: str,
            generated_author: str,
            metadata_title: str | None,
            metadata_author: str | None,
    ) -> bool:
        title_score = LLMResponseValidator._similarity(
            generated_title,
            metadata_title,
        )
        author_score = LLMResponseValidator._similarity(
            generated_author,
            metadata_author,
        )

        # Если название хорошо совпало — считаем книгу найденной,
        # а автора дальше можно уточнить из metadata_service.
        if title_score >= 0.65:
            return True

        # Если и название, и автор примерно совпали — тоже принимаем.
        return title_score >= 0.45 and author_score >= 0.45
    @staticmethod
    async def _validate_single_with_metadata(
        recommendation: RecommendedBook,
        metadata_service_url: str,
    ) -> RecommendedBook | None:
        """
        Проверяет одну рекомендацию через metadata_service.

        Если metadata_service не подтверждает книгу или автора,
        рекомендация отбрасывается.
        """
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"{metadata_service_url.rstrip('/')}/metadata/enrich",
                json={
                    "title": recommendation.title,
                    "author": recommendation.author,
                    "isbn": "",
                },
            )

        if response.status_code != 200:
            return None

        metadata = response.json()

        metadata_title = metadata.get("title")
        metadata_author = metadata.get("author")

        if not LLMResponseValidator._is_metadata_match(
            generated_title=recommendation.title,
            generated_author=recommendation.author,
            metadata_title=metadata_title,
            metadata_author=metadata_author,
        ):
            return None

        corrected_data = recommendation.model_dump()

        # Если metadata_service нашёл книгу, используем уточнённые данные.
        # Это исправляет случаи, когда LLM указала неточный перевод или ошиблась в авторе.
        corrected_data["title"] = metadata_title or recommendation.title
        corrected_data["author"] = metadata_author or recommendation.author
        corrected_data["search_query"] = f"{corrected_data['title']} {corrected_data['author']}"

        try:
            return RecommendedBook(**corrected_data)
        except ValidationError:
            return None

    @staticmethod
    async def validate_with_metadata(
            content: str,
            metadata_service_url: str,
            count: int,
    ) -> list[RecommendedBook]:
        recommendations = LLMResponseValidator.validate(content)

        # Не проверяем бесконечно много кандидатов.
        # Берём с запасом, но ограниченно.
        candidates = recommendations[: max(count * 2, 8)]

        tasks = [
            LLMResponseValidator._validate_single_with_metadata(
                recommendation=recommendation,
                metadata_service_url=metadata_service_url,
            )
            for recommendation in candidates
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        validated: list[RecommendedBook] = []

        for item in results:
            if isinstance(item, RecommendedBook):
                validated.append(item)

            if len(validated) >= count:
                break

        if not validated:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=(
                    "Не удалось подтвердить рекомендации через metadata_service. "
                    "GigaChat вернул рекомендации, но metadata_service не смог подтвердить книги."
                ),
            )

        # Важно: не требуем строго count, иначе хороший ответ может падать,
        # если подтвердились 3–4 книги из 5.
        return validated