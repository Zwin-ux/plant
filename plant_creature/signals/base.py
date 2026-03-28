from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol


@dataclass(frozen=True)
class SignalSample:
    timestamp: datetime
    raw_value: float

    @classmethod
    def now(cls, raw_value: float) -> "SignalSample":
        return cls(timestamp=datetime.now(timezone.utc), raw_value=raw_value)


class SignalProvider(Protocol):
    def read(self) -> SignalSample:
        """Return a single raw signal sample."""


class SignalProviderUnavailable(RuntimeError):
    """Raised when a requested signal provider cannot run in the current environment."""
