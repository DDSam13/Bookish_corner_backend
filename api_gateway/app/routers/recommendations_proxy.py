from fastapi import APIRouter, Depends, Header, Request

from ..core.config import settings
from ..core.security import verify_jwt_token
from ..services.proxy_service import ProxyService

router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations Gateway"],
)


@router.post("/generate")
async def generate_recommendations(
    request: Request,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    body = await request.json()

    return await ProxyService().forward_request(
        method="POST",
        url=f"{settings.recommendation_service_url}/recommendations/generate",
        json=body,
        headers={"Authorization": authorization},
    )