# TODO

## Tomorrow morning

- verify the ADS1115 arrives and inspect its pin labels before wiring
- enable or verify Pi I2C access
- install `adafruit-circuitpython-ads1x15` inside `~/plant/.venv` if needed
- confirm the ADS1115 appears on the bus with `i2cdetect -y 1`
- wire one soil moisture sensor to A0 only, not everything at once
- run `python main.py --signal-source ads1115 --ticks 10`
- capture the first JSONL log of real values

## After first real readings

- tune the thirst / calm / alert / overload thresholds against actual moisture behavior
- map the first LED ring color and pulse behaviors from `color_intent` and `animation_intent`
- keep OLED work minimal: one proof screen, not a dashboard
- compare simulated profiles against the real sensor range

## Later

- add persistence for longer-term creature memory
- expand beyond one signal source
- support module types beyond plants
- revisit voice / LLM flavor only after sensing is trustworthy
