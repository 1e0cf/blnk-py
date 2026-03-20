from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Balance(BaseModel):
    """Blnk balance — maps to Go model.Balance struct."""

    balance_id: str
    balance: int
    credit_balance: int
    debit_balance: int
    inflight_balance: int = 0
    inflight_credit_balance: int = 0
    inflight_debit_balance: int = 0
    currency_multiplier: float = 0
    ledger_id: str
    identity_id: str = ""
    indicator: str | None = None
    currency: str
    version: int = 0
    created_at: datetime
    meta_data: dict[str, Any] | None = None


class CreateBalance(BaseModel):
    ledger_id: str
    currency: str
    indicator: str | None = None
    currency_multiplier: float = 0
    identity_id: str | None = None
    meta_data: dict[str, Any] | None = Field(default=None)
