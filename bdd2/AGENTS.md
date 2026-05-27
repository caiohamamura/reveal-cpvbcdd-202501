# Repository Guidelines

## Project Structure & Module Organization

This directory contains Banco de Dados II course materials for the shared Reveal.js slide framework.

- `*.html`: student-facing Reveal.js slide decks, one lesson/topic per file.
- `planos/*.md`: lesson plans, practice scripts, and instructor/student guides.
- `planos/*.sql`: SQL datasets and classroom exercises used by the decks.
- `planos/*.png`: local diagrams and images used by lesson materials.
- For graph-heavy visuals reused in headers or multiple slides, generate a notebook-rendered PNG/SVG under `planos/<aula>_..._assets/` and embed that asset instead of inline Mermaid. Keep the notebook next to the asset so the visual is reproducible.
- Shared framework files live one level up: `../dist/`, `../plugin/`, `../components/`, `../slides_template/`, and `../img/`.

Keep new BDD2-specific assets inside `bdd2/planos/` unless they are reused across courses.

## Build, Test, and Development Commands

- `python3 -m http.server 8000` from the repository root: serves decks locally. Open `http://localhost:8000/bdd2/materialized_views.html`.
- `python3 -c "from html.parser import HTMLParser; import glob; [HTMLParser().feed(open(f).read()) for f in glob.glob('bdd2/**/*.html', recursive=True)]"`: quick HTML parse check.
- `git diff -- bdd2`: review only changes in this module before committing.

This is a static presentation repository; there is no project-wide build script or unit test suite for `bdd2`.

## Coding Style & Naming Conventions

Use 4-space indentation inside `<div class="slides">`. Write all slide content in Brazilian Portuguese; English technical terms are acceptable. Do not mention internal tooling or environment setup in student-facing materials.

Prefer existing Vue components such as `<header1>`, `<multi-col>`, `<ls-u>`, `<code-block>`, `<highlight-box>`, and `<leader-line></leader-line>`. Use inline `style=""` for one-off slide adjustments and keep the Dracula palette consistent with existing decks.

Name new decks with descriptive lowercase filenames, using hyphens or underscores consistently with nearby files, for example `materialized_views.html` or `jsonb-nosql.html`.

Keep visible slide text personal and direct. Avoid course codes, institutional labels, and other internal meta references in student-facing instructions; prefer phrasing like "aqui", "neste caso", and generic placeholders such as `local` or `ifsp`.

## Testing Guidelines

Before opening a pull request, run the HTML parse check and manually open changed decks through a local static server. Verify navigation, fragments, code highlighting, Vue components, images, and SQL snippets. Every `<img>` must include meaningful `alt` text and should reference valid local assets or attributed external sources.

For MongoDB lesson decks, `mongodb` from conda-forge provides `mongod` but not `mongosh`. To verify exact student `mongosh` commands, use a micromamba test environment with MongoDB server plus a separately installed `mongosh` client.

## Commit & Pull Request Guidelines

Recent commits use short imperative summaries, for example `Consolidate Aula12 clustering deck` and `Fix K-Means demo: remove duplicate label`. Follow that style: concise, specific, and focused on the changed lesson or behavior.

Pull requests should include a brief description, changed deck paths, manual verification notes, and screenshots or screen recordings when visual layout changes are significant. Link related issues or classroom requests when available.

## Agent-Specific Instructions

Follow the root `AGENTS.md` and `docs/ECOSSISTEMA.md` for framework conventions. Use `micromamba` for Python package work if notebooks or data scripts are involved; do not install packages with `pip`.

**Always commit and push after making changes.** Do not wait for the user to ask.

**Post-task reflection**: After learning something new, receiving user correction/complaint, or struggling through multiple attempts, immediately run the `reflect-and-learn` skill protocol from the root `AGENTS.md`. Do not wait to be asked.
