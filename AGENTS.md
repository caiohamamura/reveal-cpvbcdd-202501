# AGENTS.md — Reveal.js Slide Framework

This repository contains Reveal.js-based slide decks for IFSP Campus Capivari technical courses (IoT, BDD1, BDD2, Ciência de Dados).

## Cold Start (No Context)

1. Read `AGENTS.md` (this file)
2. Read `docs/ECOSSISTEMA.md` for full framework documentation
3. Read `.opencode/skills/create-slides/SKILL.md` for slide creation patterns

## Repository Layout

```
reveal-cpvbcdd-202501/
├── iot/                   # IoT course slides (.html)
├── bdd1/                  # Banco de Dados I slides (.html)
├── bdd2/                  # Banco de Dados II slides (.html)
├── ciencia-dados/         # Data Science slides (.html) + images/, notebooks/, aulas/
├── dist/                  # Reveal.js core, themes, Vue.js, custom.css (built assets)
├── plugin/                # Reveal.js plugins + leader-line.min.js (NOT via npm)
├── components/            # Vue.js custom components (components.js)
├── slides_template/       # Shared templates: header1.js, init.js
├── img/                   # Shared images (logo, background)
├── docs/                  # ECOSSISTEMA.md — full framework documentation
├── .opencode/skills/      # opencode skills (create-slides, search-images, run-notebook, reflect-and-learn)
└── .github/workflows/     # GitHub Pages static deployment
```

**Critical architecture facts:**
- **100% static** — no bundler. `dist/` contains manually copied Reveal.js + Vue 3 ESM Browser files.
- **Central init**: `slides_template/init.js` defines `mountSlideApp()` which wires Vue, components, Reveal, and auto-detects optional plugins.
- `package.json` only has `reveal-code-focus` — Node.js is NOT required to run the app.

## Course Development Commands

```bash
# Python environment (micromamba — use name "opencode")
micromamba create -n opencode -y -c conda-forge python=3.11 jupyter nbconvert numpy pandas plotly scipy scikit-learn
micromamba run -n opencode python3 script.py

# Serve locally
python3 -m http.server 8000

# Validate HTML files
python3 -c "
import glob
from html.parser import HTMLParser
for f in glob.glob('**/*.html', recursive=True):
    p = HTMLParser(); p.feed(open(f).read())
    print(f'OK: {f}')
"

# Run Jupyter notebooks
micromamba run -n opencode jupyter nbconvert --execute --to notebook notebook.ipynb

# Extract notebook images to standalone PNGs
python3 .opencode/skills/run-notebook/extract_notebook_images.py notebook.ipynb --output-dir images/

# Search & extract images for slides
python3 .opencode/skills/search-images/extract_images.py URL1 URL2

# Generate Dracula-themed plots from notebook
python3 .opencode/skills/export-plots/export_plots.py notebook.ipynb --output-dir ciencia-dados/images/
```

## Slide Wiring & Gotchas

### `mountSlideApp()` rules
- Load `slides_template/init.js` as a **regular `<script>`** (NOT `type="module"`) — it defines `mountSlideApp()` globally.
- Call `window.app = mountSlideApp();` in a regular `<script>` block after all plugin scripts are loaded.
- **Order matters**: load `socket.io` CDN **before** `init.js`, and `plugin/seminar/plugin.js` **after** `init.js`.
- `init.js` hardcodes `RevealMermaid` in the plugins array (line 79). **Every deck MUST load the mermaid script** (`https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin@11.6.0/plugin/mermaid/mermaid.js`) even if it doesn't use diagrams — omitting it causes `ReferenceError: RevealMermaid is not defined`.

### Chalkboard plugin
- **Use ONLY the local version** at `plugin/chalkboard/plugin.js`. The CDN version lacks custom keyboard shortcuts.

### Vue Components — critical usage rules

| Component | Critical Rule |
|-----------|---------------|
| `<header1>` | Cover slide only. Props: `aula`, `curso`, `title`, `title-size` |
| `<leader-line>` | **MUST use explicit close tag** `</leader-line>`. Self-closing `<leader-line />` consumes subsequent DOM elements. |
| `<code-block>` | Code with `<` or `>` (C/C++/Arduino) **must** be wrapped in `<script type="text/plain">` to prevent HTML parser mangling. |
| `<poll-question>` | Each question must be a **separate `<section>` inside a parent `<section>`** wrapper. |
| `<plotly-figure>` | Vue 3 does NOT resolve bare `window` globals in templates. For static charts, intercept `Vue.createApp` to inject constants as `globalProperties`. For interactive charts, replace `mountSlideApp()` entirely. See `create-slides/SKILL.md` for exact patterns. |

### Code highlighting synced with fragments
- Use `data-line-numbers="ALL-LINES|F1|F2|F3"` on `<code-block>`. First value = initial visible lines; subsequent values = highlighted lines per fragment step.
- `data-fragment-index` starts at **1** (0 = initial state). Each `<li class="fragment" data-fragment-index="N">` corresponds to the N-th value after the first in `data-line-numbers`.

### r-stack fragment synchronization
- When using `div.r-stack` with paired fragments (image + overlay), **both elements MUST share the same `data-fragment-index`** so they trigger simultaneously.
- Pattern: `<img class="fragment semi-fade-out" data-fragment-index="N" ... /><div class="fragment" data-fragment-index="N">...</div>`

## Content & Style Rules

### Language
- **All slide content in Brazilian Portuguese**. No Chinese characters. English technical terms are fine.

### Student-facing instructions
- Do **not** mention `micromamba`, `opencode`, or internal project environment/setup details in slides, notebooks, exercises, or comments intended for students.

### Images
- **All `<img>` must have `alt` text.**
- Validate images before committing: status 200, Content-Type starts with `image/`, size > 1KB.
- Include source attribution: `Fonte: [Site] ([License])`
- Wikimedia Commons `/thumb/.../Filename.svg.png` often returns 400/404 — use direct SVG URLs.
- Many Random Nerd Tutorials URLs have restructured and return 404.

### Structure
- **Super sections**: Wrap major topics in parent `<section>` elements for vertical navigation.
- **4-space indentation**: All content inside `<div class="slides">`.
- **No comments in code**: Do not add comments unless explicitly requested.

### Fragments
- Use fragments **sparingly** — only for step-by-step concept introduction, code walkthroughs, and exercise steps.
- Use `<ls-u>` (auto-fragmenting) only for: motivation slides, exercise steps, summaries.
- Use plain `<ul>` for: definitions, reference lists, informational content.

### Styling
- Dracula palette: bg `#282a36`, fg `#f8f8f2`, cyan `#8be9fd`, green `#50fa7b`, pink `#ff79c6`, red `#ff5555`, yellow `#f1fa8c`, purple `#bd93f9`
- `<h2>`: 42pt Impact, left-aligned
- `<li>`: 22pt, left-aligned
- Use inline `style=""` for one-off styling

### Content Flow (per lesson)
1. Cover (`<header1>`)
2. Review (previous lesson recap)
3. Motivation (why topic matters)
4. Concept sections (2-5 slides per concept)
5. Practical exercise
6. Summary

## CI / Deploy

- `.github/workflows/static.yml` deploys to GitHub Pages on every push to `main`.
- The workflow auto-generates `index.html` listing all `.html` files in the repo.
- No build step required — upload artifact is the raw repo contents.

## Post-Task Reflection Protocol

After completing any tasks (needed debugging, had new features, migrations, issues were found, user complained about something, etc.), **automatically** run the `reflect-and-learn` skill protocol:

1. **Reflect** — Did you encounter gotchas, discover new patterns, or learn library-specific details?
2. **Evaluate** — Where does this knowledge belong? (existing skill, AGENTS.md, ECOSSISTEMA.md, or new skill)
3. **Act** — Update the relevant file(s) with concise, actionable entries
4. **Notify** — Briefly tell the user what you learned and where you stored it

**Mandatory triggers** — run this protocol immediately after ANY of the following:
- You learned something new about the codebase, framework, or tools
- The user complained about something you did or corrected your approach
- You struggled and had to try multiple different ways before getting it right

Do NOT wait for the user to ask. Be proactive. Load the `reflect-and-learn` skill if you need the full checklist.

## Skills

Five opencode skills are available:

1. **create-slides** — Generate new Reveal.js slide files (load for detailed patterns and gotchas)
2. **search-images** — Find images via web search + deterministic extraction
3. **run-notebook** — Execute Jupyter notebooks and extract images
4. **reflect-and-learn** — Post-task reflection protocol for capturing and persisting learned patterns

## Reference Documentation

- `docs/ECOSSISTEMA.md` — Complete framework documentation (components, plugins, CSS, architecture)
- `.opencode/skills/create-slides/SKILL.md` — Detailed slide creation patterns and gotchas
