from __future__ import annotations

import argparse
import sys
from pathlib import Path

from config import APP_CONFIG, AppConfig
from plant_creature.logging import JsonlRecorder, NullRecorder
from plant_creature.services import CreatureRuntime
from plant_creature.services.runtime import simulation_profile_choices
from plant_creature.signals import SignalProviderUnavailable


def parse_args(config: AppConfig) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Core Cube creature runtime.")
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
        default=config.input_mode,
        help="Choose which signal provider to run.",
    )
    parser.add_argument(
        "--simulation-profile",
        choices=simulation_profile_choices(),
        default=config.simulation.profile,
        help="Choose the simulated signal profile for no-hardware runs.",
    )
    parser.add_argument(
        "--simulation-seed",
        type=int,
        default=config.simulation.seed,
        help="Optional seed for deterministic simulation runs.",
    )
    return parser.parse_args()


def build_recorder(config: AppConfig, log_file: Path | None) -> JsonlRecorder | NullRecorder:
    if log_file is not None:
        return JsonlRecorder(log_file)
    if config.logging.enabled_by_default:
        return JsonlRecorder(config.logging.default_path)
    return NullRecorder()


def main() -> int:
    args = parse_args(APP_CONFIG)
    recorder = build_recorder(APP_CONFIG, args.log_file)

    try:
        runtime = CreatureRuntime(
            APP_CONFIG,
            recorder=recorder,
            signal_source=args.signal_source,
            simulation_profile=args.simulation_profile,
            simulation_seed=args.simulation_seed,
        )
        runtime.run(ticks=args.ticks)
    except SignalProviderUnavailable as exc:
        print(f"Signal source unavailable: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nStopping Core Cube.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
