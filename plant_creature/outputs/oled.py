from __future__ import annotations

from typing import Any

from config import OLEDConfig

from .base import OutputUnavailable


class SSD1306Output:
    """
    Placeholder SSD1306 output surface for the first hardware bring-up pass.

    This module intentionally stops short of creature rendering behavior so the
    repo can prepare the boundary without pretending the display logic is done.
    """

    def __init__(self, config: OLEDConfig) -> None:
        self._config = config
        available, reason = self.probe(config)
        if not available:
            raise OutputUnavailable(reason)

    @classmethod
    def probe(cls, config: OLEDConfig) -> tuple[bool, str]:
        try:
            cls._load_dependencies()
        except OutputUnavailable as exc:
            return False, str(exc)

        return (
            True,
            "SSD1306 libraries are available. Rendering behavior is still a placeholder.",
        )

    @staticmethod
    def _load_dependencies() -> tuple[Any, Any, Any]:
        try:
            import board
            import busio
            import adafruit_ssd1306
        except ImportError as exc:
            missing = exc.name or "hardware library"
            raise OutputUnavailable(
                "SSD1306 output requires optional libraries "
                f"(missing: {missing})."
            ) from exc

        return board, busio, adafruit_ssd1306

    def emit(self, signal: object, snapshot: object) -> None:
        del signal
        del snapshot
        raise OutputUnavailable(
            "SSD1306 output is not wired into behavior yet. This module is a bring-up scaffold."
        )
