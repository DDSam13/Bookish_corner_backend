import httpx


class ProxyService:
    async def forward_request(
        self,
        method: str,
        url: str,
        json: dict | None = None,
        headers: dict | None = None,
    ):
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                json=json,
                headers=headers,
            )

        try:
            return response.json()

        except Exception:
            return {
                "status_code": response.status_code,
                "message": response.text,
            }