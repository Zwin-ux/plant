from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CreatureState(str, Enum):
    SLEEPY = "SLEEPY"
    CALM = "CALM"
    ACTIVE = "ACTIVE"
    ALERT = "ALERT"
    STRESSED = "STRESSED"
    RECOVERING = "RECOVERING"


@dataclass(frozen=True)
class CreatureSnapshot:
    state: CreatureState
    previous_state: CreatureState | None
    is_transition: bool = False
