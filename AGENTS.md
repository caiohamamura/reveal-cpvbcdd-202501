# AGENTS.md — Reveal.js Slide Framework

This repository contains Reveal.js-based slide decks for IFSP Campus Capivari technical courses.

## Cold Start (No Context)

1. Read `AGENTS.md` (this file)
2. Read `docs/ECOSSISTEMA.md` for full framework documentation
3. Read `.opencode/skills/create-slides/SKILL.md` for slide creation patterns

## Repository Layout

```
reveal-cpvbcdd-202501/
├── AGENTS.md                  # This file — AI agent instructions
├── opencode.json              # opencode CLI configuration
├── package.json               # Node dependencies
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
├── .opencode/skills/          # opencode skills (create-slides, search-images, run-notebook, reflect-and-learn)
└── .github/workflows/         # GitHub Pages static deployment
```

## Course Development Commands

```bash
# Package management (use opencode environment)
micromamba create -n opencode -y -c conda-forge python=3.11 jupyter nbconvert numpy pandas plotly scipy scikit-learn
micromamba install -n opencode -y <package>
micromamba run -n opencode python3 script.py

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
micromamba run -n opencode jupyter nbconvert --execute --to notebook notebook.ipynb

# Extract notebook images
python3 .opencode/skills/run-notebook/extract_notebook_images.py notebook.ipynb --output-dir images/

# Search for images for slides
python3 .opencode/skills/search-images/extract_images.py URL1 URL2

# Generate Dracula-themed plots
python3 .opencode/skills/export-plots/export_plots.py notebook.ipynb --output-dir ciencia-dados/images/
```

## Slide Development Rules

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
- Do NOT use fragments in section header slides (e.g., slides with "Parte X" titles).

### Pedagogical Style

- **Schematic Content**: Avoid continuous text. Use schematic comparisons (e.g., `multi-col` layouts) and structured lists with clear points instead of long paragraphs.
- **Direct to Students**: Write slide content addressing the students directly. Do NOT include meta-commentary directed at the teacher (e.g., "O ponto didático aqui é...") in the slides.

### Content Flow (per lesson)

1. Cover (`<header1>`)
2. Review (previous lesson recap)
3. Motivation (why topic matters)
4. Concept sections (2-5 slides per concept)
5. Practical exercise
6. Summary

## Important Rules

- **Language**: All slide content in Brazilian Portuguese. No Chinese characters. English technical terms are fine.
- **Student-facing instructions**: Do not mention `micromamba`, `opencode`, or internal project environment/setup details in slides, notebooks, exercises, or comments intended for students.
- **Images**: All `<img>` must have `alt` text. Validate images (status 200, valid binary data, >1KB).
- **Attribution**: Include source attribution for images (`Fonte: [Site] ([License])`)
- **Super sections**: Wrap major topics in parent `<section>` elements for vertical navigation
- **4-space indentation**: All content inside `<div class="slides">`
- **No comments in code**: Do not add comments unless explicitly requested

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
5. **validate-slides** — Run deterministic static validation for slide decks (HTML parse, Chinese characters, local refs, image alt text)

## Google Drive Access (gogcli)

`gog` (from `gogcli` package) is installed at `/home/linuxbrew/.linuxbrew/opt/gogcli/bin/gog`.

```bash
GOG_KEYRING_PASSWORD=x /home/linuxbrew/.linuxbrew/opt/gogcli/bin/gog <command>
```

**Key gotchas:**
- Binary is named `gog`, not `gogcli`
- `/home/homebrew` does not exist; use `/home/linuxbrew/.linuxbrew/`
- Keyring password is `x` (from `.bashrc`), but stored tokens may be corrupted — re-auth if "integrity check failed"
- `gog search` does NOT support `--query`; use `gog ls --parent <folder-id>` to list folder contents
- Folder names are case-sensitive in Drive

**Auth flow (when tokens are corrupted):**
```bash
# Step 1: print auth URL
GOG_KEYRING_PASSWORD=x gog auth add <email> --remote --step 1 --services drive

# Step 2: paste redirect URL from browser
GOG_KEYRING_PASSWORD=x gog auth add <email> --remote --step 2 --auth-url '<redirect-url>' --services drive
```

**Navigate Drive folders:**
```bash
# Find folder by name
gog search "foldername" -a <email> -j

# List folder contents by ID
gog ls -a <email> -j --parent <folder-id> --max 100
```

## Reference Documentation

- `docs/ECOSSISTEMA.md` — Complete framework documentation (components, plugins, CSS, architecture)
- `.opencode/skills/create-slides/SKILL.md` — Detailed slide creation patterns and gotchas
