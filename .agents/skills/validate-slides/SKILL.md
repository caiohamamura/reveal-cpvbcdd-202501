---
name: validate-slides
description: >-
  Run deterministic static and browser-level validation on Reveal.js slide decks
  (HTML parse, CJK check, code-block script check, Etapa phase markers, leader-line
  closing tags, image alt/binary/orphan checks, and 960x700 overflow verification).
  Use after creating or modifying any HTML slide deck.
---

# Validate Slides

Run deterministic validation after every deck creation or edit.

## Step 1 — Static Validation

Run the bundled validator on modified deck(s):

```bash
python3 .agents/skills/validate-slides/scripts/validate_slide_deck.py ia/aula06-deteccao-objetos-segmentacao.html
```

Include `--check-orphans` to also detect unused image files inside a lesson's image directory:

```bash
python3 .agents/skills/validate-slides/scripts/validate_slide_deck.py ia/aulaNN-slug.html --check-orphans
```

### Static Checks Performed

- Valid HTML parse (`HTMLParser`)
- Zero Chinese / CJK characters
- Zero `<script>` tags inside `<code-block>`
- Zero self-closing `<leader-line ... />` tags (must use `</leader-line>`)
- Balanced `Etapa N:` / `fim Etapa N` super-section comment markers
- Every local `href`, `src`, and `data-background-image` exists on disk
- Every `<img>` has non-empty `alt`
- Local images are valid binaries >1 KB (verified with Pillow when available)
- Optional (`--check-orphans`): warns on unused image files inside referenced lesson asset folders

Fix every `ERROR` and review every `WARN`.

## Step 2 — Browser Overflow & Broken-Image QA (960×700 Canvas)

1. Serve the repository locally:
   ```bash
   python3 -m http.server 8123
   ```
   (or use the preview config in `.claude/launch.json`).
2. Open `http://localhost:8123/<course>/<deck>.html` in a browser (e.g., Chrome DevTools MCP) and evaluate [scripts/check_overflow.js](./scripts/check_overflow.js).
3. Confirm:
   - `over` is empty (`[]`) — if any slide overflows `960×700`, reduce image height/width, spacing, or font sizes and re-check
   - `brokenImages` is empty (`[]`)
   - Zero runtime errors or Vue warnings in the browser console
4. Verify external URLs return HTTP 200 when links were added or modified.
