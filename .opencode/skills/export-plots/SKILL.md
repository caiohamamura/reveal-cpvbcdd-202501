---
name: export-plots
description: Generate beautiful Dracula-themed plots from Python code for use in Reveal.js slides
license: MIT
compatibility: opencode
metadata:
  audience: instructors
  domain: education
---

## What I do

- Generate publication-quality PNG images from Python plotting code (matplotlib/seaborn/altair)
- Apply a **Dracula dark theme** that matches the Reveal.js slide background (`#282a36`)
- Save images at high resolution to `ciencia-dados/images/` for direct use in `<img>` tags
- Validate generated images (size > 1KB, valid PNG format)
- Support: scatterplot, boxplot, heatmap, lineplot, dendrogram, radar plot, countplot

## When to use me

Use this skill when creating slides for data science lessons that need high-quality visualizations extracted from Jupyter notebooks or custom Python plotting code.

## How I work

### Phase 1: Write or extract the plotting code

Extract the plotting code from the source notebook's code cells. Adapt it for standalone execution with the Dracula theme.

### Phase 2: Apply Dracula theme

Use the `export_plots.py` script which sets up the theme automatically:

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Dracula theme colors
DRACULA = {
    "background": "#282a36",
    "current_line": "#44475a",
    "selection": "#44475a",
    "foreground": "#f8f8f2",
    "comment": "#6272a4",
    "cyan": "#8be9fd",
    "green": "#50fa7b",
    "orange": "#ffb86c",
    "pink": "#ff79c6",
    "purple": "#bd93f9",
    "red": "#ff5555",
    "yellow": "#f1fa8c",
}

sns.set_style("darkgrid", {"axes.facecolor": DRACULA["background"],
                           "figure.facecolor": DRACULA["background"],
                           "grid.color": DRACULA["current_line"],
                           "text.color": DRACULA["foreground"],
                           "axes.labelcolor": DRACULA["foreground"],
                           "xtick.color": DRACULA["foreground"],
                           "ytick.color": DRACULA["foreground"]})
```

### Phase 3: Generate and save images

```bash
python3 .opencode/skills/export-plots/export_plots.py \
  ciencia-dados/aulas/aula12_cluster/Aula10_cluster.ipynb \
  --output-dir ciencia-dados/images/ \
  --dpi 150
```

Or write standalone Python scripts that:
1. Load data (from CSV URL or gist)
2. Preprocess (same steps as notebook)
3. Generate each plot with Dracula theme
4. Save as high-DPI PNG

### Phase 4: Validate images

After generation, verify each image:
```bash
python3 .opencode/skills/export-plots/export_plots.py --check ciencia-dados/images/*.png
```

The check verifies:
- File size > 1024 bytes
- Valid PNG header (`\x89PNG`)
- Reasonable dimensions (>= 100px on each side)

### Example: Complete workflow

```bash
# 1. Generate all plots for the cluster lecture
python3 .opencode/skills/export-plots/generate_cluster_plots.py

# 2. Verify outputs
python3 .opencode/skills/export-plots/export_plots.py --check ciencia-dados/images/

# 3. Reference in slides
# <img src="images/scatter-clusters.png" alt="Scatter plot: Income vs Spending by cluster">
```

### Image naming convention

Use descriptive names that include the plot type:
- `dendrograma.png` — hierarchical clustering dendrogram
- `cotovelo.png` — elbow method plot
- `scatter-gasto-income.png` — scatter plot Income vs Spending by cluster
- `boxplot-consumo.png` — box plot of consumption per cluster
- `radar-clusters.png` — radar-boxplot multivariate view
- `kmeans-inertia.png` — K-Means inertia vs K plot
- `dbscan-demo.png` — DBSCAN clustering demo
