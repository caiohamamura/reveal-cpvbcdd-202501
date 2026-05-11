# AGENTS.md — reveal-cpvbcdd-202501

## Project Overview

This is an **educational slide framework** built on Reveal.js for IFSP Capivari's CPVBCDD program. It produces interactive HTML slide decks for courses: **IoT**, **BDD1** (Banco de Dados I), **BDD2** (Banco de Dados II), and **Ciência de Dados**.

All slide content is in **Brazilian Portuguese**. Technical terms may stay in English.

## Repository Structure

```
reveal-cpvbcdd-202501/
├── AGENTS.md                  # This file — AI agent instructions
├── opencode.json              # opencode CLI configuration
├── iot/                       # IoT course slides (.html)
├── bdd1/                      # Banco de Dados I slides (.html)
├── bdd2/                      # Banco de Dados II slides (.html)
├── ciencia-dados/             # Data Science slides (.html) + images/, notebooks/, aulas/
├── dist/                      # Reveal.js core, themes, Vue.js, custom.css (built assets)
├── plugin/                    # Reveal.js plugins (highlight, markdown, math, notes, poll, seminar, chalkboard, customcontrols, zoom, chart, search)
├── components/                # Vue.js custom components (components.js)
├── slides_template/           # Shared templates (header1.js, init.js)
├── img/                       # Shared images (logo, background)
├── docs/                      # ECOSSISTEMA.md — full framework documentation
├── bin/                       # micromamba binary
├── .opencode/skills/          # opencode skills (create-slides, search-images, export-plots, run-notebook)
└── .github/workflows/         # GitHub Pages static deployment
```

## Tech Stack

- **Reveal.js 5.2.1** — slide engine
- **Vue.js 3** (ESM Browser) — reactive components
- **highlight.js** — code syntax highlighting
- **Mermaid** — diagrams
- **KaTeX/MathJax** — math equations
- **LeaderLine** — connector arrows between elements
- **Custom plugins** — poll, seminar (live voting/classroom), chalkboard, customcontrols

## Key Commands

There is no build step. Slides are static HTML files served directly.

**IMPORTANT: Always use micromamba (`./bin/micromamba`) for Python packages — NEVER `pip install` or `python3 -m pip install`.**

```bash
# Package management (use opencode environment)
./bin/micromamba install -n opencode -y <package>
./bin/micromamba run -n opencode python3 script.py

# Serve locally (any static server)
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
jupyter nbconvert --execute --to notebook notebook.ipynb

# Extract notebook images
python3 .opencode/skills/run-notebook/extract_notebook_images.py notebook.ipynb --output-dir images/

# Search for images for slides
python3 .opencode/skills/search-images/extract_images.py URL1 URL2

# Generate Dracula-themed plots
python3 .opencode/skills/export-plots/export_plots.py notebook.ipynb --output-dir ciencia-dados/images/
```

## Slide Creation Conventions

### File Naming

- IoT: `iot/NN-topic-description.html` (e.g., `13-sensores-atuadores-glm.html`)
- BDD1: `bdd1/aulaNN.html`
- BDD2: `bdd2/topic-name.html`
- Ciência de Dados: `ciencia-dados/aulaNN-topic.html`

### HTML Boilerplate

All slides must follow the exact boilerplate in `.opencode/skills/create-slides/SKILL.md`. Key requirements:

1. Use `../dist/` relative paths for CSS and JS
2. Load plugins in correct order (see SKILL.md)
3. Call `window.app = mountSlideApp()` from `slides_template/init.js`
4. Theme: `dracula.css` for all courses
5. All code blocks use `<script type="text/plain">` wrapper to prevent HTML parser mangling
6. Mermaid graphs have **0 indentation** inside `<pre>` (whitespace-sensitive)

### Vue Components

| Component | Purpose |
|-----------|---------|
| `<header1>` | Cover slide (props: `aula`, `curso`, `title`, `title-size`) |
| `<multi-col>` | Multi-column layouts (prop: `cols`, `style="gap:15px"`) |
| `<ls-u>` | Auto-fragmenting bullet list |
| `<code-block>` | Code with copy button (attr: `lang`) |
| `<highlight-box>` | Callout boxes |
| `<copy-btn>` | Copy button for tables |
| `<md>` | Markdown rendering |
| `<leader-line>` | Arrow connectors (MUST use explicit close tag) |
| `<poll-question>` | Interactive live voting |

### Styling

- Dracula palette: bg `#282a36`, fg `#f8f8f2`, cyan `#8be9fd`, green `#50fa7b`, pink `#ff79c6`, red `#ff5555`, yellow `#f1fa8c`, purple `#bd93f9`
- `<h2>`: 42pt Impact, left-aligned
- `<li>`: 22pt, left-aligned
- Use inline `style=""` for one-off styling

### Fragment Usage

- Use fragments SPARINGLY — only for step-by-step concept introduction, code walkthroughs, and exercise steps
- Use `<ls-u>` (auto-fragment) only for: motivation slides, exercise steps, summaries
- Use plain `<ul>` for: definitions, reference lists, informational content

### Content Flow (per lesson)

1. Cover (`<header1>`)
2. Review (previous lesson recap)
3. Motivation (why topic matters)
4. Concept sections (2-5 slides per concept)
5. Practical exercise
6. Summary

## Important Rules

- **Language**: All slide content in Brazilian Portuguese. No Chinese characters. English technical terms are fine.
- **Images**: All `<img>` must have `alt` text. Validate images (status 200, valid binary data, >1KB).
- **Attribution**: Include source attribution for images (`Fonte: [Site] ([License])`)
- **Super sections**: Wrap major topics in parent `<section>` elements for vertical navigation
- **4-space indentation**: All content inside `<div class="slides">`
- **No comments in code**: Do not add comments unless explicitly requested

## Post-Task Reflection Protocol

After completing any non-trivial task (debugging, new features, migrations, etc.), **automatically** run the `reflect-and-learn` skill protocol:

1. **Reflect** — Did you encounter gotchas, discover new patterns, or learn library-specific details?
2. **Evaluate** — Where does this knowledge belong? (existing skill, AGENTS.md, ECOSSISTEMA.md, or new skill)
3. **Act** — Update the relevant file(s) with concise, actionable entries
4. **Notify** — Briefly tell the user what you learned and where you stored it

Do NOT wait for the user to ask. Be proactive. Load the `reflect-and-learn` skill if you need the full checklist.

## Skills

Five opencode skills are available:

1. **create-slides** — Generate new Reveal.js slide files (load for detailed patterns and gotchas)
2. **search-images** — Find images via web search + deterministic extraction
3. **export-plots** — Generate Dracula-themed matplotlib/seaborn plots from notebooks
4. **run-notebook** — Execute Jupyter notebooks and extract images
5. **reflect-and-learn** — Post-task reflection protocol for capturing and persisting learned patterns

## Reference Documentation

- `docs/ECOSSISTEMA.md` — Complete framework documentation (components, plugins, CSS, architecture)
- `.opencode/skills/create-slides/SKILL.md` — Detailed slide creation patterns and gotchas
