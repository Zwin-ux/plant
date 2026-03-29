# Core Cube / Plant Creature Alpha

Core Cube is a Raspberry Pi-based signal creature: a small living-feeling system that turns input signals into mood, language, and future physical expression.

Tonight's goal is software confidence, not breadboard heroics. The runtime must work cleanly with zero hardware attached, then swap to ADS1115 input tomorrow without changing the engine.

## Current architecture

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
  - console output today
  - OLED / LED ring placeholders for tomorrow
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

That keeps tomorrow's OLED and LED ring work decoupled from engine internals.

## Simulation mode

Simulation is the default and requires no hardware libraries.

Profiles available tonight:

- `healthy`
- `dry`
- `recovering`
- `unstable`
- `overloaded`

These are meant to rehearse tomorrow's hardware scenarios in the terminal before anything touches the breadboard.

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

Deterministic simulation if you want a repeatable rehearsal:

```bash
python main.py --ticks 12 --simulation-profile dry --simulation-seed 7
```

## Tomorrow's ADS1115 path

The real soil moisture path is prepared but still optional.

Current command:

```bash
python main.py --ticks 1 --signal-source ads1115
```

Right now that should fail gracefully if the hardware libraries or I2C device are missing.

Tomorrow's flow:

```bash
cd ~/plant
source .venv/bin/activate
python main.py --ticks 1 --signal-source ads1115
```

If the ADS1115 stack is not installed yet, install it inside the venv:

```bash
pip install adafruit-circuitpython-ads1x15
```

Then verify the bus on the Pi:

```bash
i2cdetect -y 1
```

Expected first target:

- ADS1115 on I2C
- one soil moisture sensor on A0
- normalized output fed into the same runtime used by simulation

## Logging

JSONL logs now capture:

- runtime startup / shutdown
- raw and normalized values
- hidden drives
- current state
- state transitions
- presentation intent
- source mode

That should make tomorrow's first hardware readings much easier to debug.

## Important scope note

This is not a dashboard project.
This is not a one-off sensor script.

The current output is terminal-first on purpose: it should feel like a creature with a pulse, not a table of metrics.
