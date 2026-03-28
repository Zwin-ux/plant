from __future__ import annotations

import argparse
import time

from config import APP_CONFIG, AppConfig
from plant_creature.outputs import ConsoleRenderer
from plant_creature.signals import SignalProcessor, SimulatedSignalProvider
from plant_creature.state import CreatureStateEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Plant Creature Alpha loop.")
    parser.add_argument(
        "--ticks",
        type=int,
        default=None,
        help="Run a fixed number of update cycles, then exit.",
    )
    return parser.parse_args()


def run(config: AppConfig, ticks: int | None = None) -> None:
    provider = SimulatedSignalProvider(config.signal)
    processor = SignalProcessor(config.signal)
    engine = CreatureStateEngine(config.thresholds)
    renderer = ConsoleRenderer(bar_width=config.console_bar_width)

    print("Plant Creature Alpha | simulation mode")
    print("Press Ctrl+C to stop.")

    cycle_count = 0

    while ticks is None or cycle_count < ticks:
        loop_started = time.monotonic()

        raw_value = provider.read()
        processed = processor.process(raw_value)
        snapshot = engine.evaluate(processed)

        print(renderer.render(processed, snapshot), flush=True)

        cycle_count += 1
        elapsed = time.monotonic() - loop_started
        sleep_for = max(0.0, config.signal.tick_seconds - elapsed)
        time.sleep(sleep_for)


def main() -> int:
    args = parse_args()

    try:
        run(APP_CONFIG, ticks=args.ticks)
    except KeyboardInterrupt:
        print("\nStopping Plant Creature Alpha.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
