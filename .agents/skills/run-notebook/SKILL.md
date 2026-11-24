---
name: run-notebook
description: >-
  Execute Jupyter notebooks (.ipynb) via nbconvert, verify cell outputs without
  errors, and extract embedded PNG plots for Reveal.js slides. Use when running
  course notebooks or extracting figures from notebooks in ia/cadernos/ or
  ciencia-dados/notebooks/.
---

# Run Notebook & Extract Images

Execute `.ipynb` files in the `opencode` micromamba environment and extract embedded `image/png` outputs cleanly.

## Commands

Run execution + image extraction together:
```bash
micromamba run -n opencode python3 .agents/skills/run-notebook/scripts/run_notebook.py \
  path/to/notebook.ipynb --output-dir path/to/images/
```

Extract images from an already-executed notebook (no re-execution):
```bash
python3 .agents/skills/run-notebook/scripts/run_notebook.py \
  path/to/notebook.ipynb --extract-only --output-dir path/to/images/
```

Execute only (verify zero cell errors):
```bash
micromamba run -n opencode python3 .agents/skills/run-notebook/scripts/run_notebook.py \
  path/to/notebook.ipynb --exec-only --timeout 300
```

The script verifies every cell output for runtime errors, decodes `image/png` outputs to PNG files, validates size >1 KB, and writes `images_manifest.json`.

## Gotchas

- **Preserve originals**: `jupyter nbconvert --execute --to notebook` overwrites in-place unless `--output executed.ipynb` is set (`scripts/run_notebook.py` executes in a temp directory to protect source notebooks).
- **Commit before stashing notebooks**: Stashing edited notebooks before committing other work risks losing cell outputs.
- **Plotly in exported notebooks**: `nbconvert --execute` emits `application/vnd.plotly.v1+json`, which does not render statically in VS Code/GitHub without an extension. Install `kaleido` and set `import plotly.io as pio; pio.renderers.default = 'png'` (or `'svg'`) when static embedded plots are needed.
- **Wisconsin Breast Cancer dataset**: `load_breast_cancer()` encodes `0 = malignant`, `1 = benign`. For novelty/anomaly detection, train on benign (`y=1`) and test against malignant (`y=0`).
