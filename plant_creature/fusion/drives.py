from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreatureDrives:
    hydration: float
    stability: float
    energy: float
    bond: float
    stress_load: float

    def as_dict(self) -> dict[str, float]:
        return {
            "hydration": round(self.hydration, 4),
            "stability": round(self.stability, 4),
            "energy": round(self.energy, 4),
            "bond": round(self.bond, 4),
            "stress_load": round(self.stress_load, 4),
        }


@dataclass(frozen=True)
class FusionSnapshot:
    drives: CreatureDrives
    targets: CreatureDrives
    normalized_delta: float
    trend: str
