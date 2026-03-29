from __future__ import annotations

from plant_creature.state.models import CreatureState


class UtteranceGenerator:
    _PHRASES = {
        CreatureState.CALM: {
            "idle": ("steady now", "holding level", "rooted"),
            "transition": ("settling in", "back to center", "easing down"),
        },
        CreatureState.THIRSTY: {
            "idle": ("need water", "running dry", "low reserve"),
            "transition": ("getting thirsty", "drying out", "need a drink"),
        },
        CreatureState.RECOVERING: {
            "idle": ("better now", "coming back", "soaking in"),
            "transition": ("recovering", "picking up", "stabilizing"),
        },
        CreatureState.ALERT: {
            "idle": ("watching shifts", "not stable", "something changed"),
            "transition": ("signal wobble", "that moved", "checking flow"),
        },
        CreatureState.OVERLOADED: {
            "idle": ("too much", "over limit", "signal spike"),
            "transition": ("overloaded", "too intense", "pulling back"),
        },
    }

    def generate(self, state: CreatureState, tick_count: int, is_transition: bool) -> str:
        bucket = "transition" if is_transition else "idle"
        phrases = self._PHRASES[state][bucket]
        return phrases[tick_count % len(phrases)]
