from __future__ import annotations

from typing import Any

from config import ADS1115Config, SignalConfig

from .base import SignalProviderUnavailable, SignalSample


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


class ADS1115SignalProvider:
    """
    Generic ADS1115-backed analog signal provider.

    This path is intentionally generic for the first hardware pass. It prepares a
    reusable analog input boundary before sensor-specific calibration logic exists.
    """

    def __init__(self, signal_config: SignalConfig, hardware_config: ADS1115Config) -> None:
        if hardware_config.input_max_voltage <= hardware_config.input_min_voltage:
            raise ValueError("ADS1115 input_max_voltage must be greater than input_min_voltage.")

        self._signal_config = signal_config
        self._hardware_config = hardware_config

        try:
            board, busio, ads_module, analog_in = self._load_dependencies()
            channel_name = f"P{hardware_config.channel}"
            channel_id = getattr(ads_module, channel_name, None)
            if channel_id is None:
                raise SignalProviderUnavailable(
                    f"Unsupported ADS1115 channel {hardware_config.channel}. Expected 0-3."
                )

            i2c = busio.I2C(board.SCL, board.SDA)
            ads = ads_module.ADS1115(i2c, address=hardware_config.address)
            ads.gain = hardware_config.gain
            ads.data_rate = hardware_config.data_rate
            self._channel = analog_in.AnalogIn(ads, channel_id)
        except SignalProviderUnavailable:
            raise
        except Exception as exc:
            raise SignalProviderUnavailable(f"ADS1115 not ready: {exc}") from exc

    @classmethod
    def probe(cls, hardware_config: ADS1115Config) -> tuple[bool, str]:
        try:
            board, busio, ads_module, analog_in = cls._load_dependencies()
            channel_name = f"P{hardware_config.channel}"
            channel_id = getattr(ads_module, channel_name, None)
            if channel_id is None:
                return False, f"Unsupported ADS1115 channel {hardware_config.channel}."

            i2c = busio.I2C(board.SCL, board.SDA)
            ads = ads_module.ADS1115(i2c, address=hardware_config.address)
            analog_in.AnalogIn(ads, channel_id)
            return True, "ADS1115 provider is available."
        except SignalProviderUnavailable as exc:
            return False, str(exc)
        except Exception as exc:
            return False, f"ADS1115 not ready: {exc}"

    @staticmethod
    def _load_dependencies() -> tuple[Any, Any, Any, Any]:
        try:
            import board
            import busio
            import adafruit_ads1x15.ads1115 as ads_module
            from adafruit_ads1x15 import analog_in
        except ImportError as exc:
            missing = exc.name or "hardware library"
            raise SignalProviderUnavailable(
                "ADS1115 support requires optional libraries "
                f"(missing: {missing})."
            ) from exc

        return board, busio, ads_module, analog_in

    def read(self) -> SignalSample:
        voltage = float(self._channel.voltage)
        fraction = (
            voltage - self._hardware_config.input_min_voltage
        ) / (
            self._hardware_config.input_max_voltage - self._hardware_config.input_min_voltage
        )
        fraction = _clamp(fraction, 0.0, 1.0)

        raw_value = self._signal_config.min_value + fraction * (
            self._signal_config.max_value - self._signal_config.min_value
        )
        return SignalSample.now(raw_value=raw_value)
