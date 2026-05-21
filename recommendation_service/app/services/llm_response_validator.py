import json

from fastapi import HTTPException, status
from pydantic import ValidationError

from ..schemas.recommendation import RecommendedBook


class LLMResponseValidator:
    @staticmethod
    def validate(content: str) -> list[RecommendedBook]:
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="GigaChat вернул невалидный JSON",
            )

        if not isinstance(parsed, dict):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Ответ GigaChat должен быть JSON-объектом",
            )

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