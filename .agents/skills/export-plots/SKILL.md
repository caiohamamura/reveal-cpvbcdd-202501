---
name: export-plots
description: >-
  Export Plotly figures from Python scripts or Jupyter notebooks into standalone
  RevealD3 iframe HTML files with smooth fragment-driven transitions. Use when
  creating interactive or animated data charts for Reveal.js slides.
---

# Export Plotly Figures for RevealD3 Slides

Export Plotly figures as standalone HTML files loaded via `<reveald3-plot>` (RevealD3 iframe pattern).

## Workflow

1. Build one or more Plotly figure states in Python (using Dracula palette `['#8be9fd', '#ff5555', '#f1fa8c', '#50fa7b', '#bd93f9', '#ff79c6', '#6272a4']`).
2. Export with [scripts/export_reveald3_plotly.py](./scripts/export_reveald3_plotly.py) into `<course>/aulas/<plot-name>.html`.
3. Include `<script src="../plugin/reveald3/reveald3.js"></script>` before `init.js` in the slide deck (`init.js` auto-detects `window.Reveald3`).
4. Embed in the slide:
   ```html
   <reveald3-plot file="aulas/<plot-name>.html" width="780px" height="460px"></reveald3-plot>
   ```
5. Add visible slide fragments beside/below the plot; `_transitions` inside the exported HTML syncs to zero-based fragment indices.

## Usage Examples

### From Python / Notebook

```python
import sys
from pathlib import Path

sys.path.append(str(Path("..") / ".agents" / "skills" / "export-plots" / "scripts"))
from export_reveald3_plotly import export_reveald3_plotly

export_reveald3_plotly(
    [fig_inicial, fig_passo_1, fig_passo_2],
    Path("../aulas/meu-grafico.html"),
    title="Meu gráfico",
)
```

### From CLI

```bash
python3 .agents/skills/export-plots/scripts/export_reveald3_plotly.py \
  plot_steps.json --output ciencia-dados/aulas/plot_steps.html --title "Plot Steps"
```

## Rules & Gotchas

- Prefer multiple complete figure states over manual DOM mutation.
- Keep trace order stable and set `uid` on traces so `Plotly.animate()` interpolates smoothly.
- Use visible slide fragments with explanatory labels (never invisible empty divs).
- **Bottom margin clipping**: When `<reveald3-plot>` height is compact (350–400 px), Plotly's default bottom margin (`b=80`) can clip categorical X-axis labels; set `margin=dict(t=50, b=90)` (or higher) in `fig.update_layout(...)`.
- **Plotly 6.x**: `colorbar.titlefont` was removed — use `colorbar=dict(title=dict(text='...', font=dict(color='...')))`.
- Never include internal paths or environment commands in student-facing slides.
