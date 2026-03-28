from __future__ import annotations

from dataclasses import dataclass

from plant_creature.presentation import CreaturePresentation


@dataclass(frozen=True)
class OLEDRegion:
    x: int
    y: int
    width: int
    height: int


TOP_BAND = OLEDRegion(x=0, y=0, width=128, height=16)
FACE_ZONE = OLEDRegion(x=0, y=16, width=128, height=32)
BOTTOM_BAND = OLEDRegion(x=0, y=48, width=128, height=16)


def build_proof_frame(presentation: CreaturePresentation) -> dict[str, object]:
    """Describe the small proof layout we will eventually draw on the OLED."""

    return {
        "top_band": {
            "region": TOP_BAND,
            "text": presentation.status_word,
            "source": presentation.source_label,
        },
        "face_zone": {
            "region": FACE_ZONE,
            "face_id": presentation.face_id,
            "trend": presentation.trend,
        },
        "bottom_band": {
            "region": BOTTOM_BAND,
            "utterance": presentation.utterance,
            "signal_bar": presentation.signal_bar,
            "flash": presentation.transition_flash,
        },
    }
