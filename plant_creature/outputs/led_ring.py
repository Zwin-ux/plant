from __future__ import annotations

from typing import Any

from config import LedRingConfig
from plant_creature.presentation import CreaturePresentation

from .base import OutputUnavailable


class WS2812RingOutput:
    """
    Placeholder WS2812 ring output surface for the first creature expression pass.

    The class now consumes the presentation object and exposes the aura pattern
    mapping we will eventually send to the ring once the hardware is attached.
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
            "WS2812 libraries are available. Aura behavior is still a hardware-gated scaffold.",
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

    def emit(self, presentation: CreaturePresentation) -> None:
        del presentation
        raise OutputUnavailable(
            "WS2812 ring output is not wired into live behavior yet. "
            "Use the presentation aura pattern during tomorrow's hardware pass."
        )
