from __future__ import annotations

import math
import random
import time

from config import SignalConfig


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


class SimulatedSignalProvider:
    """
    Generate a soft, living-feeling signal for development before hardware arrives.

    The signal mixes:
    - slow cyclical motion
    - faster surface flutter
    - random drift
    - occasional surges

    Future real hardware providers should expose the same narrow contract:
    `read() -> float`
    """

    def __init__(self, config: SignalConfig, seed: int | None = None) -> None:
        self._config = config
        self._random = random.Random(seed)
        self._slow_phase = self._random.uniform(0.0, math.tau)
        self._fast_phase = self._random.uniform(0.0, math.tau)
        self._drift = self._random.uniform(-4.0, 4.0)
        self._surge = 0.0
        self._last_tick = time.monotonic()

    def read(self) -> float:
        now = time.monotonic()
        dt = max(now - self._last_tick, 0.001)
        self._last_tick = now

        self._slow_phase += dt * 0.55
        self._fast_phase += dt * 1.8

        self._drift += self._random.uniform(
            -self._config.wander_step,
            self._config.wander_step,
        ) * dt * 0.45
        self._drift = _clamp(self._drift, -14.0, 14.0)

        if self._random.random() < self._config.surge_chance_per_second * dt:
            self._surge = min(
                self._surge + self._random.uniform(5.0, self._config.max_surge_strength),
                24.0,
            )
        else:
            self._surge *= 0.72**dt

        slow_rhythm = math.sin(self._slow_phase) * 11.0
        fast_flutter = math.sin(self._fast_phase) * 3.5
        micro_noise = self._random.uniform(
            -self._config.micro_noise,
            self._config.micro_noise,
        )

        raw_value = (
            self._config.baseline
            + slow_rhythm
            + fast_flutter
            + self._drift
            + self._surge
            + micro_noise
        )
        return _clamp(raw_value, self._config.min_value, self._config.max_value)
