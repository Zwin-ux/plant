from __future__ import annotations

from plant_creature.state.models import CreatureState


class UtteranceGenerator:
    _PHRASES = {
        CreatureState.SLEEPY: {
            "idle": ("resting", "dim now", "slow breath"),
            "transition": ("getting sleepy", "night mode", "curling up"),
        },
        CreatureState.CALM: {
            "idle": ("steady", "here", "listening"),
            "transition": ("settled now", "all even", "holding"),
        },
        CreatureState.ACTIVE: {
            "idle": ("awake", "bright", "moving"),
            "transition": ("feeling up", "full of spark", "ready"),
        },
        CreatureState.ALERT: {
            "idle": ("watching", "on edge", "something changed"),
            "transition": ("what was that", "shift sensed", "checking"),
        },
        CreatureState.STRESSED: {
            "idle": ("too dry", "uneasy", "need balance"),
            "transition": ("stress spike", "not right", "help me"),
        },
        CreatureState.RECOVERING: {
            "idle": ("better", "coming back", "settling"),
            "transition": ("repairing", "returning", "softening"),
        },
    }

    def generate(self, state: CreatureState, tick_count: int, is_transition: bool) -> str:
        bucket = "transition" if is_transition else "idle"
        phrases = self._PHRASES[state][bucket]
        return phrases[tick_count % len(phrases)]
