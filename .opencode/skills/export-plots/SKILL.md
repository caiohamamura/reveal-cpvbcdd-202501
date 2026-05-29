---
name: export-plots
description: Export Plotly figures from Python or notebooks into standalone RevealD3 iframe HTML files for Reveal.js slides
---

# Export Plotly Figures for RevealD3 Slides

Use this skill when creating Plotly charts for slides. The default output is a standalone HTML file loaded by RevealD3 via `data-file`.

## Default Workflow

1. Generate one or more Plotly figures in Python.
2. Export them with `scripts/export_reveald3_plotly.py`.
3. Put the exported HTML under the course folder, usually `ciencia-dados/aulas/<plot-name>.html`.
4. Load the plot in the deck with:
   ```html
   <reveald3-plot file="aulas/<plot-name>.html" width="780px" height="460px"></reveald3-plot>
   ```
   or:
   ```html
   <div class="fig-container" data-file="aulas/<plot-name>.html" data-scroll="no"></div>
   ```
5. Add visible Reveal fragments beside/below the plot. The iframe `_transitions` array will receive the same zero-based fragment indexes.

## Python Script Example

```python
from pathlib import Path
import plotly.express as px
from export_reveald3_plotly import export_reveald3_plotly

df = px.data.iris()
fig0 = px.scatter(df, x="sepal_width", y="sepal_length", color_discrete_sequence=["#8be9fd"])
fig1 = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

export_reveald3_plotly(
    [fig0, fig1],
    Path("ciencia-dados/aulas/iris-step.html"),
    title="Iris",
)
```

## Notebook Example

```python
import sys
from pathlib import Path

sys.path.append(str(Path("..") / ".opencode" / "skills" / "export-plots" / "scripts"))
from export_reveald3_plotly import export_reveald3_plotly

export_reveald3_plotly(
    [fig_inicial, fig_colorido, fig_tendencia],
    Path("../aulas/meu-grafico.html"),
    title="Meu gráfico",
)
```

## CLI Example

Export JSON from Python:

```python
import json

with open("plot_steps.json", "w", encoding="utf-8") as f:
    json.dump([fig0.to_dict(), fig1.to_dict()], f)
```

Convert to standalone HTML:

```bash
python ../.opencode/skills/export-plots/scripts/export_reveald3_plotly.py plot_steps.json --output aulas/plot_steps.html --title "Plot Steps"
```

## Rules

- Prefer multiple complete Plotly figure states over manual DOM updates.
- Use `Plotly.react()` for initial rendering.
- Use `Plotly.animate()` for transitions between states.
- Keep trace order stable between states whenever possible.
- Set `uid` on traces when creating states manually.
- Use visible slide fragments with explanatory labels; avoid invisible empty fragments.
- Keep student-facing slides free of internal commands, paths, and environment details.

- **X-axis labels hidden under slide components**: Plotly's default bottom margin (=80) might be too tight if the iframe (<reveald3-plot>) height is small (e.g., 350px-400px) and there are banners/components underneath. Set margin=dict(t=50, b=90) (or higher) in ig.update_layout to ensure categorical X-axis labels are not cut off.
