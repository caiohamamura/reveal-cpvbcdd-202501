# AGENTS.md — Reveal.js Slide Framework (IFSP Campus Capivari)

Static educational presentation repository built on **Reveal.js 5.2.1** + **Vue 3 ESM** (no bundler, deployed via GitHub Pages in `.github/workflows/static.yml`).

## Repository Map

```text
reveal-cpvbcdd-202501/
├── AGENTS.md                  # Repo-wide rules (this file)
├── .agents/skills/            # Canonical modular skills (symlinked from .claude/skills & .opencode/skills)
├── ia/                        # Inteligência Artificial — decks, images/, cadernos/, source .pptx + ia/AGENTS.md
├── bdd1/                      # Banco de Dados I — decks
├── bdd2/                      # Banco de Dados II — decks, planos/, generate_exams.py + bdd2/AGENTS.md
├── ciencia-dados/             # Ciência de Dados — decks, images/, notebooks/, aulas/ + ciencia-dados/AGENTS.md
├── iot/                       # IoT — decks + iot/AGENTS.md
├── components/                # Shared Vue components (components.js, test-components.html)
├── slides_template/           # Shared cover (<header1>) and Reveal+Vue initializer (init.js)
├── dist/                      # Reveal.js core, Dracula theme, custom.css, Vue 3
├── plugin/                    # Local Reveal plugins (highlight, math, markdown, notes, poll, seminar, chalkboard, customcontrols, zoom, chart, reveald3, leader-line)
├── img/                       # Shared assets (fundo.png IFSP green banner, IFSP logo)
└── docs/ECOSSISTEMA.md        # Complete component, CSS, and plugin reference
```

## Skills Catalog (`.agents/skills/`)

Load skills on demand rather than guessing conventions:

| Skill | Use When |
|-------|----------|
| `slide-design` | Designing or refining slide aesthetics; defines Prof. Caio's **Illustrated Pedagogical Style** (`references/illustrated-style-guide.md`) |
| `create-slides` | Creating or editing Reveal.js `.html` decks (boilerplate, components, `references/gotchas.md`, `references/google-slides-export.md`) |
| `visual-assets` | Sourcing seminal paper figures, generating custom illustrations/infographics, or extracting validated web images (`scripts/extract_images.py`) |
| `convert-pptx` | Converting `.pptx` or Google Slides decks into illustrated Reveal.js decks (`scripts/extract_pptx.py`) |
| `validate-slides` | Running static validation (`scripts/validate_slide_deck.py`) and 960×700 overflow QA (`scripts/check_overflow.js`) |
| `export-plots` | Exporting Plotly figures into standalone RevealD3 iframe HTML (`scripts/export_reveald3_plotly.py`) |
| `run-notebook` | Executing `.ipynb` notebooks and extracting PNG outputs (`scripts/run_notebook.py`) |
| `reflect-and-learn` | Capturing new gotchas, style corrections, or patterns into skills/rules after non-trivial tasks |

Always read the target course's `AGENTS.md` (`ia/`, `bdd2/`, `ciencia-dados/`, `iot/`) before creating or editing slides in that course.

## Visual & Pedagogical Philosophy

- **Visual-first, sparse text**: Slides support a live spoken lecture. Lead with one strong visual artifact (seminal paper figure, custom illustrated diagram/infographic, real executed output, notebook plot, or progressive equation breakdown) and concise pt-BR text — never continuous paragraphs or repetitive card walls.
- **No crude icon/CSS cartoons**: Never substitute FontAwesome icons (`fa-car-side`, `fa-plane`) + CSS boxes/blobs for real figures, photos, or custom technical illustrations.
- **Illustrated style for conceptual/IA lessons**: Anchor milestones in real papers (`<paper-card>`), open chapters with `<section-banner>` (`img/fundo.png`), unpack architectures/formulas progressively (`.figure-stage`, `.annotate-box`, `.formula-stage`), and attach `.colab-pill` links where concepts land.
- **Direct to students**: Write in Brazilian Portuguese (`pt-BR`) addressing students directly. Technical terms in English are fine. Never include Chinese/CJK characters, teacher meta-commentary, or internal setup/tool mentions (`micromamba`, `opencode`, etc.).

## Universal Technical Rules

- **Initialization**: Use `dist/theme/dracula.css` + `dist/custom.css` and `window.app = mountSlideApp();` via a regular `<script>` tag (never `type="module"`). Load local `../plugin/chalkboard/plugin.js` (never CDN).
- **Formatting**: Use **4-space indentation** inside `<div class="slides">`. Group major topics in parent `<section>` super-sections closed with `<!-- fim Etapa N -->`. Keep cover, standalone quiz, summary, and references at top level.
- **Vue DOM templates**: Always use **kebab-case** props (`title-size`, `start-socket`, `middle-label`, `answer-text`). Always close `<leader-line></leader-line>` explicitly.
- **Code blocks**: Place ordinary code as raw text inside `<code-block lang="...">`; wrap in `<textarea>` only if the code contains `<` or `>`. **Never** place `<script>` inside `<code-block>`.
- **Fragments**: Use sparingly (progressive figure/formula annotations, synced code highlighting, motivation, exercise steps, final recap). Use plain `<ul>` for definitions and reference lists. Never fragment section divider slides.
- **Images**: Every `<img>` requires concise pt-BR `alt` text, `width` **or** `height` (not both), valid local binary >1 KB (or HTTP 200), `.figure-card` framing for light-bg diagrams, and `<p class="source">` attribution.
- **Code comments**: Do not add unrequested comments in code files; preserve existing unrelated comments/docstrings.

## Development & QA Commands

```bash
# Serve decks locally
python3 -m http.server 8123

# Static validation (mandatory after every deck edit)
python3 .agents/skills/validate-slides/scripts/validate_slide_deck.py <deck.html> --check-orphans

# Python / Jupyter environment
micromamba run -n opencode python3 <script.py>
```

## Post-Task Reflection

After debugging non-obvious issues, learning new patterns, or receiving style/approach feedback from the user, run the `reflect-and-learn` skill protocol proactively and briefly inform the user what was recorded and where.
