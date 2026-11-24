# AGENTS.md — Banco de Dados II (`bdd2/`)

Course-specific guidelines for **Banco de Dados II** decks and lab materials. Follows root `../AGENTS.md`, `create-slides`, `slide-design`, and `validate-slides`.

## Directory Layout

- `*.html` — Student-facing Reveal.js slide decks (lowercase descriptive names with hyphens/underscores matching nearby files).
- `planos/*.md` — Lesson plans, practice scripts, and classroom guides.
- `planos/*.sql` — Seed data, schemas, and exercises referenced by slides.
- `planos/<aula>_assets/` — Lesson-specific diagrams, screenshots, and notebook-rendered assets (keep BDD2-specific assets inside `bdd2/planos/`).
- `generate_exams.py` — Deterministic exam generator (keep fixed random seed for reproducibility).

## Course-Specific Conventions

- **Graph-heavy visuals**: For graph/schema diagrams reused across headers or slides, prefer notebook-rendered PNG/SVG under `planos/<aula>_assets/` (keeping the generating notebook beside the asset) instead of complex inline Mermaid.
- **Data consistency**: Whenever a slide shows a SQL, Cypher, or MongoDB query alongside a result table, include enough seed data earlier in the deck so the query actually returns the shown rows.
- **`aula14-neo4j-grafos.html`**: Keep the author-to-post relationship in Portuguese as `Pessoa-[:PUBLICA]->Post` (do not rename to `POSTS`).
- **MongoDB verification**: `mongodb` from conda-forge provides `mongod` but not `mongosh`; verify classroom `mongosh` commands using a separate `mongosh` installation (`npm install -g mongosh`).
- **Python packages**: Use `micromamba` (`opencode` environment) for Python/notebook work rather than system `pip`.

## Verification & Git Workflow

```bash
# Static validation
python3 .agents/skills/validate-slides/scripts/validate_slide_deck.py bdd2/<deck>.html

# Local preview (from repository root)
python3 -m http.server 8123
```

Verify navigation, fragments, code highlighting, SQL/Cypher/Mongo examples, and 960×700 overflow (`check_overflow.js`) before finalizing. Use short imperative commit messages scoped to the lesson/change.
