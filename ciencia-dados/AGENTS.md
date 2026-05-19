# AGENTS.md — Ciência de Dados (IFSP Capivari)

Subagent for the Data Science course within the Reveal.js slide framework.

## Course Scope

4 slide decks covering supervised learning, clustering, anomaly detection, and dimensionality reduction.

```
ciencia-dados/
├── AGENTS.md                         # This file
├── aula-09-projeto-completo.html     # ML pipeline (supervised)
├── aula12-cluster-analysis.html      # K-Means, hierarchical clustering
├── aula13-deteccao-anomalias.html    # Isolation Forest, LOF, novelty detection
├── pca-e-lda.html                    # PCA, LDA, feature reduction
├── notebooks/                        # Jupyter notebooks + R scripts
│   ├── aula-09-projeto-completo.ipynb
│   ├── aula12_clustering.ipynb
│   ├── aula13-deteccao-anomalias.ipynb
│   ├── aula13-gerar-figuras.ipynb
│   ├── aula13-ilustracoes-algoritmos.ipynb
│   └── *.R                           # Plot refinement scripts
├── images/                           # Extracted plots for slides
└── aulas/                            # Sub-lesson content
```

## Key Commands

```bash
# Serve slides locally
python -m http.server 8000

# Execute notebook + extract images
jupyter nbconvert --execute --to notebook --output executed.ipynb notebook.ipynb
python .opencode/skills/run-notebook/extract_notebook_images.py notebook.ipynb --output-dir images/

# Rebuild Dracula-themed plots from R scripts
python .opencode/skills/export-plots/export_plots.py notebook.ipynb --output-dir images/

# Validate all HTML images (status 200, >1KB, image MIME)
python -c "
import glob, requests
for f in glob.glob('*.html'):
    html = open(f).read()
    for url in re.findall(r'<img[^>]+src=\"([^\"]+)\"', html):
        r = requests.head(url)
        assert r.status_code == 200 and 'image' in r.headers.get('content-type','')
"
```

## Slide Patterns Specific to Ciência de Dados

### Plotly charts in slides
- Load Plotly.js CDN before the component: `<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>`
- Use `<plotly-figure :traces="tracesVar" :layout="layoutVar">` from `components/components.js`
- For interactive step-by-step demos (e.g. K-Means centroids), override `mountSlideApp()` to inject reactive state — see `.opencode/skills/create-slides/SKILL.md` → "Interactive Plotly with Vue reactivity"
- Export Plotly JSON from Python via `fig.to_dict()`, clean `None` values before embedding in JS
- Vue 3 does NOT resolve bare `window` globals in templates — inject via `globalProperties` or custom `mountSlideApp()`

### Dracula plot colors
```python
dracula = ['#8be9fd', '#ff5555', '#f1fa8c', '#50fa7b', '#bd93f9', '#ff79c6', '#6272a4']
```

### Notebook → Slide pipeline
1. Generate figures in notebook
2. Export as JSON: `json.dump(fig.to_dict(), f)`
3. Convert to JS constants: `const NAME_TRACES = [...]; const NAME_LAYOUT = {...};`
4. Reference in `<plotly-figure :traces="NAME_TRACES" :layout="NAME_LAYOUT">`

### Standalone Plotly figure generation (when Jupyter env is missing packages)
- Create a Python script with the same plotting code + `write_plotly_js()` helper
- Run directly with `python script.py` after `pip install numpy pandas plotly scikit-learn`
- This avoids `jupyter nbconvert --execute` dependency issues and is faster for iterative plot tuning
- Example: `notebooks/run_svm_plots.py` → outputs `images/plotly/aula13_oneclass_svm_figures.js`

### R Scripts for plot fixes
- `fix_plots.R`, `regenerate_plots.R` — fix/regenerate Python-level plot aesthetics
- `fix_roc.R`, `roc_only.R` — ROC curve visualization fixes
- Run with: `Rscript fix_plots.R`

## Dataset Gotchas

- **Wisconsin Breast Cancer** (`load_breast_cancer()`): 0=malignant, 1=benign. For novelty/anomaly detection, train on benign (y=1), test against malignant (y=0 — the anomaly).
- **Class imbalance**: common in anomaly detection lessons. Document class semantics explicitly in notebook headers.

## Framework Integration

This directory follows the same patterns as the root Reveal.js framework:
- All `.html` files use `mountSlideApp()` from `../slides_template/init.js`
- Vue components from `../components/components.js` and `../slides_template/header1.js`
- Dracula theme (`../dist/theme/dracula.css`)
- Plugin scripts from `../plugin/`
- 4-space indentation inside `<div class="slides">`
- All content in Brazilian Portuguese

See `../AGENTS.md` for framework-wide rules, `../docs/ECOSSISTEMA.md` for component docs, and `../.opencode/skills/create-slides/SKILL.md` for slide creation gotchas.
