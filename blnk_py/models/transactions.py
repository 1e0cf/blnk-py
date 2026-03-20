from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Distribution(BaseModel):
    identifier: str
    distribution: str
    narration: str | None = None


class TransactionCreate(BaseModel):
    source: str | None = None
    destination: str | None = None
    sources: list[Distribution] | None = None
    destinations: list[Distribution] | None = None
    amount: float
    precision: float = 100
    reference: str
    currency: str
    description: str | None = None
    inflight: bool = False
    allow_overdraft: bool = False
    skip_queue: bool = False
    inflight_expiry_date: str | None = None
    meta_data: dict[str, Any] | None = Field(default=None)


class Transaction(BaseModel):
    """Blnk transaction — maps to Go model.Transaction struct."""

    transaction_id: str
    amount: float
    precise_amount: int | None = None
    precision: float = 0
    source: str | None = None
    destination: str | None = None
    reference: str
    currency: str
    description: str = ""
    status: str
    hash: str = ""
    allow_overdraft: bool = False
    inflight: bool = False
    parent_transaction: str = ""
    created_at: datetime
    meta_data: dict[str, Any] | None = None
    sources: list[Distribution] | None = None
    destinations: list[Distribution] | None = None


class InflightUpdate(BaseModel):
    status: str
    amount: float | None = None


class RefundRequest(BaseModel):
    reason: str | None = None
    meta_data: dict[str, Any] | None = Field(default=None)


class BulkTransactionRequest(BaseModel):
    transactions: list[TransactionCreate]
    inflight: bool = False
    atomic: bool = False
    run_async: bool = False
    skip_queue: bool = False


class BulkTransactionResult(BaseModel):
    batch_id: str
    status: str
    transaction_count: int = 0
    error: str | None = None
