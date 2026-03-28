# TODO

## Next up

- wire `plant_creature.logging.recorder` into the main loop
- track explicit state transitions instead of only current state
- move thresholds and timings toward richer config tuning
- add a hardware input contract for future ADC-backed signal readers

## Soon after

- persist signal and state events to JSONL or CSV
- add replay-friendly log structure
- design placeholder hooks for LEDs, displays, and sound
- add lightweight tests for the processor and state engine

## Later

- integrate a real ADC input path once hardware is confirmed
- compare simulated and real signal streams with the same pipeline
- tune creature behavior so it feels emotionally coherent over longer sessions
