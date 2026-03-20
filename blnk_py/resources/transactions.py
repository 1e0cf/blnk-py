from __future__ import annotations

from typing import Any

from ..http import AsyncHttp
from ..models.transactions import (
    BulkTransactionRequest,
    BulkTransactionResult,
    InflightUpdate,
    RefundRequest,
    Transaction,
    TransactionCreate,
)


class TransactionsResource:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def create(
        self, body: TransactionCreate, *, idempotency_key: str | None = None,
    ) -> Transaction:
        data = await self._http.request(
            "POST",
            "/transactions",
            json=body.model_dump(exclude_none=True),
            idempotency_key=idempotency_key,
        )
        return Transaction.model_validate(data)

    async def get(self, transaction_id: str) -> Transaction:
        data = await self._http.request("GET", f"/transactions/{transaction_id}")
        return Transaction.model_validate(data)

    async def get_by_ref(self, reference: str) -> Transaction:
        data = await self._http.request("GET", f"/transactions/reference/{reference}")
        return Transaction.model_validate(data)

    async def commit_inflight(self, inflight_id: str, *, amount: float | None = None) -> Transaction:
        payload = InflightUpdate(status="commit", amount=amount)
        data = await self._http.request(
            "PUT",
            f"/transactions/inflight/{inflight_id}",
            json=payload.model_dump(exclude_none=True),
        )
        return Transaction.model_validate(data)

    async def void_inflight(self, inflight_id: str) -> Transaction:
        payload = InflightUpdate(status="void")
        data = await self._http.request(
            "PUT",
            f"/transactions/inflight/{inflight_id}",
            json=payload.model_dump(exclude_none=True),
        )
        return Transaction.model_validate(data)

    async def refund(self, transaction_id: str, body: RefundRequest | None = None) -> dict[str, Any]:
        data = await self._http.request(
            "POST",
            f"/refund-transaction/{transaction_id}",
            json=body.model_dump(exclude_none=True) if body else {},
        )
        return data

    async def filter(
        self,
        filters: list[dict[str, Any]],
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Transaction]:
        data = await self._http.request(
            "POST",
            "/transactions/filter",
            json={"filters": filters, "limit": limit, "offset": offset},
        )
        items = data.get("data", []) if isinstance(data, dict) else data
        return [Transaction.model_validate(item) for item in items]

    async def create_bulk(self, body: BulkTransactionRequest) -> BulkTransactionResult:
        data = await self._http.request(
            "POST",
            "/transactions/bulk",
            json=body.model_dump(exclude_none=True),
        )
        return BulkTransactionResult.model_validate(data)
