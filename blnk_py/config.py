from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    api_key: str
    base_url: str = "http://localhost:5001"
    timeout_seconds: float = 30.0
