from fastapi import APIRouter, Request

from ..core.config import settings
from ..services.proxy_service import ProxyService

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth Gateway"],
)


@router.post("/register")
async def register(request: Request):
    body = await request.json()

    return await ProxyService().forward_request(
        method="POST",
        url=f"{settings.auth_service_url}/auth/register",
        json=body,
    )


@router.post("/login")
async def login(request: Request):
    body = await request.json()

    return await ProxyService().forward_request(
        method="POST",
        url=f"{settings.auth_service_url}/auth/login",
        json=body,
    )