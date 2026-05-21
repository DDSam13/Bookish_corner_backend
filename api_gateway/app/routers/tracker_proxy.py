from fastapi import APIRouter, Depends, Header, Request

from ..core.config import settings
from ..core.security import verify_jwt_token
from ..services.proxy_service import ProxyService

router = APIRouter(
    prefix="/api/tracker",
    tags=["Tracker Gateway"],
)


@router.get("/goal/{user_id}")
async def get_goal(
    user_id: str,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    return await ProxyService().forward_request(
        method="GET",
        url=f"{settings.tracker_service_url}/tracker/goal/{user_id}",
        headers={"Authorization": authorization},
    )


@router.post("/goal")
async def create_goal(
    request: Request,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    body = await request.json()

    return await ProxyService().forward_request(
        method="POST",
        url=f"{settings.tracker_service_url}/tracker/goal",
        json=body,
        headers={"Authorization": authorization},
    )


@router.patch("/goal/{user_id}")
async def update_goal(
    user_id: str,
    request: Request,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    body = await request.json()

    return await ProxyService().forward_request(
        method="PATCH",
        url=f"{settings.tracker_service_url}/tracker/goal/{user_id}",
        json=body,
        headers={"Authorization": authorization},
    )


@router.post("/session")
async def create_session(
    request: Request,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    body = await request.json()

    return await ProxyService().forward_request(
        method="POST",
        url=f"{settings.tracker_service_url}/tracker/session",
        json=body,
        headers={"Authorization": authorization},
    )


@router.get("/session/{user_id}")
async def get_sessions(
    user_id: str,
    authorization: str = Header(default=None),
    payload=Depends(verify_jwt_token),
):
    return await ProxyService().forward_request(
        method="GET",
        url=f"{settings.tracker_service_url}/tracker/session/{user_id}",
        headers={"Authorization": authorization},
    )