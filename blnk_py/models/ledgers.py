from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Ledger(BaseModel):
    """Blnk ledger — maps to Go model.Ledger struct."""

    ledger_id: str
    name: str
    created_at: datetime
    meta_data: dict[str, Any] | None = None


class CreateLedger(BaseModel):
    name: str
    meta_data: dict[str, Any] | None = Field(default=None)
