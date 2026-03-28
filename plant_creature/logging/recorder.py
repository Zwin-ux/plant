from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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
    """Write line-delimited runtime events for later replay or analysis."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def record(self, kind: str, payload: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        event = LogEvent.create(kind=kind, payload=payload)

        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event)))
            handle.write("\n")

    def record_tick(self, signal: ProcessedSignal, snapshot: CreatureSnapshot) -> None:
        self.record(
            kind="tick",
            payload={
                "signal": {
                    "raw": round(signal.raw_value, 4),
                    "smoothed": round(signal.smoothed_value, 4),
                    "normalized": round(signal.normalized_value, 4),
                },
                "state": snapshot.state.value,
                "intensity": round(snapshot.intensity, 4),
            },
        )


class NullRecorder:
    """No-op recorder used when logging is disabled."""

    def record_tick(self, signal: ProcessedSignal, snapshot: CreatureSnapshot) -> None:
        del signal
        del snapshot
