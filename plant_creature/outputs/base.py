from __future__ import annotations

from typing import Protocol

from plant_creature.signals import ProcessedSignal
from plant_creature.state import CreatureSnapshot


class CreatureOutput(Protocol):
    def emit(self, signal: ProcessedSignal, snapshot: CreatureSnapshot) -> None:
        """Render or express the current creature state."""


class OutputUnavailable(RuntimeError):
    """Raised when a requested output surface cannot run in the current environment."""
