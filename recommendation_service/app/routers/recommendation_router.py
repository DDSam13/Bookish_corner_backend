from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.recommendation import RecommendationRequest, RecommendationResponse
from ..services.recommendation_service import RecommendationService

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.post("/generate", response_model=RecommendationResponse)
async def generate_recommendations(
    data: RecommendationRequest,
    db: Session = Depends(get_db),
):
    return await RecommendationService(db).generate_recommendations(data)