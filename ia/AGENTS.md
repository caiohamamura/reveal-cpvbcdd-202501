# AGENTS.md — Inteligência Artificial (`ia/`)

Course-specific rules for **Inteligência Artificial** decks at IFSP Campus Capivari. Read together with root `../AGENTS.md`, `slide-design` (especially `references/illustrated-style-guide.md`), `visual-assets`, and `create-slides`.

## Directory Layout

- `aulaNN-<slug>.html` — Student-facing Reveal.js slide decks (`curso="Inteligência Artificial"`).
- `images/aulaNN/` — Local versioned images, cropped paper figures, and custom illustrated infographics per lesson (kebab-case pt-BR names; zero orphan files).
- `cadernos/` — Course Jupyter/Colab notebooks (`mnist_medio.ipynb`, `variational_autoencoder.ipynb`, `VAE - perceptual loss.ipynb`, `Usando StyleGAN.ipynb`, `YOLO11 Tutorial.ipynb`, `SingleHeadAttention.ipynb`, `multiHeadAttention.ipynb`, etc.).
- `2025*.pptx` — Historical PowerPoint sources used as reference or input for `convert-pptx`.

## Mandatory Illustrated Style Contract

All new or refactored IA decks **must** follow Prof. Caio's Illustrated Pedagogical Style (modeled on *2026IA - Aula 11 - Do VAE ao Stable Diffusion* and detailed in `.agents/skills/slide-design/references/illustrated-style-guide.md`):

1. **Visual Hero First, Sparse Text Always**
   - Every conceptual slide centers on **one high-signal visual** (real seminal paper figure, custom illustrated technical infographic, real generated sample grid, mathematical plot, or progressive formula breakdown).
   - Target **0–35 words** per visual slide (1–2 crisp pt-BR takeaways or 2–4 ultra-short bullets). Never write dense explanatory paragraphs or walls of 5–6 bullets.
2. **Chronological, Problem-Driven Paper Narrative**
   - Structure lessons around real research milestones: *Limitation of previous model → Core insight → Seminal paper (author, year, clickable arXiv/DOI link) → Visual proof*.
   - Anchor papers explicitly with `<paper-card>` (full card with progressive `<mark class="paper-mark fragment">` abstract highlights, or `<paper-card compact>` in `.title-with-paper` headers).
3. **Progressive Visual Deconstruction (Never Dump All at Once)**
   - **Architectures & pipelines**: Display the real architecture figure large inside `.figure-card` + `.figure-stage`, then illuminate one sub-block at a time using translucent `.annotate-box` overlays, SVG arrows / `<leader-line>`, and a 1-line plain-Portuguese `.slide-takeaway` (e.g., *"Isso é o VAE"*, *"O ruído atua no espaço latente"*).
   - **Equations**: Render in `.formula-stage`, frame each meaningful term in a distinct color (`.formula-term--yellow`, `.formula-term--pink`, etc.), and reveal the intuitive pt-BR meaning directly underneath (`.formula-caption`).
   - **Cross-slide visual continuity**: Reuse an earlier diagram alongside a new chart when connecting mechanisms (e.g., latent diffusion diagram next to VAE latent-space manifold).
4. **Authentic Visuals & Custom Illustrations ONLY**
   - **Use**: real cropped figures from original papers (arXiv PDF/HTML), real model outputs/grids, Python/Matplotlib scientific plots (gradient vector fields, distributions, manifolds), and custom illustrated infographics generated specifically for the lesson.
   - **STRICTLY FORBIDDEN**:
     - Crude FontAwesome icon scenes (`fa-car-side`, `fa-plane`) with CSS boxes or `clip-path` masks standing in for real images/illustrations.
     - Crude CSS circles/divs pretending to be clustering, vision, or neural visualizations.
     - Repetitive dark `pipeline-node` text-box chains or 3–4 column `artifact-card` walls substituting for an actual visual diagram.
5. **IFSP Green-Striped Section Dividers**
   - Open major chapters and transitions ("Na aula passada", "O histórico até...", "Adicionando e removendo ruído...") with `<section-banner>` (`../img/fundo.png`), optionally featuring an iconic diagram or `<paper-card compact>` in the banner slot.
6. **Contextual Notebooks & Practical Anchors**
   - When a notebook in `ia/cadernos/` or a Colab URL corresponds to a concept, place a `.colab-pill` link directly beneath the slide finishing that concept — do not bury all practical links only on the final slide.

## Expected Lesson Flow

1. **Capa** (`<header1 aula="NN" curso="Inteligência Artificial">`) with recognizable tool logos or iconic visual.
2. **Na aula passada** (`<section-banner>` + 1 visual anchor slide from the previous lesson, not a long bullet list).
3. **Intuição geral primeiro** — big-picture visual diagram + 2–3 short steps before diving into history or math.
4. **Etapas em super-sections** (`<!-- Etapa N: ... -->` ... `<!-- fim Etapa N -->`), each opened by `<section-banner>`, progressing through seminal papers, annotated architectures, visual intuition, and contextual notebooks.
5. **Resumo da aula** (concise `<ls-u>`) and **Referências** (clickable arXiv/DOI/Colab links).

## QA Gate for IA Decks

1. Static validation with orphan check:
   ```bash
   python3 .agents/skills/validate-slides/scripts/validate_slide_deck.py ia/aulaNN-<slug>.html --check-orphans
   ```
2. Browser check on `960×700` canvas via `.agents/skills/validate-slides/scripts/check_overflow.js` → `over: []`, `brokenImages: []`, zero console errors.
3. Visual style audit: confirm zero FontAwesome/CSS-shape cartoons, crisp `.figure-card` framing on light figures, sparse slide word counts, and valid external paper/Colab links.
