from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from plant_creature.fusion import FusionSnapshot
from plant_creature.signals import ProcessedSignal
from plant_creature.state import CreatureSnapshot, CreatureState


class AuraPattern(str, Enum):
    BREATH = "breath"
    PULSE = "pulse"
    NARROW_PULSE = "narrow_pulse"
    FLICKER = "flicker"
    SOFTEN = "soften"


@dataclass(frozen=True)
class CreaturePresentation:
    state: CreatureState
    status_word: str
    intensity: float
    face_id: str
    utterance: str
    signal_bar: int
    trend: str
    transition_flash: bool
    aura_pattern: AuraPattern
    color_intent: str
    animation_intent: str
    source_label: str


class UtteranceProvider(Protocol):
    def generate(self, state: CreatureState, tick_count: int, is_transition: bool) -> str:
        """Return a short creature utterance for the current tick."""


class PresentationComposer:
    _STATUS_WORDS = {
        CreatureState.CALM: "CALM",
        CreatureState.THIRSTY: "THIRSTY",
        CreatureState.RECOVERING: "HEALING",
        CreatureState.ALERT: "ALERT",
        CreatureState.OVERLOADED: "OVERLOAD",
    }

    _FACE_IDS = {
        CreatureState.CALM: "calm",
        CreatureState.THIRSTY: "thirsty",
        CreatureState.RECOVERING: "recovering",
        CreatureState.ALERT: "alert",
        CreatureState.OVERLOADED: "overloaded",
    }

    _AURA_PATTERNS = {
        CreatureState.CALM: AuraPattern.BREATH,
        CreatureState.THIRSTY: AuraPattern.PULSE,
        CreatureState.RECOVERING: AuraPattern.SOFTEN,
        CreatureState.ALERT: AuraPattern.NARROW_PULSE,
        CreatureState.OVERLOADED: AuraPattern.FLICKER,
    }

    _COLOR_INTENTS = {
        CreatureState.CALM: "blue",
        CreatureState.THIRSTY: "orange",
        CreatureState.RECOVERING: "teal",
        CreatureState.ALERT: "yellow",
        CreatureState.OVERLOADED: "red",
    }

    _ANIMATION_INTENTS = {
        CreatureState.CALM: "slow-breathe",
        CreatureState.THIRSTY: "slow-pulse",
        CreatureState.RECOVERING: "soft-rise",
        CreatureState.ALERT: "narrow-pulse",
        CreatureState.OVERLOADED: "hard-flicker",
    }

    def __init__(self, utterances: UtteranceProvider, bar_steps: int = 8) -> None:
        self._utterances = utterances
        self._bar_steps = bar_steps

    def compose(
        self,
        signal: ProcessedSignal,
        fusion: FusionSnapshot,
        snapshot: CreatureSnapshot,
        tick_count: int,
        source_label: str,
    ) -> CreaturePresentation:
        face_id = self._FACE_IDS[snapshot.state]
        if (
            fusion.drives.bond >= 0.65
            and snapshot.state in {CreatureState.CALM, CreatureState.RECOVERING}
        ):
            face_id = f"{face_id}_warm"

        aura_pattern = self._AURA_PATTERNS[snapshot.state]
        return CreaturePresentation(
            state=snapshot.state,
            status_word=self._STATUS_WORDS[snapshot.state],
            intensity=round(snapshot.intensity, 4),
            face_id=face_id,
            utterance=self._utterances.generate(
                snapshot.state,
                tick_count=tick_count,
                is_transition=snapshot.is_transition,
            ),
            signal_bar=max(0, min(self._bar_steps, round(signal.normalized_value * self._bar_steps))),
            trend=fusion.trend,
            transition_flash=snapshot.is_transition,
            aura_pattern=aura_pattern,
            color_intent=self._COLOR_INTENTS[snapshot.state],
            animation_intent=self._ANIMATION_INTENTS[snapshot.state],
            source_label=source_label.upper(),
        )
