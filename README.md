# Plant Creature Alpha

Plant Creature Alpha is a Raspberry Pi-based living-system prototype: a small digital organism that starts in simulation mode and later grows into a plant-linked biofeedback companion.

The current alpha is shaped more like a Tamagotchi crossed with a Pokewalker than a sensor dashboard. Raw inputs are processed into hidden creature drives, then surfaced as short moods, expressions, and tiny bits of language.

## Current status
- Raspberry Pi 5 setup is stable enough for software work
- SSH is working
- simulation-first runtime is live
- hardware-aware ADS1115, OLED, and LED boundaries exist
- tomorrow's first hardware set includes an ADS1115 ADC, SSD1306 OLED, WS2812 ring, capacitive moisture sensors, breadboards, and jumper wires

## Creature loop

The runtime now follows a five-layer loop:

```text
input -> processing -> fusion drives -> public state -> presentation -> expression
```

What that means in practice:

- `signals/` reads simulated input now, with ADS1115 support prepared for later
- `signals/processor.py` smooths and normalizes raw values
- `fusion/` converts those values into hidden drives:
  - hydration
  - stability
  - energy
  - bond
  - stress_load
- `state/` maps the hidden drives into public creature states:
  - `SLEEPY`
  - `CALM`
  - `ACTIVE`
  - `ALERT`
  - `STRESSED`
  - `RECOVERING`
- `presentation.py` turns state into creature-readable output data
- `outputs/` renders that presentation to the console today, with OLED and LED surfaces scaffolded for tomorrow

## Important scope note

This repo does **not** include actual [TRIBE v2](https://github.com/facebookresearch/tribev2) code, weights, or dependencies.

TRIBE is inspiration here, not runtime infrastructure. The current repo uses a lightweight hidden-drive fusion layer that fits a Raspberry Pi 5 and keeps the project simulation-first.

## Project structure

```text
plant/
  .gitignore
  README.md
  SOURCES.md
  DECISIONS.md
  TODO.md
  HANDOFF_CHATGPT.md
  requirements.txt
  main.py
  config.py
  scripts/
    sync_to_pi.ps1
    run_pi_smoke.ps1
    bootstrap_pi.sh
    pi_status.ps1
  plant_creature/
    __init__.py
    fusion/
      __init__.py
      drives.py
      interpreter.py
    logging/
      __init__.py
      recorder.py
    memory/
      __init__.py
      session.py
    outputs/
      __init__.py
      base.py
      console.py
      led_ring.py
      oled.py
      oled_layouts.py
      voice.py
    presentation.py
    signals/
      __init__.py
      ads1115.py
      base.py
      processor.py
      simulated.py
    state/
      __init__.py
      engine.py
      models.py
```

## What the current scaffold does

- generates a living-feeling simulated signal
- smooths and normalizes it
- interprets it through hidden drives instead of direct state thresholds
- produces short, creature-readable phrases
- renders a concise console expression once per tick
- logs signal, drives, state, and presentation data to JSONL when enabled
- keeps OLED and LED ring code side-by-side as optional hardware scaffolds

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Short simulation run:

```bash
python3 main.py --ticks 10
```

Run with JSONL logging:

```bash
python3 main.py --ticks 10 --log-file logs/dev.jsonl
```

Probe the future ADS1115 path:

```bash
python3 main.py --ticks 1 --signal-source ads1115
```

If the optional hardware libraries or the ADC are not available yet, that command should fail gracefully with a clear message.

## Pi workflow

GitHub remains the default source of truth:

```bash
ssh pi@192.168.137.142
cd /home/pi/plant
git pull --ff-only
bash scripts/bootstrap_pi.sh
source .venv/bin/activate
python main.py --ticks 10
```

For fast local iteration from Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync_to_pi.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\run_pi_smoke.ps1 -SkipPull
powershell -ExecutionPolicy Bypass -File .\scripts\run_pi_smoke.ps1 -SignalSource ads1115
powershell -ExecutionPolicy Bypass -File .\scripts\pi_status.ps1
```

## Advisor handoff

Use `HANDOFF_CHATGPT.md` when you want ChatGPT to stay aligned with the actual machine state, the current repo status, and the hardware arriving tomorrow.
