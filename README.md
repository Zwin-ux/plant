# Plant Creature Alpha

Plant Creature Alpha is a Raspberry Pi-based living-system prototype: a digital creature that begins in simulation mode and later evolves into a plant biofeedback-driven organism.

## Current status
- Raspberry Pi 5 setup in progress
- SSH working
- Software scaffold under active development
- Hardware integration planned after core simulation pipeline is stable

## Goals
- simulation-first signal pipeline
- modular creature state engine
- swappable real sensor input later
- local logging and expressive output

## What the current scaffold does

The first clean commit focuses on a runnable core:

- a simulated signal source that feels alive instead of purely random
- a processor that smooths and normalizes the signal
- a creature state engine with `SLEEPY`, `CALM`, `ACTIVE`, `ALERT`, and `STRESSED`
- expressive console output
- a logging module ready for the next pass

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
  plant_creature/
    __init__.py
    signals/
      __init__.py
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

## Run

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Run a short test loop:

```bash
python3 main.py --ticks 10
```
