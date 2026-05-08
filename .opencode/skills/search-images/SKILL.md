---
name: search-images
description: Search for images to use in slides, documentation, or educational materials. web search + extraction.
license: MIT
compatibility: opencode
metadata:
  audience: instructors
  domain: education
---

### VERY IMPORTANT

- NEVER do `ollama_web_web_search` calls in parallel because the tool will return too many requests
- NEVER add words like "image", "diagram", "photo", "picture", or "foto" to the `query`. Search for the topic directly (e.g. `hall sensor`, `ESP32 WiFi`, `LED PWM`). Tutorial pages already contain images; adding English keywords hurts results on Brazilian/Portuguese domains.

## What I do

- Use Ollama's web search API with site-specific queries on educational/technical sites (Random Nerd Tutorials, Adafruit, SparkFun, etc.) and fallback to general sites
- Extract image URLs from web pages deterministically
- Provide attribution information for every image found

## When to use me

Use this skill when the user asks to find images, search for pictures, get photos, or needs visual assets for slides, documentation, or educational materials.

## How I work

### Phase 1: Specific Site Search (Preferred)

Call `ollama_web_web_search` with site-specific queries using `site:` operator to target educational/technical sites. Then run the `extract_images.py` script on promising result URLs to fetch pages and extract images.

Target sites (searched via `site:` prefix in query):
- `randomnerdtutorials.com` — ESP32/Arduino tutorials with hardware photos
- `learn.adafruit.com` — Only adafruit tutorials, not boring product spec photos
- `sparkfun.com` — SparkFun product images
- `docs.espressif.com` — Espressif official docs
- `circuits-diy.com` — Circuit diagrams and project images
- `makerhero.com` — Brazilian maker community images
- `usinainfo.com.br` — Brazilian electronics store images
- `instructables.com` — DIY project photos
- `guiarobotica.com` — Robotics guides
- `create.arduino.cc` — Arduino project hub
- `circuitsbasics.com` — Basic circuit images
- `arduinogetstarted.com` — Arduino tutorials
- `arduinoecia.com.br` — Brazilian Arduino community
- `hackster.io` — Hardware projects
- `how2electronics.com` — Electronics tutorials
- `portal.vidadesilicio.com.br` — Brazilian maker content

Usage pattern:
1. Call `ollama_web_web_search` with the topic and `site:` prefix in the query (see example below). Search **one site at a time** to get focused results; start with the most relevant 2-3 sites.
2. From the search result URLs, pick the most promising tutorial pages.
3. Run `python3 .opencode/skills/search-images/extract_images.py` on the selected URLs. The script fetches each page, extracts and validates images, and returns ranked JSON.
4. Return the best images with attribution.

### Phase 2: General Web Search (Fallback)

Only if Phase 1 yields no usable images, call `ollama_web_web_search` again **without** `site:` prefix, using the topic-only query with `max_results: 5`. Then apply the same deterministic extraction.

### Deterministic Image Extraction

**Use the `extract_images.py` script** for deterministic extraction. It does the full pipeline and returns validated JSON.

```bash
python3 .opencode/skills/search-images/extract_images.py URL1 URL2 URL3...
```

**What the script does (for each page URL):**

1. **Fetch the page HTML** via `requests` (with real browser User-Agent).
2. **Collect candidate image URLs** from `<meta og:image>`, `<meta twitter:image>`, `<link rel=preload as=image>`, and `<img src>` tags inside `<article>/<main>` and content divs.
3. **Filter out non-content images** by URL pattern (logo, icon, avatar, social, share, button, banner, ad, tracking, pixel, spacer, loading, placeholder, emoji, gravatar, etc.) and by `width`/`height` attributes <= 80px.
4. **Deduplicate** by exact URL (case-insensitive).
5. **Validate each candidate** via HTTP HEAD request:
   - Status must be 200
   - Content-Type must start with `image/`
   - Content-Length must be >= 1024 bytes (uses GET+stream peek if no Content-Length header)
6. **Score and rank** remaining candidates:
   - `og:image` or `twitter:image` → +100
   - `<img>` inside `<article>`/`<main>`/content div → +50
   - URL contains circuit/diagram/wiring/schematic/breadboard/project/pinout → +30
   - URL ends in `.png` → +5
7. **Return top 5** per page as JSON with `url`, `alt`, `content_type`, `size_bytes`, `score`, `source_page`, `source_domain`.

### Example `ollama_web_web_search` calls with site-specific queries

Search one site at a time for best results. Use `site:` prefix in the query string:

```json
{
  "query": "hall sensor site:randomnerdtutorials.com",
  "max_results": 5
}
```

```json
{
  "query": "ESP32 PWM site:learn.adafruit.com",
  "max_results": 5
}
```

For general fallback search (Phase 2):

```json
{
  "query": "hall sensor ESP32 tutorial",
  "max_results": 5
}
```

### Example extract_images.py usage

```bash
python3 .opencode/skills/search-images/extract_images.py \
  https://randomnerdtutorials.com/esp32-hall-effect-sensor/ \
  https://learn.adafruit.com/esp32-pwm
```

### Alt labelling and attribution Rules

- Create a short and objective description of the image and put is as `alt` attribute.
- Always include image attribution in slides:

```html
<p style="font-size: 12pt; color: #6272a4;">Fonte: [Site] ([License])</p>
```

- **Wikimedia Commons**: Include photographer name + CC license
- **Random Nerd Tutorials**: Include "Fonte: Random Nerd Tutorials"
- **Unsplash/Pexels/Pixabay**: Include photographer name + site name
- **Adafruit/SparkFun**: Check their specific attribution requirements

### Image Selection Criteria

For educational slides, prefer images that are:
- **Clear and well-lit** — students need to see component details
- **Show components in context** — connected to breadboard/ESP32 when possible
- **Have neutral backgrounds** — white or simple backgrounds work best on slides
- **Have reasonable file size** — avoid 4K+ images that slow slide loading
