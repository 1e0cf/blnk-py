from __future__ import annotations

from typing import Any

from ..errors import NotFoundError
from ..http import AsyncHttp
from ..models.balances import Balance, CreateBalance


class BalancesResource:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def create(self, body: CreateBalance) -> Balance:
        data = await self._http.request("POST", "/balances", json=body.model_dump(exclude_none=True))
        return Balance.model_validate(data)

    async def get(self, balance_id: str) -> Balance:
        data = await self._http.request("GET", f"/balances/{balance_id}")
        return Balance.model_validate(data)

    async def get_by_indicator(self, indicator: str, currency: str) -> Balance | None:
        """Look up a balance by indicator + currency. Returns None if not found."""
        try:
            data = await self._http.request(
                "GET",
                f"/balances/indicator/{indicator}/currency/{currency}",
            )
        except NotFoundError:
            return None
        return Balance.model_validate(data)

    async def list(self) -> list[Balance]:
        data = await self._http.request("GET", "/balances")
        if not data:
            return []
        return [Balance.model_validate(item) for item in data]

    async def filter(
        self,
        filters: list[dict[str, Any]],
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Balance]:
        data = await self._http.request(
            "POST",
            "/balances/filter",
            json={"filters": filters, "limit": limit, "offset": offset},
        )
        if not data:
            return []
        items = data.get("data", []) if isinstance(data, dict) else data
        if not items:
            return []
        return [Balance.model_validate(item) for item in items]
