from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from config import SignalConfig


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


@dataclass(frozen=True)
class ProcessedSignal:
    timestamp: datetime
    raw_value: float
    smoothed_value: float
    normalized_value: float


class SignalProcessor:
    """Smooth and normalize raw samples into a stable control signal."""

    def __init__(self, config: SignalConfig) -> None:
        self._config = config
        self._last_smoothed: float | None = None

    def process(self, raw_value: float) -> ProcessedSignal:
        if self._last_smoothed is None:
            smoothed = raw_value
        else:
            alpha = self._config.smoothing_factor
            smoothed = (alpha * raw_value) + ((1.0 - alpha) * self._last_smoothed)

        self._last_smoothed = smoothed

        normalized = (
            smoothed - self._config.min_value
        ) / (self._config.max_value - self._config.min_value)
        normalized = _clamp(normalized, 0.0, 1.0)

        return ProcessedSignal(
            timestamp=datetime.now(timezone.utc),
            raw_value=raw_value,
            smoothed_value=smoothed,
            normalized_value=normalized,
        )
