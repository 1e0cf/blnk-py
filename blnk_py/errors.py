from __future__ import annotations

from typing import Any


class BlnkError(Exception):
    """Base exception for all Blnk SDK errors."""


class AuthError(BlnkError):
    """Raised on 401 Unauthorized."""


class NotFoundError(BlnkError):
    """Raised on 404 Not Found."""


class ApiError(BlnkError):
    """Raised on any non-2xx response not covered above."""

    def __init__(self, status_code: int, message: str, payload: Any | None = None) -> None:
        super().__init__(f"{status_code}: {message}")
        self.status_code = status_code
        self.payload = payload
