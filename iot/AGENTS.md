# AGENTS.md — IoT (`iot/`)

Course-specific guidelines for **Internet das Coisas (IoT)** slide decks. Follows root `../AGENTS.md`, `create-slides`, `slide-design`, `visual-assets`, and `validate-slides`.

## Directory Layout

- Standalone decks: `aula-rtc-deep-sleep.html`, `bots-telegram-discord-iot.html`.
- `13-sensores-atuadores-{MODEL}[-noplan].html`: Benchmark comparison family of 17 model-generated variants of Aula 13 (leave historical variants untouched unless explicitly asked).

## Course-Specific Patterns

- **Code blocks (C++ / Arduino)**: Use `<code-block lang="cpp" data-trim>` with `<textarea>` ONLY when C++ angle brackets appear (such as `#include <Arduino.h>`). **Never** use `<script type="text/plain">` inside `<code-block>` (causes Vue template warnings and fails static validation).
- **Hardware & circuit visuals**: Prefer real, well-lit hardware photos, clear pinout diagrams, and breadboard schematics sourced via `visual-assets` (e.g., `randomnerdtutorials.com`, `learn.adafruit.com`, `docs.espressif.com`, `makerhero.com`, `arduinoecia.com.br`) with concise pt-BR `alt` text and `<p class="source">` attribution.
- **Library versions**: For ESP8266/ESP32 Telegram bots, use `cotestatnt/AsyncTelegram2 @ ^2.3.4` with `bblanchon/ArduinoJson @ ^6.21.5` (v6, not v7); see `.agents/skills/create-slides/references/gotchas.md` for API details.
- **Optional plugins CSS/JS**: Use `../plugin/poll/style.css` (not `plugin.css`), `../plugin/customcontrols/style.css`, and local `../plugin/chalkboard/plugin.js`.

## Verification

```bash
python3 .agents/skills/validate-slides/scripts/validate_slide_deck.py iot/<deck>.html
```
