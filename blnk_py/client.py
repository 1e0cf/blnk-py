from __future__ import annotations

from .config import Config
from .http import AsyncHttp
from .resources.balances import BalancesResource
from .resources.ledgers import LedgersResource
from .resources.reconciliation import ReconciliationResource
from .resources.search import SearchResource
from .resources.transactions import TransactionsResource


class AsyncBlnkClient:
    """Async Python client for the Blnk ledger API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:5001",
        *,
        timeout: float = 30.0,
        http: AsyncHttp | None = None,
    ) -> None:
        cfg = Config(api_key=api_key, base_url=base_url, timeout_seconds=timeout)
        self._http = http or AsyncHttp(cfg)
        self.transactions = TransactionsResource(self._http)
        self.balances = BalancesResource(self._http)
        self.ledgers = LedgersResource(self._http)
        self.reconciliation = ReconciliationResource(self._http)
        self.search = SearchResource(self._http)

    async def aclose(self) -> None:
        await self._http.aclose()
