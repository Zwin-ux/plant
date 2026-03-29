from __future__ import annotations

from plant_creature.presentation import CreaturePresentation


class ConsoleRenderer:
    _FACES = {
        "calm": "(o_o)",
        "calm_warm": "(u_u)",
        "thirsty": "(._.)",
        "recovering": "(^_^)",
        "recovering_warm": "(^.^)",
        "alert": "(O_O)",
        "overloaded": "(>_<)",
    }

    def __init__(self, bar_width: int = 24, bar_steps: int = 8) -> None:
        self._bar_width = bar_width
        self._bar_steps = bar_steps

    def render(self, presentation: CreaturePresentation) -> str:
        flash = ">>" if presentation.transition_flash else "  "
        face = self._FACES.get(presentation.face_id, "(o_o)")
        meter = self._meter(presentation.signal_bar)
        signal_percent = round((presentation.signal_bar / self._bar_steps) * 100)

        return (
            f"{flash} "
            f"{presentation.status_word:<8} "
            f"{face} "
            f"{presentation.utterance:<16} "
            f"sig={signal_percent:>3}% "
            f"{meter} "
            f"int={presentation.intensity:0.2f} "
            f"trend={presentation.trend:<7} "
            f"color={presentation.color_intent:<6} "
            f"anim={presentation.animation_intent:<12} "
            f"src={presentation.source_label}"
        )

    def _meter(self, signal_bar: int) -> str:
        filled = round((signal_bar / self._bar_steps) * self._bar_width)
        filled = max(0, min(self._bar_width, filled))
        empty = self._bar_width - filled
        return "[" + ("#" * filled) + ("-" * empty) + "]"

    def emit(self, presentation: CreaturePresentation) -> None:
        print(self.render(presentation), flush=True)
