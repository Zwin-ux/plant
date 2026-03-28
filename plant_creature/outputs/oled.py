from __future__ import annotations

from typing import Any

from config import OLEDConfig
from plant_creature.presentation import CreaturePresentation

from .base import OutputUnavailable
from .oled_layouts import build_proof_frame


class SSD1306Output:
    """
    Placeholder SSD1306 output surface for the first creature expression pass.

    The module now consumes the same presentation object as the console path, but
    it still stops short of live hardware drawing until the display is connected.
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
            "SSD1306 libraries are available. Creature rendering is still a hardware-gated scaffold.",
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

    def emit(self, presentation: CreaturePresentation) -> None:
        del presentation
        raise OutputUnavailable(
            "SSD1306 output is not wired into live drawing yet. "
            "Use build_proof_frame() and the shared presentation model during hardware bring-up."
        )

    def preview_frame(self, presentation: CreaturePresentation) -> dict[str, object]:
        return build_proof_frame(presentation)
