# Sources

This repo is currently built from first-principles product and architecture decisions rather than external code imports.

## Current source of truth

- project brief and handoff prompt for Plant Creature Alpha
- local Raspberry Pi 5 runtime goals
- Python 3 standard library only for the initial scaffold
- Raspberry Pi deployment target at `pi@192.168.137.142:/home/pi/plant`

## External references planned for later phases

- Raspberry Pi documentation for GPIO and hardware integration
- ADS1115 documentation for the first ADC path
- SSD1306 documentation for the first local display path
- WS2812 reference material for the first expressive light output path
- sensor wiring notes once the plant signal hardware is confirmed

## Notes

- No third-party code has been copied into this scaffold.
- The current simulation behavior is intentionally expressive, not scientific.
- Deployment scripts rely on standard `ssh`, `scp`, `tar`, `git`, and Python tools already present on Windows or Raspberry Pi OS.
