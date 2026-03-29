# ChatGPT Advisor Handoff

Use this as the current truth snapshot for Core Cube / Plant Creature Alpha.

## Project role split

- Codex handles implementation, repo changes, deployment, and tomorrow's hardware hookup.
- ChatGPT is the advisor for creature behavior, calibration thinking, product direction, and emotional design.

## Current reality

- Canonical repo: `~/plant`
- Platform: Raspberry Pi 5
- Hardware work is intentionally paused for tonight
- Breadboard wiring is not considered stable yet
- The software must run cleanly with zero hardware dependencies
- ADS1115 is the next critical integration item and is expected tomorrow

## Current software shape

The repo now runs as:

```text
signal source -> processor -> creature engine -> presentation -> outputs/logs
```

Key pieces:

- `main.py` is orchestration-only
- `plant_creature/services/runtime.py` owns the runtime loop
- `plant_creature/signals/simulated.py` provides rehearsal profiles:
  - `healthy`
  - `dry`
  - `recovering`
  - `unstable`
  - `overloaded`
- `plant_creature/signals/ads1115.py` is the optional real input boundary
- `plant_creature/state/` exposes public states:
  - `CALM`
  - `THIRSTY`
  - `RECOVERING`
  - `ALERT`
  - `OVERLOADED`
- `plant_creature/presentation.py` creates output-facing presentation data
- `plant_creature/outputs/` is console-first, with OLED and LED placeholders still unwired
- `plant_creature/logging/recorder.py` writes startup, tick, transition, and shutdown events to JSONL

## How to run tonight

```bash
cd ~/plant
source .venv/bin/activate
python main.py
```

Helpful rehearsals:

```bash
python main.py --ticks 10 --simulation-profile healthy
python main.py --ticks 10 --simulation-profile dry
python main.py --ticks 14 --simulation-profile recovering
python main.py --ticks 12 --simulation-profile unstable
python main.py --ticks 8 --simulation-profile overloaded
python main.py --ticks 10 --log-file logs/dev.jsonl
```

## Tomorrow's hardware path

Do not assume this is already wired.

The prepared path is:

- ADS1115 on I2C
- one capacitive soil moisture sensor on A0
- normalized reading into the same input contract used by simulation

Current probe command:

```bash
python main.py --ticks 1 --signal-source ads1115
```

If optional libraries are missing, that graceful failure is expected tonight.

## Guardrails for advice

Please keep advice aligned with these constraints:

- no hardware assumptions tonight
- no dashboard-first thinking
- no giant frameworks
- no fake scientific claims
- keep the engine hardware-agnostic
- optimize for tomorrow-readiness and confidence

## Good advice targets right now

- how to interpret soil moisture into creature behavior
- what the first LED ring aura mappings should be
- what one OLED proof screen should show later
- how to calibrate "dry" vs "healthy" safely once ADS1115 is live
- how to keep the creature expressive without turning it into a metrics wall
