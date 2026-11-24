
import asyncio

import httpx

from ai_client.config import settings


class AIClient:
    def __init__(self):
        self.base_url = settings.api_base_url
        self.api_key = settings.api_key
        self.timeout = settings.request_timeout
        self.max_retries = settings.max_retries

    async def get(self, endpoint: str):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(
                    base_url=self.base_url,
                    timeout=self.timeout
                ) as client:
                    response = await client.get(
                        endpoint,
                        headers=headers
                    )

                response.raise_for_status()
                return response.json()

            except (httpx.TimeoutException, httpx.TransportError):
                if attempt == self.max_retries:
                    raise

                await asyncio.sleep(0.5 * (attempt + 1))

            except httpx.HTTPStatusError:
                raise
