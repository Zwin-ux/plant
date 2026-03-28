# ChatGPT Advisor Handoff

Use this as the current truth snapshot for Plant Creature Alpha.

## Project role split

- Codex is the implementation and deployment agent.
- ChatGPT is the advisor/helper for product logic, creature behavior, hardware strategy, calibration thinking, and critique.
- The repo and the Raspberry Pi state below are the ground truth. Advice should stay aligned with them.

## What this project is

Plant Creature Alpha is a Raspberry Pi-based living-system prototype: a digital creature that starts in simulation mode and later grows into a plant-linked biofeedback organism.

This is not a generic IoT dashboard.
This is not a throwaway sensor demo.
It should feel like the beginning of a real product system.

## Live system status

Verified over SSH on March 27, 2026 at 10:37 PM Pacific from `pi@192.168.137.142`.

For a fresh live snapshot before making decisions, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\pi_status.ps1
```

- Hostname: `plantpi`
- User: `pi`
- IP: `192.168.137.142`
- Kernel: `Linux 6.12.75+rpt-rpi-2712 aarch64 GNU/Linux`
- Python: `3.13.5`
- Uptime at check: `26 minutes`
- Load at check: `0.00, 0.02, 0.00`
- Memory at check: `485Mi / 4.0Gi used`
- Disk at check: `7.0G / 29G used (26%)`
- Repo path on Pi: `/home/pi/plant`
- Virtualenv: present
- Pi repo HEAD matched the local repo HEAD at the time of the check

### Device nodes seen at check

- I2C nodes: `/dev/i2c-13`, `/dev/i2c-14`
- SPI node: `/dev/spidev10.0`
- GPIO chips: `/dev/gpiochip0`, `/dev/gpiochip10`, `/dev/gpiochip11`, `/dev/gpiochip12`, `/dev/gpiochip13`, `/dev/gpiochip4`

This does not mean the project hardware is connected yet. It only means the Pi exposes those device nodes right now.

## Current software status

The current repo already supports:

- simulation-first runtime
- living-feeling fake signal generation
- signal smoothing and normalization
- creature states: `SLEEPY`, `CALM`, `ACTIVE`, `ALERT`, `STRESSED`
- one-line console rendering per tick
- opt-in JSONL logging
- Git-first Pi deployment workflow
- Windows helper scripts for sync, smoke, and status

Main entrypoint:

- `python main.py --ticks 10`
- `python main.py --ticks 10 --log-file logs/dev.jsonl`

Pi helper scripts:

- `scripts/bootstrap_pi.sh`
- `scripts/run_pi_smoke.ps1`
- `scripts/sync_to_pi.ps1`
- `scripts/pi_status.ps1`

## Hardware arriving tomorrow

Confirmed incoming parts:

- ADS1115 ADC modules
- SSD1306 0.96" I2C OLED modules
- WS2812 / SK6812 16-pixel LED ring
- capacitive soil moisture sensors
- breadboards
- jumper wires

Current reality:

- only the Raspberry Pi 5 is available today
- no plant-signal or ADC integration should be assumed yet
- software must remain runnable without hardware attached

## What ChatGPT should help with next

Best advisory areas:

- creature behavior design
- state semantics and emotional logic
- how to map noisy real inputs into creature-readable states
- calibration strategy for ADS1115 + sensors
- OLED and LED expression vocabulary
- data logging schema and replay ideas
- ordering the first hardware-integration milestones

## Guardrails

Please keep advice aligned with these constraints:

- simulation-first
- modular architecture
- `main.py` stays orchestration-only
- no giant framework
- no dashboard unless explicitly requested
- no database unless clearly justified
- no fake scientific claims
- no pretending hardware is already wired or verified

## Good next implementation direction

The most useful next build step after hardware arrives is probably:

1. add a real ADS1115-backed signal provider behind the existing signal contract
2. keep the simulator available side-by-side
3. add a minimal output hook for the OLED and LED ring
4. start logging both simulated and real runs in the same schema
5. calibrate signal ranges before making strong creature-behavior claims

## Prompt to give ChatGPT

```text
You are advising on Plant Creature Alpha, a Raspberry Pi 5 plant-creature system.

Current reality:
- canonical repo: https://github.com/Zwin-ux/plant.git
- the software already runs in simulation mode
- Raspberry Pi hostname: plantpi
- Pi IP: 192.168.137.142
- Pi repo path: /home/pi/plant
- Python 3.13.5 is working
- the Pi checkout has already been deployed and smoke-tested successfully
- hardware is not fully connected yet
- incoming hardware tomorrow: ADS1115, SSD1306 OLED, WS2812 ring, capacitive moisture sensors, breadboards, jumper wires

The implementation agent is handling code, deployment, and hardware connection work.
Your job is to advise on:
- creature behavior design
- calibration and signal interpretation strategy
- OLED/LED expression ideas
- state transition logic
- product direction and sequencing

Important constraints:
- stay simulation-first until the hardware is actually wired
- do not assume ADC or sensor integration already exists
- do not suggest a generic IoT dashboard
- do not suggest giant frameworks
- avoid fake scientific claims
- preserve the existing modular architecture

Base your advice on the real machine state and the repo reality above, not on imagined infrastructure.
```
