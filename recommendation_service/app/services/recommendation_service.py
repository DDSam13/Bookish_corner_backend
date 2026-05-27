from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..core.config import settings
from ..repositories.recommendation_repository import RecommendationRepository
from ..schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
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

            print("\n========== RAW GIGACHAT RESPONSE ==========")
            print(raw_response)
            print("==========================================\n")

            recommendations = await LLMResponseValidator.validate_with_metadata(
                content=raw_response,
                metadata_service_url=settings.metadata_service_url,
                count=data.count,
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