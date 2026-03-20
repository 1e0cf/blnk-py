from __future__ import annotations

from ..http import AsyncHttp
from ..models.ledgers import CreateLedger, Ledger


class LedgersResource:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def create(self, body: CreateLedger) -> Ledger:
        data = await self._http.request("POST", "/ledgers", json=body.model_dump(exclude_none=True))
        return Ledger.model_validate(data)

    async def get(self, ledger_id: str) -> Ledger:
        data = await self._http.request("GET", f"/ledgers/{ledger_id}")
        return Ledger.model_validate(data)

    async def list(self) -> list[Ledger]:
        data = await self._http.request("GET", "/ledgers")
        return [Ledger.model_validate(item) for item in data]
