from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from config import APP_CONFIG, AppConfig
from plant_creature.fusion import DriveInterpreter
from plant_creature.logging import JsonlRecorder, NullRecorder
from plant_creature.memory import SessionTracker
from plant_creature.outputs import ConsoleRenderer, UtteranceGenerator
from plant_creature.presentation import PresentationComposer
from plant_creature.signals import (
    ADS1115SignalProvider,
    SignalProcessor,
    SignalProvider,
    SignalProviderUnavailable,
    SimulatedSignalProvider,
)
from plant_creature.state import CreatureStateEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Plant Creature Alpha loop.")
    parser.add_argument(
        "--ticks",
        type=int,
        default=None,
        help="Run a fixed number of update cycles, then exit.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Write JSONL creature logs to the given file.",
    )
    parser.add_argument(
        "--signal-source",
        choices=("simulated", "ads1115"),
        default="simulated",
        help="Choose which signal provider to run.",
    )
    return parser.parse_args()


def build_recorder(config: AppConfig, log_file: Path | None) -> JsonlRecorder | NullRecorder:
    if log_file is not None:
        return JsonlRecorder(log_file)
    if config.logging.enabled_by_default:
        return JsonlRecorder(config.logging.default_path)
    return NullRecorder()


def build_signal_provider(config: AppConfig, signal_source: str) -> SignalProvider:
    if signal_source == "ads1115":
        return ADS1115SignalProvider(
            signal_config=config.signal,
            hardware_config=config.ads1115,
        )
    return SimulatedSignalProvider(config.signal)


def source_label(signal_source: str) -> str:
    return "ADC" if signal_source == "ads1115" else "SIM"


def run(
    config: AppConfig,
    ticks: int | None = None,
    log_file: Path | None = None,
    signal_source: str = "simulated",
) -> None:
    provider = build_signal_provider(config, signal_source)
    processor = SignalProcessor(config.signal)
    interpreter = DriveInterpreter(config.fusion)
    session_tracker = SessionTracker(config.fusion)
    engine = CreatureStateEngine(config.state)
    presenter = PresentationComposer(UtteranceGenerator())
    output = ConsoleRenderer(bar_width=config.console_bar_width)
    recorder = build_recorder(config, log_file)

    print(f"Plant Creature Alpha | {signal_source} source")
    print("Press Ctrl+C to stop.")

    cycle_count = 0

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
            source_label=source_label(signal_source),
        )

        output.emit(presentation)
        recorder.record_tick(processed, fusion, snapshot, presentation, session)

        cycle_count += 1
        elapsed = time.monotonic() - loop_started
        sleep_for = max(0.0, config.signal.tick_seconds - elapsed)
        time.sleep(sleep_for)


def main() -> int:
    args = parse_args()

    try:
        run(
            APP_CONFIG,
            ticks=args.ticks,
            log_file=args.log_file,
            signal_source=args.signal_source,
        )
    except SignalProviderUnavailable as exc:
        print(f"Signal source unavailable: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nStopping Plant Creature Alpha.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
