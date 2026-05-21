from sqlalchemy.orm import Session

from ..core.config import settings
from ..models.llm_request import LLMRequest
from ..models.recommendation_cache import RecommendationCache


class RecommendationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cached(self, user_id, source_title: str, source_author: str | None, mode: str):
        return (
            self.db.query(RecommendationCache)
            .filter(
                RecommendationCache.user_id == user_id,
                RecommendationCache.source_title == source_title,
                RecommendationCache.source_author == source_author,
                RecommendationCache.mode == mode,
            )
            .first()
        )

    def save_cache(self, data, prompt: str, recommendations: list[dict]):
        cache = RecommendationCache(
            user_id=data.user_id,
            source_title=data.source_book.title,
            source_author=data.source_book.author,
            mode=data.mode.value,
            prompt=prompt,
            recommendations=recommendations,
        )

        self.db.add(cache)
        self.db.commit()
        self.db.refresh(cache)

        return cache

    def log_llm_success(self, prompt: str, response: str):
        log = LLMRequest(
            provider="gigachat",
            model=settings.gigachat_model,
            prompt=prompt,
            response=response,
            status="success",
        )

        self.db.add(log)
        self.db.commit()

    def log_llm_error(self, prompt: str, error_message: str):
        log = LLMRequest(
            provider="gigachat",
            model=settings.gigachat_model,
            prompt=prompt,
            status="error",
            error_message=error_message,
        )

        self.db.add(log)
        self.db.commit()