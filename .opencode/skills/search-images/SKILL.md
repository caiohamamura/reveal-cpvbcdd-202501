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

- Never flood any API/server, always sleep randomly from 1 to 4 seconds between requests
- NEVER search in parallel


## What I do

- Use site-specific searches on educational/technical sites (Random Nerd Tutorials, Adafruit, SparkFun, etc.) and fallback to general sites
- Extract image URLs from web pages when needed
- Provide attribution information for every image found

## When to use me

Use this skill when the user asks to find images, search for pictures, get photos, or needs visual assets for slides, documentation, or educational materials.

## How I work

### Phase 1: Specific Site Search (Fallback)

Search these educational/technical and other education/technical sites:

1. `randomnerdtutorials.com` — ESP32/Arduino tutorials with hardware photos
2. `learn.adafruit.com` — Adafruit product images
3. `sparkfun.com` — SparkFun product images
4. `docs.espressif.com` — Espressif official docs
5. `circuits-diy.com` — Circuit diagrams and project images
6. `makerhero.com` — Brazilian maker community images
7. `usinainfo.com.br` — Brazilian electronics store images
8. `instructables.com` — DIY project photos
9. `guiarobotica.com` — Robotics guides
10. `create.arduino.cc` — Arduino project hub
11. `circuitsbasics.com` — Basic circuit images
12. `arduinogetstarted.com` — Arduino tutorials
13. `arduinoecia.com.br` — Brazilian Arduino community
14. `hackster.io` — Hardware projects
15. `how2electronics.com` — Electronics tutorials
16. `portal.vidadesilicio.com.br` — Brazilian maker content

Usage pattern: search with `site:randomnerdtutorials.com OR site:learn.adafruit.com`, then `webfetch` promising pages and extract direct image URLs from the HTML.

### Phase 3: General Web Search (Last Resort)

Use `websearch` with a descriptive query plus `"image"`, then `webfetch` promising pages. Extract image URLs from `<meta property="og:image">`, `<link rel="preload">`, or `<img>` tags.

### Attribution Rules

Always include image attribution in slides:

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
- **Are properly licensed** — CC licenses, public domain, or permissive licenses
- **Have reasonable file size** — avoid 4K+ images that slow slide loading

