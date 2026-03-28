# TODO

## Next up

- track explicit state transitions instead of only current state
- move thresholds and timings toward richer config tuning
- add a real ADC-backed provider that implements the same `SignalProvider` contract
- add the first OLED and LED output hooks once the SSD1306 and WS2812 ring arrive

## Soon after

- persist signal and state events to JSONL or CSV with replay-friendly structure
- compare simulated and real ADC streams through the same processing pipeline
- design placeholder hooks for LEDs, displays, and sound
- add lightweight tests for the processor and state engine
- add a lightweight status command for checking Pi environment health

## Later

- integrate the capacitive moisture sensor as a separate signal path from future biofeedback experiments
- tune creature behavior so it feels emotionally coherent over longer sessions
- layer in more expressive output behavior once physical signals feel trustworthy
