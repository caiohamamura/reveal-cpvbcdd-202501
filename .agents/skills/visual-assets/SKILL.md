---
name: visual-assets
description: >-
  Source, generate, crop, validate, and attribute authentic visual assets for
  Reveal.js slides — seminal paper figures, custom technical illustrations and
  infographics, Python/Matplotlib plots, and validated educational web images.
  Use whenever a deck needs diagrams, paper figures, illustrations, or photos.
---

# Visual Assets for Slides

Source high-signal visual assets that match Prof. Caio's Illustrated Pedagogical Style. **Never substitute crude FontAwesome icons or CSS shape cartoons for real figures, photos, or custom illustrations.**

## Asset Hierarchy (Pick the Best Fit First)

1. **Seminal Paper Figures & Headers (Top Priority for IA / ML)**
   - Fetch the paper's PDF or HTML version from `arXiv` (`https://arxiv.org/pdf/<id>` or `https://arxiv.org/html/<id>`).
   - Render pages cleanly with `pdftoppm -png -r 180 paper.pdf /tmp/paper_page` and crop the exact figure or header with Pillow (`Image.crop()`), saving to `<course>/images/aulaNN/<descriptive-name>.png`.
   - Always frame white-background paper crops in `.figure-card` and add a clickable `<p class="source">` citing authors, year, paper title, and figure number.
   - Alternatively, use `<paper-card>` for crisp native typography + progressive yellow abstract highlights (`<mark class="paper-mark fragment">`).

2. **Custom Illustrated Diagrams & Infographics**
   - When explaining an architecture, multi-step visual process, or intuitive metaphor in pt-BR (e.g., *Arquitetura VAE com EBlock/DBlock*, *evolução de ruído t=500 → t=0*, *cena realista de objetos para detecção*):
     - Use available image-generation tooling (e.g., `image-generator` subagent) with clear art direction: clean pedagogical infographic or realistic editorial scene, readable labels (or clean unlabeled visual annotated via `.figure-stage` + `.annotate-box`), dark-slide friendly or clean white diagram framed in `.figure-card`.
     - Or author a crisp **bespoke SVG** or **Python Matplotlib/Seaborn figure** for exact mathematical visuals (vector fields / density gradients "bússola", 2D latent manifolds, loss landscapes, activation curves, Gaussian noise schedules).
   - Always visually inspect generated/rendered images with `read_file` to verify zero garbled text, clean layout, and high contrast.

3. **Notebook Plots & Executed Outputs**
   - For data-driven charts and interactive step-by-step plots, use `run-notebook` or `export-plots` (RevealD3 + Plotly).

4. **Deterministic Web Image Extraction (Tutorials, Hardware, Official Docs)**
   - Search with your web search tool using **topic-only queries** (never add `"image"`, `"diagram"`, `"photo"`, or `"foto"` — it degrades results on pt-BR technical sites).
   - Target authoritative sources:
     - **IA / Ciência de Dados / Software**: `arxiv.org`, `pytorch.org`, `ultralytics.com`, `scikit-learn.org`, `distill.pub`, `jalammar.github.io`, `lilianweng.github.io`, `commons.wikimedia.org`
     - **IoT / Hardware**: `randomnerdtutorials.com`, `learn.adafruit.com`, `sparkfun.com`, `docs.espressif.com`, `makerhero.com`, `arduinoecia.com.br`, `usinainfo.com.br`, `how2electronics.com`
   - Extract and validate candidates deterministically:
     ```bash
     python3 .agents/skills/visual-assets/scripts/extract_images.py URL1 URL2
     ```
     The script filters UI chrome/icons, checks HTTP 200, `image/*` MIME type, and size >= 1 KB, and returns ranked JSON with `url`, `alt`, `content_type`, `size_bytes`, and `source_domain`.
   - Prefer downloading selected assets locally into `<course>/images/aulaNN/` so lessons work reliably offline in labs.

## Hygiene & Attribution Rules

- **Storage & naming**: `<course>/images/aulaNN/<kebab-case-pt-br>.{png,jpg,svg}` (no orphan files left unused).
- **File size**: Resize raster assets >500 KB to max width 1200 px (JPEG q85 for photos; optimized PNG for diagrams/screenshots).
- **Dark-theme legibility**: Wrap light-background figures/diagrams in `<div class="figure-card">...</div>`. Give photos `style="border-radius: 8px;"`.
- **Dimensions**: Constrain `width` **or** `height` — never both.
- **Accessibility**: Every `<img>` MUST have a concise, objective pt-BR `alt` description.
- **Attribution**: Include `<p class="source">Fonte: [Autor/Site] ([Ano/Licença])</p>` (clickable link to paper/source whenever available). For Wikimedia SVGs, link directly to `upload.wikimedia.org/wikipedia/commons/.../File.svg` (never `/thumb/...svg.png`).
