---
name: search-images
description: Search for images to use in slides, documentation, or educational materials. Uses dedicated image APIs first, then falls back to web search + extraction.
license: MIT
compatibility: opencode
metadata:
  audience: instructors
  domain: education
---

## What I do

- Search for licensed images across multiple sources (Wikimedia Commons, Openverse, Unsplash, Pexels, Pixabay)
- Fall back to site-specific searches on educational/technical sites (Random Nerd Tutorials, Adafruit, SparkFun, etc.)
- Extract image URLs from web pages when needed
- Provide attribution information for every image found

## When to use me

Use this skill when the user asks to find images, search for pictures, get photos, or needs visual assets for slides, documentation, or educational materials.

## How I work

### Phase 1: Dedicated Image APIs (Preferred)

Call multiple tools in parallel with the same query:

| Tool | Best For | License Info |
|------|----------|--------------|
| `wikimedia_search_commons` | Technical diagrams, hardware, scientific images | CC licenses, public domain |
| `openverse_search_images` | Creative Commons images from Flickr, Wikimedia, etc. | CC licenses |
| `unsplash_search_photos` | High-quality photos (nature, tech, people) | Unsplash License |
| `pexels_photos_search` | General stock photos | Pexels License |
| `pixabay_search_pixabay_images` | Illustrations, vectors, general images | Pixabay License |

Select the best image based on relevance, visual clarity, license appropriateness, and attribution requirements.

### Phase 2: Specific Site Search (Fallback)

If dedicated APIs don't return suitable results, search these educational/technical sites:

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
