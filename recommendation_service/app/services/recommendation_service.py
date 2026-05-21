from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repositories.recommendation_repository import RecommendationRepository
from ..schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendedBook,
)
from .gigachat_client import GigaChatClient
from .llm_response_validator import LLMResponseValidator
from .prompt_builder import PromptBuilder


class RecommendationService:
    def __init__(self, db: Session):
        self.repository = RecommendationRepository(db)
        self.gigachat = GigaChatClient()

    async def generate_recommendations(
        self,
        data: RecommendationRequest,
    ) -> RecommendationResponse:
        cached = self.repository.get_cached(
            user_id=data.user_id,
            source_title=data.source_book.title,
            source_author=data.source_book.author,
            mode=data.mode.value,
        )

        if cached:
            recommendations = [
                RecommendedBook(**item)
                for item in cached.recommendations
            ]

            return RecommendationResponse(
                source_book=data.source_book,
                mode=data.mode,
                recommendations=recommendations,
            )

        prompt = PromptBuilder.build_prompt(data)

        try:
            raw_response = await self.gigachat.generate(prompt)

            recommendations = LLMResponseValidator.validate(raw_response)

            recommendations = recommendations[: data.count]

            if len(recommendations) < data.count:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="GigaChat вернул меньше рекомендаций, чем требуется",
                )

            serialized_recommendations = [
                item.model_dump()
                for item in recommendations
            ]

            self.repository.log_llm_success(
                prompt=prompt,
                response=raw_response,
            )

            self.repository.save_cache(
                data=data,
                prompt=prompt,
                recommendations=serialized_recommendations,
            )

            return RecommendationResponse(
                source_book=data.source_book,
                mode=data.mode,
                recommendations=recommendations,
            )

        except HTTPException as exception:
            self.repository.log_llm_error(
                prompt=prompt,
                error_message=str(exception.detail),
            )
            raise exception

        except Exception as exception:
            self.repository.log_llm_error(
                prompt=prompt,
                error_message=str(exception),
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка генерации рекомендаций",
            )