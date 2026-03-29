from __future__ import annotations

from config import StateConfig
from plant_creature.fusion import CreatureDrives
from plant_creature.memory.session import SessionMemory

from .models import CreatureSnapshot, CreatureState


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(value, maximum))


class CreatureStateEngine:
    """Map hidden drives into plant-creature states that are legible at a glance."""

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
                intensity=self._intensity_for(candidate, drives),
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
            intensity=self._intensity_for(self._current_state, drives),
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

        if (
            drives.hydration >= self._config.overload_hydration_ceiling
            or (
                drives.stress_load >= self._config.overload_stress_ceiling
                and drives.stability <= 0.5
            )
        ):
            return CreatureState.OVERLOADED

        if (
            drives.hydration <= self._config.thirsty_hydration_floor
            or (
                drives.stress_load >= 0.68
                and drives.hydration < 0.45
            )
        ):
            return CreatureState.THIRSTY

        if (
            previous_state in {
                CreatureState.THIRSTY,
                CreatureState.ALERT,
                CreatureState.OVERLOADED,
            }
            and drives.hydration
            >= previous_hydration + self._config.recovering_hydration_lift
            and drives.stress_load <= self._config.recovering_stress_ceiling
            and session.recent_peak_stress >= self._config.recovery_peak_floor
        ):
            return CreatureState.RECOVERING

        if (
            drives.stability <= self._config.alert_stability_floor
            or drives.stress_load >= self._config.stress_warning_floor
        ):
            return CreatureState.ALERT

        return CreatureState.CALM

    def _should_transition(
        self,
        candidate: CreatureState,
        drives: CreatureDrives,
        ticks_in_state: int,
    ) -> bool:
        if self._current_state is CreatureState.RECOVERING:
            return ticks_in_state >= self._config.recovering_min_ticks

        if candidate is CreatureState.OVERLOADED and (
            drives.hydration >= 0.92 or drives.stress_load >= 0.88
        ):
            return True

        return ticks_in_state >= self._config.min_dwell_ticks

    @staticmethod
    def _intensity_for(state: CreatureState, drives: CreatureDrives) -> float:
        if state is CreatureState.CALM:
            return _clamp(
                ((drives.hydration + drives.stability + (1.0 - drives.stress_load)) / 3.0)
            )
        if state is CreatureState.THIRSTY:
            return _clamp(max(1.0 - drives.hydration, drives.stress_load))
        if state is CreatureState.RECOVERING:
            return _clamp(max(drives.hydration, 1.0 - drives.stress_load))
        if state is CreatureState.ALERT:
            return _clamp(max(1.0 - drives.stability, drives.stress_load))
        return _clamp(max(drives.hydration, drives.stress_load))
