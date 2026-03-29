from __future__ import annotations

import time
from dataclasses import replace

from config import AppConfig
from plant_creature.fusion import DriveInterpreter
from plant_creature.logging import JsonlRecorder, NullRecorder
from plant_creature.memory import SessionTracker
from plant_creature.outputs import ConsoleRenderer, UtteranceGenerator
from plant_creature.presentation import PresentationComposer
from plant_creature.signals import (
    ADS1115SignalProvider,
    SUPPORTED_SIMULATION_PROFILES,
    SignalProcessor,
    SignalProvider,
    SignalProviderUnavailable,
    SimulatedSignalProvider,
)
from plant_creature.state import CreatureStateEngine


class CreatureRuntime:
    """Run the creature pipeline end-to-end while keeping main.py tiny."""

    def __init__(
        self,
        config: AppConfig,
        recorder: JsonlRecorder | NullRecorder,
        signal_source: str,
        simulation_profile: str,
        simulation_seed: int | None,
    ) -> None:
        self._config = config
        self._recorder = recorder
        self._signal_source = signal_source
        self._simulation_profile = simulation_profile
        self._simulation_seed = simulation_seed

    def run(self, ticks: int | None = None) -> None:
        self._recorder.record_runtime_event(
            "runtime_started",
            {
                "signal_source": self._signal_source,
                "simulation_profile": self._simulation_profile,
                "simulation_seed": self._simulation_seed,
            },
        )

        provider = self._build_signal_provider()
        processor = SignalProcessor(self._config.signal)
        interpreter = DriveInterpreter(self._config.fusion)
        session_tracker = SessionTracker(self._config.fusion)
        engine = CreatureStateEngine(self._config.state)
        presenter = PresentationComposer(UtteranceGenerator())
        output = ConsoleRenderer(bar_width=self._config.console_bar_width)

        print(
            f"Core Cube | source={self._signal_source} | profile={self._simulation_profile}",
            flush=True,
        )
        print("Press Ctrl+C to stop.", flush=True)

        cycle_count = 0
        try:
            while ticks is None or cycle_count < ticks:
                loop_started = time.monotonic()
                session = session_tracker.memory

                sample = provider.read()
                processed = processor.process(sample)
                fusion = interpreter.interpret(processed, session)
                snapshot = engine.evaluate(fusion.drives, session)
                session = session_tracker.update(fusion.drives, snapshot)
                presentation = presenter.compose(
                    processed,
                    fusion,
                    snapshot,
                    tick_count=session.tick_count,
                    source_label=self._source_label(),
                )

                output.emit(presentation)
                self._recorder.record_tick(processed, fusion, snapshot, presentation, session)

                cycle_count += 1
                elapsed = time.monotonic() - loop_started
                sleep_for = max(0.0, self._config.signal.tick_seconds - elapsed)
                time.sleep(sleep_for)
        finally:
            self._recorder.record_runtime_event(
                "runtime_stopped",
                {
                    "signal_source": self._signal_source,
                    "ticks_completed": cycle_count,
                },
            )

    def _build_signal_provider(self) -> SignalProvider:
        if self._signal_source == "ads1115":
            try:
                return ADS1115SignalProvider(
                    signal_config=self._config.signal,
                    hardware_config=self._config.ads1115,
                )
            except SignalProviderUnavailable as exc:
                self._recorder.record_runtime_event(
                    "provider_unavailable",
                    {
                        "signal_source": self._signal_source,
                        "message": str(exc),
                    },
                )
                raise

        simulation_config = replace(
            self._config.simulation,
            profile=self._simulation_profile,
            seed=self._simulation_seed,
        )
        return SimulatedSignalProvider(
            self._config.signal,
            simulation_config,
        )

    def _source_label(self) -> str:
        return "ADC" if self._signal_source == "ads1115" else "SIM"


def simulation_profile_choices() -> tuple[str, ...]:
    return SUPPORTED_SIMULATION_PROFILES
