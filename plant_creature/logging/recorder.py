from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from plant_creature.fusion import FusionSnapshot
from plant_creature.memory import SessionMemory
from plant_creature.presentation import CreaturePresentation
from plant_creature.signals import ProcessedSignal
from plant_creature.state import CreatureSnapshot


@dataclass(frozen=True)
class LogEvent:
    timestamp: str
    kind: str
    payload: dict[str, Any]

    @classmethod
    def create(cls, kind: str, payload: dict[str, Any]) -> "LogEvent":
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(),
            kind=kind,
            payload=payload,
        )


class JsonlRecorder:
    """Write line-delimited creature events for replay or later analysis."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def record(self, kind: str, payload: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        event = LogEvent.create(kind=kind, payload=payload)

        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event)))
            handle.write("\n")

    def record_runtime_event(self, kind: str, payload: dict[str, Any]) -> None:
        self.record(kind=kind, payload=payload)

    def record_tick(
        self,
        signal: ProcessedSignal,
        fusion: FusionSnapshot,
        snapshot: CreatureSnapshot,
        presentation: CreaturePresentation,
        session: SessionMemory,
    ) -> None:
        payload = {
            "signal": {
                "raw": round(signal.raw_value, 4),
                "smoothed": round(signal.smoothed_value, 4),
                "normalized": round(signal.normalized_value, 4),
            },
            "drives": fusion.drives.as_dict(),
            "state": snapshot.state.value,
            "previous_state": (
                None if snapshot.previous_state is None else snapshot.previous_state.value
            ),
            "transition": snapshot.is_transition,
            "presentation": {
                "status_word": presentation.status_word,
                "intensity": round(presentation.intensity, 4),
                "face_id": presentation.face_id,
                "utterance": presentation.utterance,
                "signal_bar": presentation.signal_bar,
                "trend": presentation.trend,
                "transition_flash": presentation.transition_flash,
                "aura_pattern": presentation.aura_pattern.value,
                "color_intent": presentation.color_intent,
                "animation_intent": presentation.animation_intent,
                "source_label": presentation.source_label,
            },
            "session": {
                "tick_count": session.tick_count,
                "stable_streak_ticks": session.stable_streak_ticks,
                "stress_streak_ticks": session.stress_streak_ticks,
                "recent_peak_stress": round(session.recent_peak_stress, 4),
                "recovery_count": session.recovery_count,
            },
        }
        self.record(kind="tick", payload=payload)

        if snapshot.is_transition:
            self.record(
                kind="state_transition",
                payload={
                    "from": (
                        None if snapshot.previous_state is None else snapshot.previous_state.value
                    ),
                    "to": snapshot.state.value,
                    "utterance": presentation.utterance,
                    "aura_pattern": presentation.aura_pattern.value,
                    "source_label": presentation.source_label,
                    "tick_count": session.tick_count,
                },
            )


class NullRecorder:
    """No-op recorder used when logging is disabled."""

    def record_runtime_event(self, kind: str, payload: dict[str, Any]) -> None:
        del kind
        del payload

    def record_tick(
        self,
        signal: ProcessedSignal,
        fusion: FusionSnapshot,
        snapshot: CreatureSnapshot,
        presentation: CreaturePresentation,
        session: SessionMemory,
    ) -> None:
        del signal
        del fusion
        del snapshot
        del presentation
        del session
