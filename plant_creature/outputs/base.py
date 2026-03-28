from __future__ import annotations

from typing import Protocol

from plant_creature.presentation import CreaturePresentation


class CreatureOutput(Protocol):
    def emit(self, presentation: CreaturePresentation) -> None:
        """Render or express the current creature presentation."""


class OutputUnavailable(RuntimeError):
    """Raised when a requested output surface cannot run in the current environment."""
