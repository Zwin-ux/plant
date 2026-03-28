from __future__ import annotations

from dataclasses import dataclass

from config import FusionConfig
from plant_creature.fusion.drives import CreatureDrives
from plant_creature.state.models import CreatureSnapshot, CreatureState


@dataclass(frozen=True)
class SessionMemory:
    tick_count: int = 0
    stable_streak_ticks: int = 0
    stress_streak_ticks: int = 0
    recent_peak_stress: float = 0.0
    last_state: CreatureState | None = None
    last_transition_tick: int = 0
    recovery_count: int = 0
    last_care_tick: int | None = None


class SessionTracker:
    """Track short-lived creature history that shapes expression and recovery."""

    def __init__(self, config: FusionConfig) -> None:
        self._config = config
        self._memory = SessionMemory()

    @property
    def memory(self) -> SessionMemory:
        return self._memory

    def update(self, drives: CreatureDrives, snapshot: CreatureSnapshot) -> SessionMemory:
        tick_count = self._memory.tick_count + 1
        stable_streak_ticks = (
            self._memory.stable_streak_ticks + 1
            if drives.stability >= self._config.stable_threshold
            else 0
        )
        stress_streak_ticks = (
            self._memory.stress_streak_ticks + 1
            if snapshot.state is CreatureState.STRESSED or drives.stress_load >= 0.55
            else 0
        )
        recent_peak_stress = max(
            drives.stress_load,
            self._memory.recent_peak_stress * self._config.stress_peak_decay,
        )
        last_transition_tick = (
            tick_count if snapshot.is_transition else self._memory.last_transition_tick
        )
        recovery_count = self._memory.recovery_count + (
            1
            if snapshot.is_transition and snapshot.state is CreatureState.RECOVERING
            else 0
        )

        self._memory = SessionMemory(
            tick_count=tick_count,
            stable_streak_ticks=stable_streak_ticks,
            stress_streak_ticks=stress_streak_ticks,
            recent_peak_stress=recent_peak_stress,
            last_state=snapshot.state,
            last_transition_tick=last_transition_tick,
            recovery_count=recovery_count,
            last_care_tick=self._memory.last_care_tick,
        )
        return self._memory
