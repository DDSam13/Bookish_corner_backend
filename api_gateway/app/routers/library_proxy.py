from fastapi import (
    APIRouter,
    Depends,
    Header,
    Request,
)

from ..core.config import settings
from ..core.security import verify_jwt_token
from ..services.proxy_service import ProxyService

router = APIRouter(
    prefix="/api/library",
    tags=["Library Gateway"],
)


@router.get("/books")
async def get_books(
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    return await ProxyService().forward_request(
        method="GET",
        url=f"{settings.library_service_url}/books/",
        headers={
            "Authorization": authorization,
        },
    )


@router.post("/books")
async def create_book(
    request: Request,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    body = await request.json()

    return await ProxyService().forward_request(
        method="POST",
        url=f"{settings.library_service_url}/books/",
        json=body,
        headers={
            "Authorization": authorization,
        },
    )

@router.get("/books/{book_id}")
async def get_book_by_id(
    book_id: str,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    return await ProxyService().forward_request(
        method="GET",
        url=f"{settings.library_service_url}/books/{book_id}",
        headers={
            "Authorization": authorization,
        },
    )