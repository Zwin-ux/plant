from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CreatureState(str, Enum):
    CALM = "CALM"
    THIRSTY = "THIRSTY"
    RECOVERING = "RECOVERING"
    ALERT = "ALERT"
    OVERLOADED = "OVERLOADED"


@dataclass(frozen=True)
class CreatureSnapshot:
    state: CreatureState
    intensity: float
    previous_state: CreatureState | None
    is_transition: bool = False
