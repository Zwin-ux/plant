from .models import CreatureSnapshot, CreatureState

__all__ = ["CreatureSnapshot", "CreatureState", "CreatureStateEngine"]


def __getattr__(name: str):
    if name == "CreatureStateEngine":
        from .engine import CreatureStateEngine

        return CreatureStateEngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
