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
class FusionConfig:
    drive_smoothing_alpha: float = 0.18
    stability_window: float = 0.18
    stable_streak_goal_ticks: int = 300
    stable_threshold: float = 0.6
    stress_peak_decay: float = 0.96


@dataclass(frozen=True)
class StateConfig:
    min_dwell_ticks: int = 5
    recovering_min_ticks: int = 3


@dataclass(frozen=True)
class LoggingConfig:
    enabled_by_default: bool = False
    default_path: str = "logs/plant_creature.jsonl"


@dataclass(frozen=True)
class ADS1115Config:
    address: int = 0x48
    channel: int = 0
    gain: int = 1
    data_rate: int = 128
    input_min_voltage: float = 0.0
    input_max_voltage: float = 3.3


@dataclass(frozen=True)
class OLEDConfig:
    address: int = 0x3C
    width: int = 128
    height: int = 64


@dataclass(frozen=True)
class LedRingConfig:
    pixel_count: int = 16
    brightness: float = 0.2
    gpio_pin: int = 18


@dataclass(frozen=True)
class AppConfig:
    signal: SignalConfig = field(default_factory=SignalConfig)
    fusion: FusionConfig = field(default_factory=FusionConfig)
    state: StateConfig = field(default_factory=StateConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    ads1115: ADS1115Config = field(default_factory=ADS1115Config)
    oled: OLEDConfig = field(default_factory=OLEDConfig)
    led_ring: LedRingConfig = field(default_factory=LedRingConfig)
    console_bar_width: int = 24


APP_CONFIG = AppConfig()
