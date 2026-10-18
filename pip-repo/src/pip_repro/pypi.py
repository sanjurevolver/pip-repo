import asyncio
from typing import Any

import httpx


class PyPIClient:
    BASE = "https://pypi.org/pypi"

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(timeout=10.0)

    async def __aenter__(self) -> "PyPIClient":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self._client.aclose()

    async def get_project(self, name: str) -> dict:
        try:
            response = await self._client.get(f"{self.BASE}/{name}/json")
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError):
            return {}

    async def get_many(self, names: list[str]) -> dict[str, dict]:
        results = await asyncio.gather(
            *(self.get_project(name) for name in names),
            return_exceptions=True,
        )
        return {
            name: (result if not isinstance(result, Exception) else {})
            for name, result in zip(names, results)
        }
