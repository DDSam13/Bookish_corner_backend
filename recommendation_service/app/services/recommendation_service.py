from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repositories.recommendation_repository import RecommendationRepository
from ..schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendedBook,
)
from .gigachat_client import GigaChatClient
from .library_client import LibraryClient
from .llm_response_validator import LLMResponseValidator
from .prompt_builder import PromptBuilder


class RecommendationService:
    def __init__(self, db: Session):
        self.repository = RecommendationRepository(db)
        self.gigachat = GigaChatClient()
        self.library_client = LibraryClient()

    async def generate_recommendations(
        self,
        data: RecommendationRequest,
        authorization: str | None = None,
    ) -> RecommendationResponse:
        cached = self.repository.get_cached(
            user_id=data.user_id,
            book_id=data.book_id,
            mode=data.mode.value,
        )

        if cached:
            recommendations = [
                RecommendedBook(**item)
                for item in cached.recommendations
            ]

            source_book = await self.library_client.get_book_by_id(
                str(data.book_id),
                authorization=authorization,
            )

            return RecommendationResponse(
                source_book=source_book,
                mode=data.mode,
                recommendations=recommendations,
            )

        source_book = await self.library_client.get_book_by_id(
            str(data.book_id),
            authorization=authorization,
        )

        prompt = PromptBuilder.build_prompt(
            book=source_book,
            mode=data.mode,
            count=data.count,
        )

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
                source_book=source_book,
                prompt=prompt,
                recommendations=serialized_recommendations,
            )

            return RecommendationResponse(
                source_book=source_book,
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