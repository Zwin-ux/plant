from __future__ import annotations

from config import StateConfig
from plant_creature.fusion import CreatureDrives
from plant_creature.memory.session import SessionMemory

from .models import CreatureSnapshot, CreatureState


class CreatureStateEngine:
    """Map hidden drives into public creature mood states with a little dwell."""

    def __init__(self, config: StateConfig) -> None:
        self._config = config
        self._current_state: CreatureState | None = None
        self._state_enter_tick = 0
        self._state_entry_hydration: float | None = None

    def evaluate(
        self,
        drives: CreatureDrives,
        session: SessionMemory,
    ) -> CreatureSnapshot:
        current_tick = session.tick_count + 1
        candidate = self._select_candidate(drives, session)

        if self._current_state is None:
            self._current_state = candidate
            self._state_enter_tick = current_tick
            self._state_entry_hydration = drives.hydration
            return CreatureSnapshot(
                state=self._current_state,
                previous_state=None,
                is_transition=False,
            )

        ticks_in_state = current_tick - self._state_enter_tick
        previous_state: CreatureState | None = None
        is_transition = False

        if candidate != self._current_state and self._should_transition(
            candidate,
            drives,
            ticks_in_state,
        ):
            previous_state = self._current_state
            self._current_state = candidate
            self._state_enter_tick = current_tick
            self._state_entry_hydration = drives.hydration
            is_transition = True

        return CreatureSnapshot(
            state=self._current_state,
            previous_state=previous_state,
            is_transition=is_transition,
        )

    def _select_candidate(
        self,
        drives: CreatureDrives,
        session: SessionMemory,
    ) -> CreatureState:
        previous_state = self._current_state
        previous_hydration = (
            drives.hydration
            if self._state_entry_hydration is None
            else self._state_entry_hydration
        )

        if drives.stress_load >= 0.78 or (
            drives.hydration <= 0.22 and drives.stability <= 0.35
        ):
            return CreatureState.STRESSED

        if (
            previous_state in {CreatureState.STRESSED, CreatureState.ALERT}
            and drives.stress_load <= 0.58
            and drives.hydration >= previous_hydration + 0.04
            and session.recent_peak_stress >= 0.72
        ):
            return CreatureState.RECOVERING

        if drives.energy <= 0.28 and drives.stress_load < 0.65:
            return CreatureState.SLEEPY

        if drives.stability <= 0.35 or (
            drives.stress_load >= 0.55 and drives.energy >= 0.45
        ):
            return CreatureState.ALERT

        if (
            drives.hydration >= 0.55
            and drives.stability >= 0.55
            and drives.energy >= 0.52
            and drives.stress_load < 0.45
        ):
            return CreatureState.ACTIVE

        return CreatureState.CALM

    def _should_transition(
        self,
        candidate: CreatureState,
        drives: CreatureDrives,
        ticks_in_state: int,
    ) -> bool:
        if self._current_state is CreatureState.RECOVERING:
            return ticks_in_state >= self._config.recovering_min_ticks

        if candidate is CreatureState.STRESSED and drives.stress_load >= 0.85:
            return True

        return ticks_in_state >= self._config.min_dwell_ticks
