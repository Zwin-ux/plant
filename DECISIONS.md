# Decisions

## Simulation-first architecture

The project starts in simulation mode so software can evolve before the hardware stack is complete.

## Small modular packages

The codebase is split into:

- `signals` for input generation and processing
- `state` for creature-state mapping
- `outputs` for rendering behavior
- `logging` for local event recording

This keeps hardware adapters swappable later without turning the repo into generic IoT glue code.

## Standard library only for the first commit

The first commit uses no external dependencies. The goal is a clean, inspectable base that runs anywhere Python 3 runs.

## Main file stays thin

`main.py` only wires together config, signal generation, processing, state mapping, and output.

## Current creature states are product states

`SLEEPY`, `CALM`, `ACTIVE`, `ALERT`, and `STRESSED` are intentionally expressive system states. They are not presented as scientific plant truth.
