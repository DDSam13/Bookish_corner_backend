from fastapi import APIRouter, Depends, Header, Request

from ..core.config import settings
from ..core.security import verify_jwt_token
from ..services.proxy_service import ProxyService

router = APIRouter(
    prefix="/api/metadata",
    tags=["Metadata Gateway"],
)


@router.post("/enrich")
async def enrich_book(
    request: Request,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    body = await request.json()

    return await ProxyService().forward_request(
        method="POST",
        url=f"{settings.metadata_service_url}/metadata/enrich",
        json=body,
        headers={"Authorization": authorization},
    )