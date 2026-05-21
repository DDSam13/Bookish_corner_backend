from fastapi import APIRouter, Depends, Header, Request

from ..core.config import settings
from ..core.security import verify_jwt_token
from ..services.proxy_service import ProxyService

router = APIRouter(
    prefix="/api/progress",
    tags=["Progress Gateway"],
)


@router.get("/{user_id}")
async def get_user_progress(
    user_id: str,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    return await ProxyService().forward_request(
        method="GET",
        url=f"{settings.progress_service_url}/progress/{user_id}",
        headers={"Authorization": authorization},
    )


@router.post("/")
async def create_progress(
    request: Request,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    body = await request.json()

    return await ProxyService().forward_request(
        method="POST",
        url=f"{settings.progress_service_url}/progress/",
        json=body,
        headers={"Authorization": authorization},
    )


@router.patch("/{user_id}/{book_id}")
async def update_progress(
    user_id: str,
    book_id: str,
    request: Request,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    body = await request.json()

    return await ProxyService().forward_request(
        method="PATCH",
        url=f"{settings.progress_service_url}/progress/{user_id}/{book_id}",
        json=body,
        headers={"Authorization": authorization},
    )