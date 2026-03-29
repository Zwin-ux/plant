# Core Cube / Plant Creature Alpha

Core Cube is a Raspberry Pi-based signal creature: a small living-feeling system that turns input signals into mood, language, and future physical expression.

The runtime is designed to work cleanly with zero hardware attached. Swapping in real hardware (e.g. the ADS1115) requires no changes to the engine.

## Architecture

The live pipeline is:

```text
signal source -> processor -> creature engine -> presentation -> outputs/logs
```

The current repo keeps that split like this:

- `plant_creature/signals/`
  - simulated input profiles
  - ADS1115 provider boundary
  - smoothing / normalization
- `plant_creature/fusion/`
  - hidden drive shaping for the creature
- `plant_creature/state/`
  - public creature states
- `plant_creature/presentation.py`
  - output-facing presentation model
- `plant_creature/outputs/`
  - console output
  - OLED / LED ring placeholders
- `plant_creature/services/runtime.py`
  - runtime orchestration
- `plant_creature/logging/`
  - JSONL event logging

## Creature states

The public creature states are intentionally simple and readable:

- `CALM`
- `THIRSTY`
- `RECOVERING`
- `ALERT`
- `OVERLOADED`

Each tick produces a presentation object with:

- state label
- intensity
- short text
- color intent
- animation intent
- trend

That keeps OLED and LED ring work decoupled from engine internals.

## Simulation mode

Simulation is the default and requires no hardware libraries.

Available profiles:

- `healthy`
- `dry`
- `recovering`
- `unstable`
- `overloaded`

These profiles let you rehearse hardware scenarios in the terminal before connecting any hardware.

## Run in the Pi venv

```bash
cd ~/plant
source .venv/bin/activate
python main.py
```

Useful runs:

```bash
python main.py --ticks 10
python main.py --ticks 10 --simulation-profile dry
python main.py --ticks 14 --simulation-profile recovering
python main.py --ticks 12 --simulation-profile unstable
python main.py --ticks 8 --simulation-profile overloaded
python main.py --ticks 10 --log-file logs/dev.jsonl
```

Deterministic simulation for a repeatable run:

```bash
python main.py --ticks 12 --simulation-profile dry --simulation-seed 7
```

## ADS1115 hardware path

The real soil moisture path is prepared but optional.

To use it:

```bash
python main.py --ticks 1 --signal-source ads1115
```

If the hardware libraries or I2C device are missing, this fails gracefully.

To install the ADS1115 library inside the venv:

```bash
pip install adafruit-circuitpython-ads1x15
```

Then verify the bus on the Pi:

```bash
i2cdetect -y 1
```

Target hardware setup:

- ADS1115 on I2C
- one soil moisture sensor on A0
- normalized output fed into the same runtime used by simulation

## Logging

JSONL logs capture:

- runtime startup / shutdown
- raw and normalized values
- hidden drives
- current state
- state transitions
- presentation intent
- source mode

This makes hardware readings much easier to debug when switching from simulation to real sensor input.

## Important scope note

This is not a dashboard project.
This is not a one-off sensor script.

The current output is terminal-first on purpose: it should feel like a creature with a pulse, not a table of metrics.
