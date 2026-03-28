from __future__ import annotations

from plant_creature.signals import ProcessedSignal
from plant_creature.state import CreatureSnapshot, CreatureState


class ConsoleRenderer:
    _MOODS = {
        CreatureState.SLEEPY: "(-.-)",
        CreatureState.CALM: "(o_o)",
        CreatureState.ACTIVE: "(^_^)",
        CreatureState.ALERT: "(O_O)",
        CreatureState.STRESSED: "(>_<)",
    }

    def __init__(self, bar_width: int = 24) -> None:
        self._bar_width = bar_width

    def render(self, signal: ProcessedSignal, snapshot: CreatureSnapshot) -> str:
        timestamp = signal.timestamp.astimezone().strftime("%H:%M:%S")
        mood = self._MOODS[snapshot.state]
        meter = self._meter(snapshot.intensity)

        return (
            f"[{timestamp}] "
            f"{snapshot.state.value:<8} "
            f"{mood} "
            f"raw={signal.raw_value:5.1f} "
            f"smooth={signal.smoothed_value:5.1f} "
            f"signal={meter} "
            f"{snapshot.intensity * 100:5.1f}%"
        )

    def _meter(self, intensity: float) -> str:
        filled = round(intensity * self._bar_width)
        filled = max(0, min(self._bar_width, filled))
        empty = self._bar_width - filled
        return "[" + ("#" * filled) + ("-" * empty) + "]"
