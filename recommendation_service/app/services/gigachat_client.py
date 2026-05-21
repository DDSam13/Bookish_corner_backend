import time
import uuid

import httpx
from fastapi import HTTPException, status

from ..core.config import settings


class GigaChatClient:
    def __init__(self):
        self.access_token: str | None = None
        self.expires_at: int = 0

    async def _get_access_token(self) -> str:
        if self.access_token and int(time.time() * 1000) < self.expires_at:
            return self.access_token

        if not settings.gigachat_auth_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не указан GIGACHAT_AUTH_KEY в .env",
            )

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {settings.gigachat_auth_key}",
        }

        data = {
            "scope": settings.gigachat_scope,
        }

        async with httpx.AsyncClient(verify=False, timeout=20) as client:
            response = await client.post(
                settings.gigachat_oauth_url,
                headers=headers,
                data=data,
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Ошибка авторизации GigaChat: {response.text}",
            )

        token_data = response.json()

        self.access_token = token_data["access_token"]
        self.expires_at = token_data["expires_at"]

        return self.access_token

    async def generate(self, prompt: str) -> str:
        token = await self._get_access_token()

        payload = {
            "model": settings.gigachat_model,
            "messages": [
                {
                    "role": "system",
                    "content": "Ты возвращаешь только валидный JSON без markdown.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.4,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        async with httpx.AsyncClient(verify=False, timeout=40) as client:
            response = await client.post(
                settings.gigachat_chat_url,
                headers=headers,
                json=payload,
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Ошибка запроса к GigaChat: {response.text}",
            )

        data = response.json()

        return data["choices"][0]["message"]["content"]