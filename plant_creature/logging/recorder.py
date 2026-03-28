from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
    """Small JSONL recorder ready for the next logging pass."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def record(self, kind: str, payload: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        event = LogEvent.create(kind=kind, payload=payload)

        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event)))
            handle.write("\n")
