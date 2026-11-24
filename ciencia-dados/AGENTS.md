# AGENTS.md — Ciência de Dados (`ciencia-dados/`)

Course-specific guidelines for **Ciência de Dados** decks, notebooks, and interactive plots. Follows root `../AGENTS.md`, `export-plots`, `run-notebook`, `create-slides`, and `slide-design`.

## Directory Layout

- `*.html` — Reveal.js decks (`aula-09-projeto-completo.html`, `aula12-cluster-analysis.html`, `aula13-deteccao-anomalias.html`, `pca-e-lda.html`, etc.).
- `notebooks/` — Source `.ipynb` notebooks, Python helper scripts, and R plot refinement scripts (`Rscript fix_plots.R`).
- `aulas/` — Standalone RevealD3 + Plotly HTML plots loaded via `<reveald3-plot>`.
- `images/` — Versioned static plots and visual assets.

## Course-Specific Patterns

- **Interactive Plotly charts (default)**: Use RevealD3 (`../plugin/reveald3/reveald3.js`) + `<reveald3-plot file="aulas/<plot>.html" width="780px" height="460px">` generated with:
  ```bash
  python3 .agents/skills/export-plots/scripts/export_reveald3_plotly.py plot_steps.json --output ciencia-dados/aulas/<plot>.html
  ```
  - Define `_transitions` inside the iframe HTML and use `Plotly.animate()` with stable trace `uid`s for step-by-step updates; do not fall back to `Plotly.react()` when only styling/positions/annotations change.
  - Use `<plotly-figure>` only when maintaining unmigrated legacy decks.
- **Dracula plot palette**: `['#8be9fd', '#ff5555', '#f1fa8c', '#50fa7b', '#bd93f9', '#ff79c6', '#6272a4']`.
- **Reproducible outputs & data**:
  - Back every Python output shown on slides with a real script or notebook in `notebooks/`.
  - Commit concrete CSV files used with `pd.read_csv()` under `ciencia-dados/`, even for fictitious classroom datasets.
  - Extract notebook PNG outputs with `python3 .agents/skills/run-notebook/scripts/run_notebook.py <nb.ipynb> --extract-only --output-dir ciencia-dados/images/`.
- **Library & dataset gotchas**:
  - `load_breast_cancer()` uses `0 = malignant`, `1 = benign`; for novelty/anomaly detection, train on benign (`y=1`) and evaluate against malignant (`y=0`).
  - For `statsmodels.OLS`, build dummies as numeric integers: `pd.get_dummies(..., dtype=int)`.
  - For `statsmodels.seasonal_decompose()`, edge trend values are `NaN`; cite the last valid trend date.
  - When indexing a SciPy sparse matrix with a pandas boolean mask, pass `mask.to_numpy()`.

## Verification

```bash
python3 .agents/skills/validate-slides/scripts/validate_slide_deck.py ciencia-dados/<deck>.html --check-orphans
```
