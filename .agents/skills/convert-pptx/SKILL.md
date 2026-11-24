---
name: convert-pptx
description: >-
  Convert PowerPoint (.pptx) or Google Slides presentations into Reveal.js HTML
  decks while preserving Prof. Caio's illustrated pedagogical style, paper cards,
  and progressive visual annotations. Use when asked to convert a PPTX or Google
  Slides deck into ia/aulaNN-<slug>.html or another course deck.
---

# Convert PPTX / Google Slides → Reveal.js

Convert `.pptx` decks (local in `ia/` or exported from Google Slides) into Reveal.js decks that **preserve and elevate Prof. Caio's Illustrated Pedagogical Style** instead of flattening visual slides into bullet lists.

## Required Companion Skills

Always read and apply:
- `create-slides` (HTML boilerplate, super sections, Vue components, QA)
- `slide-design` + `slide-design/references/illustrated-style-guide.md` (illustrated style, paper cards, progressive overlays, sparse text)
- `ia/AGENTS.md` (when target is `ia/`)
- `create-slides/references/google-slides-export.md` (when source is a Google Slides URL)

## Step 1 — Inspect Visually AND Extract Structure

Never convert from raw XML text alone — progressive highlights, arrows, paper headers, and visual pacing are invisible in text-only dumps!

1. If source is a Google Slides URL, export **both** `.pdf` (for exact slide visuals via `pdftoppm`) and `.pptx` (for clean text, links, and embedded images).
2. Run the bundled extractor:
   ```bash
   python3 .agents/skills/convert-pptx/scripts/extract_pptx.py \
     "ia/ARQUIVO.pptx" \
     --media-dir ia/images/aulaNN \
     --contact-sheet /tmp/aulaNN_contact.png
   ```
   This prints every slide's text, hyperlinks (arXiv, Colab, YouTube), speaker notes, and used image filenames, extracts only used media, and builds a labeled contact sheet.
3. **Visually read** `/tmp/aulaNN_contact.png` (and PDF slide contact sheets if available) to identify:
   - Section divider slides → convert to `<section-banner>`
   - Paper headers & highlighted abstracts → convert to `<paper-card>` + `<mark class="paper-mark fragment">` (or cropped high-res paper image inside `.figure-card`)
   - Multi-slide progressive visual builds (e.g., Slides 20→21→22→23 boxing parts of one figure, or Slides 14→15→16 highlighting equation terms) → reconstruct as clean progressive Reveal.js steps using `.figure-stage` + `.annotate-box` + `.annotate-svg` / `<leader-line>`, `.formula-stage`, or `data-auto-animate`!
   - Full-slide custom infographics (e.g., VAE architecture diagram) → keep large inside `.figure-card`, never shrink into a tiny column next to invented bullets!
   - Colab / notebook links → render as `.colab-pill` directly under the corresponding slide.

## Step 2 — Clean, Rename & Optimize Extracted Images

1. Rename kept images to descriptive pt-BR kebab-case (e.g., `arquitetura-ldm.png`, `vae-espaco-latente.png`).
2. Compress heavy raster files (>500 KB): resize to max width 1200 px (JPEG q85 if opaque, optimized PNG if transparent/diagram). Always load images inside `with Image.open(p) as im:` before renaming/removing.
3. Discard unused/broken/decorative background-master artifacts (`fundo.png`, duplicate IFSP logos, near-black crops). Delete temporary contact sheets before finishing.
4. Light-background figures, screenshots, and paper diagrams MUST sit inside `.figure-card` (white rounded frame with subtle shadow) for crisp readability on Dracula. Photos use `border-radius: 8px`.

## Step 3 — Author the Deck Faithfully

- Output path: `ia/aulaNN-<slug>.html`, images in `ia/images/aulaNN/`.
- Cover: `<header1 aula="NN" curso="Inteligência Artificial" title-size="26" title="...">` with recognizable visual(s) from slide 1.
- Group major chapters into super sections (`<!-- Etapa N: ... -->` ... `<!-- fim Etapa N -->`) opened by `<section-banner>`.
- Preserve Prof. Caio's sparse prose (do NOT pad sparse visual slides with invented textbook bullets!).
- Decode any XML entities (`&gt;` → `>`, `&amp;` → `&`), format code in `<code-block lang="python">`, and convert equations to KaTeX (with `.formula-stage` when broken down term-by-term).
- Close with concise `Resumo da aula` and clickable `Referências` (all arXiv/DOI/Colab/web links from the source deck).

## Step 4 — Mandatory QA (`validate-slides`)

1. Run static validation (including orphan-asset check):
   ```bash
   python3 .agents/skills/validate-slides/scripts/validate_slide_deck.py ia/aulaNN-<slug>.html --check-orphans
   ```
   Must pass with **0 errors / 0 warnings**.
2. Verify external links return HTTP 200 (`curl -s -o /dev/null -w "%{http_code}" -L -A "Mozilla/5.0" URL`).
3. Serve locally (`python3 -m http.server 8123` or `.claude/launch.json`) and run `.agents/skills/validate-slides/scripts/check_overflow.js` on the 960×700 canvas. Confirm `over: []`, zero broken images, and clean console.
