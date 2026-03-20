from __future__ import annotations

import uuid
from typing import Any

import httpx

from .config import Config
from .errors import ApiError, AuthError, NotFoundError

IDEMPOTENCY_HEADER = "Idempotency-Key"


class AsyncHttp:
    """Thin async HTTP transport for Blnk API.

    No retries, no rate-limit handling — just request, check status, return or raise.
    """

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self._client = httpx.AsyncClient(
            base_url=cfg.base_url,
            timeout=cfg.timeout_seconds,
            headers={
                "X-Blnk-Key": cfg.api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any] | list[Any]:
        headers: dict[str, str] = {}
        if method.upper() in {"POST", "PUT", "PATCH"}:
            headers[IDEMPOTENCY_HEADER] = idempotency_key or str(uuid.uuid4())

        resp = await self._client.request(method, path, json=json, headers=headers)

        if resp.status_code == 401:
            raise AuthError("unauthorized (check API key)")
        if resp.status_code == 404:
            raise NotFoundError(f"not found: {path}")
        if resp.status_code >= 400:
            raise ApiError(resp.status_code, "API error", resp.text)

        return resp.json()

    async def aclose(self) -> None:
        await self._client.aclose()
