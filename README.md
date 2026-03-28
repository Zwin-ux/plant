# Plant Creature Alpha

Plant Creature Alpha is a Raspberry Pi-based living-system prototype: a digital creature that begins in simulation mode and later evolves into a plant biofeedback-driven organism.

## Current status
- Raspberry Pi 5 setup in progress
- SSH working
- Software scaffold under active development
- Hardware integration planned after core simulation pipeline is stable
- Tomorrow's first hardware set includes an ADS1115 ADC, SSD1306 OLED, WS2812 ring, capacitive moisture sensors, breadboards, and jumper wires

## Goals
- simulation-first signal pipeline
- modular creature state engine
- swappable real sensor input later
- local logging and expressive output

## What the current scaffold does

The current Phase 1 scaffold focuses on a runnable core:

- a simulated signal source that feels alive instead of purely random
- a processor that smooths and normalizes the signal
- a creature state engine with `SLEEPY`, `CALM`, `ACTIVE`, `ALERT`, and `STRESSED`
- expressive console output
- opt-in JSONL logging
- Pi deployment scripts for bootstrap, sync, and smoke tests

## Project structure

```text
plant/
  .gitignore
  README.md
  SOURCES.md
  DECISIONS.md
  TODO.md
  requirements.txt
  main.py
  config.py
  scripts/
    sync_to_pi.ps1
    run_pi_smoke.ps1
    bootstrap_pi.sh
  plant_creature/
    __init__.py
    signals/
      __init__.py
      base.py
      simulated.py
      processor.py
    state/
      __init__.py
      engine.py
      models.py
    outputs/
      __init__.py
      console.py
    logging/
      __init__.py
      recorder.py
```

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Run a short test loop:

```bash
python3 main.py --ticks 10
```

Run with logging:

```bash
python3 main.py --ticks 10 --log-file logs/dev.jsonl
```

## Pi workflow

GitHub is the default source of truth:

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
powershell -ExecutionPolicy Bypass -File .\scripts\pi_status.ps1
```

## Advisor handoff

Use `HANDOFF_CHATGPT.md` when you want ChatGPT to stay aligned with the actual machine state, the current repo status, and the hardware arriving next.
