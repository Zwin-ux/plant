# TODO

## Next up

- enable Pi I2C and verify the OLED plus ADS1115 addresses on the live bus
- wire the first real ADS1115 channel into the existing signal pipeline
- decide how the capacitive moisture sensor should map into hydration after calibration data exists
- replace the OLED placeholder with one proof screen built from the shared presentation model
- replace the LED placeholder with one real aura pattern driven by the shared presentation model

## Soon after

- add real care/check-in inputs before unlocking states like `PLEASED` or `LONELY`
- persist longer-lived memory once care events and progression are real
- add replay-friendly creature logs for comparing simulated and real runs
- tune the hidden-drive formulas using real sensor behavior instead of only simulated input
- add lightweight tests for fusion, session memory, and state dwell behavior

## Later

- add richer OLED face sets and stronger LED expression vocabulary
- add progression, forms, and unlockable phrase sets
- explore future plant-electrode input as a separate signal path from moisture sensing
- revisit a local voice or LLM flavor layer only after sensing and outputs feel solid
