from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass

from config import SignalConfig, SimulationConfig

from .base import SignalProvider, SignalSample


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


@dataclass(frozen=True)
class _ProfileSettings:
    baseline_offset: float
    drift_bias: float
    wander_multiplier: float
    micro_multiplier: float
    surge_multiplier: float
    slow_multiplier: float
    fast_multiplier: float


_PROFILE_SETTINGS = {
    "healthy": _ProfileSettings(6.0, 0.08, 0.70, 0.65, 0.30, 0.85, 0.55),
    "dry": _ProfileSettings(-28.0, -0.75, 0.35, 0.45, 0.08, 0.55, 0.30),
    "recovering": _ProfileSettings(-32.0, 1.45, 0.30, 0.25, 0.08, 0.50, 0.20),
    "unstable": _ProfileSettings(0.0, 0.0, 2.80, 2.80, 1.10, 0.65, 1.55),
    "overloaded": _ProfileSettings(42.0, 0.70, 1.20, 1.70, 1.55, 1.25, 1.10),
}

SUPPORTED_SIMULATION_PROFILES = tuple(_PROFILE_SETTINGS.keys())


class SimulatedSignalProvider(SignalProvider):
    """
    Generate a believable development signal without requiring hardware.

    Profiles make it easy to rehearse tomorrow's moisture and ADC scenarios:
    `healthy`, `dry`, `recovering`, `unstable`, and `overloaded`.
    """

    def __init__(
        self,
        config: SignalConfig,
        simulation_config: SimulationConfig,
    ) -> None:
        if simulation_config.profile not in _PROFILE_SETTINGS:
            supported = ", ".join(SUPPORTED_SIMULATION_PROFILES)
            raise ValueError(
                f"Unknown simulation profile {simulation_config.profile!r}. "
                f"Supported profiles: {supported}."
            )

        self._config = config
        self._simulation_config = simulation_config
        self._profile_name = simulation_config.profile
        self._settings = _PROFILE_SETTINGS[simulation_config.profile]
        self._random = random.Random(simulation_config.seed)
        self._slow_phase = self._random.uniform(0.0, math.tau)
        self._fast_phase = self._random.uniform(0.0, math.tau)
        self._drift = self._random.uniform(-4.0, 4.0)
        self._surge = 0.0
        self._shock = 0.0
        self._recovery_lift = 0.0
        self._last_tick = time.monotonic()

    def read(self) -> SignalSample:
        now = time.monotonic()
        dt = max(now - self._last_tick, 0.001)
        self._last_tick = now

        self._slow_phase += dt * 0.48
        self._fast_phase += dt * 1.65

        self._drift += (
            self._random.uniform(-self._config.wander_step, self._config.wander_step)
            * self._settings.wander_multiplier
            + self._settings.drift_bias
        ) * dt * 0.45
        self._drift = _clamp(self._drift, -18.0, 18.0)

        if self._random.random() < (
            self._config.surge_chance_per_second
            * self._settings.surge_multiplier
            * dt
        ):
            self._surge = min(
                self._surge
                + self._random.uniform(4.0, self._config.max_surge_strength)
                * self._settings.surge_multiplier,
                28.0,
            )
        else:
            self._surge *= 0.72**dt

        if self._profile_name == "unstable":
            if self._random.random() < 0.80 * dt:
                self._shock = self._random.uniform(-35.0, 35.0)
            else:
                self._shock *= 0.28**dt
        else:
            self._shock *= 0.28**dt

        if self._profile_name == "recovering":
            self._recovery_lift = min(self._recovery_lift + (dt * 2.8), 24.0)
        else:
            self._recovery_lift = max(0.0, self._recovery_lift - (dt * 4.0))

        slow_rhythm = (
            math.sin(self._slow_phase) * 11.0 * self._settings.slow_multiplier
        )
        fast_flutter = (
            math.sin(self._fast_phase) * 3.5 * self._settings.fast_multiplier
        )
        micro_noise = self._random.uniform(
            -self._config.micro_noise * self._settings.micro_multiplier,
            self._config.micro_noise * self._settings.micro_multiplier,
        )

        raw_value = (
            self._config.baseline
            + self._settings.baseline_offset
            + slow_rhythm
            + fast_flutter
            + self._drift
            + self._surge
            + self._shock
            + self._recovery_lift
            + micro_noise
        )
        return SignalSample.now(
            raw_value=_clamp(raw_value, self._config.min_value, self._config.max_value)
        )
