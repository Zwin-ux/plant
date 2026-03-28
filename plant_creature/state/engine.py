from __future__ import annotations

from config import StateThresholds
from plant_creature.signals import ProcessedSignal

from .models import CreatureSnapshot, CreatureState


class CreatureStateEngine:
    """Map normalized signal energy into creature-readable states."""

    def __init__(self, thresholds: StateThresholds) -> None:
        self._thresholds = thresholds

    def evaluate(self, signal: ProcessedSignal) -> CreatureSnapshot:
        value = signal.normalized_value

        if value <= self._thresholds.sleepy_max:
            state = CreatureState.SLEEPY
        elif value <= self._thresholds.calm_max:
            state = CreatureState.CALM
        elif value <= self._thresholds.active_max:
            state = CreatureState.ACTIVE
        elif value <= self._thresholds.alert_max:
            state = CreatureState.ALERT
        else:
            state = CreatureState.STRESSED

        return CreatureSnapshot(state=state, intensity=value)
