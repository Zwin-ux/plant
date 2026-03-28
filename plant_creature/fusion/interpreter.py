from __future__ import annotations

import math

from config import FusionConfig
from plant_creature.memory import SessionMemory
from plant_creature.signals import ProcessedSignal

from .drives import CreatureDrives, FusionSnapshot


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


class DriveInterpreter:
    """Blend processed input into a small hidden drive model for the creature."""

    def __init__(self, config: FusionConfig) -> None:
        self._config = config
        self._last_drives: CreatureDrives | None = None
        self._last_normalized: float | None = None

    def interpret(self, signal: ProcessedSignal, session: SessionMemory) -> FusionSnapshot:
        previous_normalized = (
            signal.normalized_value
            if self._last_normalized is None
            else self._last_normalized
        )
        normalized_delta = signal.normalized_value - previous_normalized

        hydration_target = signal.normalized_value
        stability_target = 1.0 - _clamp(
            abs(normalized_delta) / self._config.stability_window,
            0.0,
            1.0,
        )

        local_time = signal.timestamp.astimezone()
        local_hour_float = (
            local_time.hour
            + (local_time.minute / 60.0)
            + (local_time.second / 3600.0)
        )
        energy_target = 0.15 + 0.85 * (
            (
                math.cos(((local_hour_float - 14.0) / 24.0) * math.tau) + 1.0
            )
            / 2.0
        )

        stable_ratio = min(
            1.0,
            session.stable_streak_ticks / self._config.stable_streak_goal_ticks,
        )
        previous_stress = 0.0 if self._last_drives is None else self._last_drives.stress_load
        bond_target = _clamp(
            0.20 + (0.45 * stable_ratio) + (0.15 * (1.0 - previous_stress)),
            0.0,
            1.0,
        )
        stress_target = _clamp(
            (0.55 * (1.0 - hydration_target))
            + (0.35 * (1.0 - stability_target))
            + (0.10 * max(0.0, energy_target - 0.75)),
            0.0,
            1.0,
        )

        targets = CreatureDrives(
            hydration=hydration_target,
            stability=stability_target,
            energy=energy_target,
            bond=bond_target,
            stress_load=stress_target,
        )

        if self._last_drives is None:
            drives = targets
        else:
            alpha = self._config.drive_smoothing_alpha
            drives = CreatureDrives(
                hydration=self._smooth(self._last_drives.hydration, hydration_target, alpha),
                stability=self._smooth(self._last_drives.stability, stability_target, alpha),
                energy=self._smooth(self._last_drives.energy, energy_target, alpha),
                bond=self._smooth(self._last_drives.bond, bond_target, alpha),
                stress_load=self._smooth(
                    self._last_drives.stress_load,
                    stress_target,
                    alpha,
                ),
            )

        self._last_normalized = signal.normalized_value
        self._last_drives = drives

        return FusionSnapshot(
            drives=drives,
            targets=targets,
            normalized_delta=normalized_delta,
            trend=self._trend_label(normalized_delta),
        )

    @staticmethod
    def _smooth(previous: float, target: float, alpha: float) -> float:
        return previous + (alpha * (target - previous))

    @staticmethod
    def _trend_label(delta: float) -> str:
        if delta >= 0.03:
            return "rising"
        if delta <= -0.03:
            return "falling"
        return "steady"
