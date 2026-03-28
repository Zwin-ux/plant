from __future__ import annotations

from typing import Any

from config import LedRingConfig

from .base import OutputUnavailable


class WS2812RingOutput:
    """
    Placeholder WS2812 ring output surface for the first hardware bring-up pass.

    The class exposes import and availability checks now, while leaving creature
    lighting behavior for the first real hardware expression pass.
    """

    def __init__(self, config: LedRingConfig) -> None:
        self._config = config
        available, reason = self.probe(config)
        if not available:
            raise OutputUnavailable(reason)

    @classmethod
    def probe(cls, config: LedRingConfig) -> tuple[bool, str]:
        try:
            cls._load_dependencies()
        except OutputUnavailable as exc:
            return False, str(exc)

        return (
            True,
            "WS2812 libraries are available. Lighting behavior is still a placeholder.",
        )

    @staticmethod
    def _load_dependencies() -> tuple[Any, Any]:
        try:
            import board
            import neopixel
        except ImportError as exc:
            missing = exc.name or "hardware library"
            raise OutputUnavailable(
                "WS2812 output requires optional libraries "
                f"(missing: {missing})."
            ) from exc

        return board, neopixel

    def emit(self, signal: object, snapshot: object) -> None:
        del signal
        del snapshot
        raise OutputUnavailable(
            "WS2812 ring output is not wired into behavior yet. This module is a bring-up scaffold."
        )
