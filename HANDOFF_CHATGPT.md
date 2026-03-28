# ChatGPT Advisor Handoff

Use this as the current truth snapshot for Plant Creature Alpha.

## Project role split

- Codex is the implementation and deployment agent.
- ChatGPT is the advisor/helper for product logic, creature behavior, calibration thinking, hardware strategy, and critique.
- The repo and the Raspberry Pi state below are the ground truth. Advice should stay aligned with them.

## What this project is

Plant Creature Alpha is a Raspberry Pi-based living-system prototype: a small digital organism that starts in simulation mode and later grows into a plant-linked biofeedback companion.

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

## Current software status

The current repo now supports:

- simulation-first runtime
- living-feeling fake signal generation
- generic ADS1115 provider boundary for future analog input
- signal smoothing and normalization
- a lightweight TRIBE-inspired fusion layer with hidden drives:
  - hydration
  - stability
  - energy
  - bond
  - stress_load
- creature states:
  - `SLEEPY`
  - `CALM`
  - `ACTIVE`
  - `ALERT`
  - `STRESSED`
  - `RECOVERING`
- deterministic creature micro-language
- presentation-first console rendering
- opt-in JSONL logging
- Git-first Pi deployment workflow
- Windows helper scripts for sync, smoke, and live Pi status
- OLED and LED ring scaffolds that consume the same presentation model as the console path

Main entrypoint:

- `python main.py --ticks 10`
- `python main.py --ticks 10 --log-file logs/dev.jsonl`
- `python main.py --ticks 1 --signal-source ads1115`

## Very important scope note

Actual [TRIBE v2](https://github.com/facebookresearch/tribev2) code is **not** integrated into this repo.

The project only borrows the idea of hidden multimodal fusion and translates it into a Pi-sized creature model. That keeps the runtime small, maintainable, and realistic for the Raspberry Pi 5.

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
- no live ADC or sensor integration should be assumed yet
- software must remain runnable without hardware attached
- the repo contains ADS1115, OLED, and LED boundaries, but the real device behavior is still intentionally unwired

## What ChatGPT should help with next

Best advisory areas:

- hidden-drive tuning
- creature mood semantics
- calibration strategy for ADS1115 + moisture sensing
- OLED face language and screen composition
- LED aura vocabulary
- how to stage care loops and progression without exposing raw sensor jargon
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
- no surprise heavyweight model stack on the Pi

## Good next implementation direction

The most useful next build step after hardware arrives is:

1. enable Pi I2C and verify device addresses
2. wire the ADS1115 through the existing signal contract
3. bring up one real OLED proof screen using the shared presentation model
4. validate one LED aura behavior from the same presentation object
5. calibrate moisture-derived hydration before making stronger creature claims

## Prompt to give ChatGPT

```text
You are advising on Plant Creature Alpha, a Raspberry Pi 5 plant-creature system.

Current reality:
- canonical repo: https://github.com/Zwin-ux/plant.git
- the software already runs in simulation mode
- the runtime uses a lightweight TRIBE-inspired hidden-drive layer, not the real TRIBE v2 model
- Raspberry Pi hostname: plantpi
- Pi IP: 192.168.137.142
- Pi repo path: /home/pi/plant
- Python 3.13.5 is working
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
- do not propose importing actual TRIBE v2 into the Pi runtime

Base your advice on the repo reality above, not on imagined infrastructure.
```
