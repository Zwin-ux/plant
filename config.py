from dataclasses import dataclass, field


@dataclass(frozen=True)
class SignalConfig:
    tick_seconds: float = 1.0
    min_value: float = 0.0
    max_value: float = 100.0
    baseline: float = 52.0
    smoothing_factor: float = 0.32
    wander_step: float = 2.8
    micro_noise: float = 1.6
    surge_chance_per_second: float = 0.08
    max_surge_strength: float = 18.0


@dataclass(frozen=True)
class StateThresholds:
    sleepy_max: float = 0.18
    calm_max: float = 0.38
    active_max: float = 0.62
    alert_max: float = 0.82


@dataclass(frozen=True)
class LoggingConfig:
    enabled_by_default: bool = False
    default_path: str = "logs/plant_creature.jsonl"


@dataclass(frozen=True)
class AppConfig:
    signal: SignalConfig = field(default_factory=SignalConfig)
    thresholds: StateThresholds = field(default_factory=StateThresholds)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    console_bar_width: int = 24


APP_CONFIG = AppConfig()
