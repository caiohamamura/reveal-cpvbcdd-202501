# Ductor Home

This is the top-level `~/.ductor` directory.
The main Telegram assistant usually runs with cwd `workspace/`.

## Cold Start (No Context)

Read in this order:

1. `workspace/CLAUDE.md` (main behavior + Telegram rules)
2. `workspace/tools/CLAUDE.md` (tool routing)
3. `workspace/memory_system/MAINMEMORY.md` (long-term context)
4. `config/CLAUDE.md` (only for config changes)

## Repository Layout

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
├── .opencode/skills/          # opencode skills (create-slides, search-images, run-notebook)
└── .github/workflows/         # GitHub Pages static deployment
```

## Top-Level Layout

- `workspace/` - agent working area (tools, memory, cron tasks, skills, files)
- `config/config.json` - runtime configuration
- `sessions.json` - per-chat session state
- `cron_jobs.json` - cron registry
- `webhooks.json` - webhook registry
- `logs/` - runtime logs

## Multi-Agent System

You are one agent in a multi-agent system managed by a central Supervisor.

### Token Management

**IMPORTANT: Always use micromamba (`micromamba`) for Python packages — NEVER `pip install` or `python3 -m pip install`.**

If `micromamba` is missing in a checkout, report that notebook execution/package installation is blocked; do not fall back to `pip`.

- `~/.ductor/agents.json` is the single source of truth for all sub-agent
  bot tokens, allowed users, and model settings.
- The Supervisor reads `agents.json` at startup and merges each agent's
  token into its runtime config. **Your Telegram bot token comes from
  `agents.json`, not from `config/config.json`.**
- Never hardcode or copy bot tokens from other agents. If you need to
  interact with Telegram, the framework has already injected the correct
  token for you.

### Inter-Agent Communication

**Synchronous** (blocks until response):
```bash
python3 workspace/tools/agent_tools/ask_agent.py TARGET_AGENT "Your message"
```

**Course Development Commands**

```bash
# Package management (use opencode environment)
micromamba create -n opencode -y -c conda-forge python=3.11 jupyter nbconvert numpy pandas plotly scipy scikit-learn  # if env is missing
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

**Asynchronous** (returns immediately, response delivered via Telegram):
```bash
python3 workspace/tools/agent_tools/ask_agent_async.py TARGET_AGENT "Your message"
```

Use async for tasks that may take longer. Use sync for quick lookups.
See `workspace/tools/agent_tools/CLAUDE.md` for all agent management tools.

### Shared Knowledge

`~/.ductor/SHAREDMEMORY.md` contains facts shared across all agents
(server info, user preferences, infrastructure). Changes are automatically
synced into every agent's `MAINMEMORY.md` by the Supervisor.

- For agent-specific knowledge: use your own `memory_system/MAINMEMORY.md`.
- For cross-agent knowledge: use `SHAREDMEMORY.md` (via
  `workspace/tools/agent_tools/edit_shared_knowledge.py`).

## Operating Rules

- Use tool scripts in `workspace/tools/` for cron/webhook lifecycle changes.
Do not manually edit `cron_jobs.json` or `webhooks.json` for normal operations.
- When config changes are requested, edit only requested keys in `config/config.json`.
Then tell the user to run `/restart`.
- Save user-facing generated files in `workspace/output_to_user/` and send with
`<file:/absolute/path/to/output_to_user/...>`.
- Update `workspace/memory_system/MAINMEMORY.md` silently when durable user facts
or preferences are learned.

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
