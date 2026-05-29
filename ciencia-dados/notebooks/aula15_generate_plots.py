"""
Generate a RevealD3 Plotly chart comparing library loan periods
for the storytelling aula15 slides.
"""
import json
import sys
from pathlib import Path

sys.path.append(str(Path("..") / ".opencode" / "skills" / "export-plots" / "scripts"))

# We'll build the chart data directly since we don't need the full notebook pipeline

# Data: empréstimos por tipo de período (baseado nos dados da aula14)
periodos = ["Semana Normal", "Semana de Prova", "Recesso/Feriado"]
emprestimos_media = [55, 85, 25]
colors = ["#8be9fd", "#50fa7b", "#ff5555"]

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Bar(
    x=periodos,
    y=emprestimos_media,
    marker_color=colors,
    text=[f"{v}" for v in emprestimos_media],
    textposition="outside",
    textfont=dict(color="#f8f8f2", size=18),
    hoverinfo="x+y",
))

fig.update_layout(
    title=dict(
        text="Demanda sobe antes de provas e cai no recesso",
        font=dict(color="#f8f8f2", size=20),
        x=0.5,
    ),
    paper_bgcolor="#282a36",
    plot_bgcolor="#282a36",
    font=dict(color="#f8f8f2", family="Inter, sans-serif"),
    xaxis=dict(automargin=True, 
        title="Tipo de Período",
        gridcolor="#44475a",
        linecolor="#44475a",
        tickfont=dict(size=16),
    ),
    yaxis=dict(automargin=True, 
        title="Empréstimos Médios por Semana",
        gridcolor="#44475a",
        linecolor="#44475a",
        range=[0, 100],
        tickfont=dict(size=14),
    ),
    margin=dict(l=60, r=30, t=80, b=120),
    showlegend=False,
    bargap=0.35,
)

# Export as standalone RevealD3 HTML
html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>
  body {{ margin: 0; background: #282a36; }}
  #plot {{ width: 100%; height: 100%; }}
</style>
</head>
<body>
<div id="plot"></div>
<script>
var data = {json.dumps(fig.to_dict()["data"], default=str)};
var layout = {json.dumps(fig.to_dict()["layout"], default=str)};
layout.autosize = true;
Plotly.newPlot('plot', data, layout, {{displayModeBar: false, responsive: true}});
</script>
</body>
</html>
"""

output_path = Path("aulas/aula15-emprestimos-por-periodo.html")
output_path.write_text(html_content, encoding="utf-8")
print(f"Written to {output_path}")

# Also create a second chart: satisfaction scores by dimension
dimensoes = ["Satisfação Geral", "Apoio Docente", "Infraestrutura", "Clareza"]
scores_info = [4.0, 3.5, 3.25, 3.75]
scores_adm = [3.0, 2.5, 2.50, 3.00]

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    name="Informática",
    x=dimensoes,
    y=scores_info,
    marker_color="#8be9fd",
    text=[f"{v:.1f}" for v in scores_info],
    textposition="outside",
    textfont=dict(color="#8be9fd", size=14),
))

fig2.add_trace(go.Bar(
    name="Administração",
    x=dimensoes,
    y=scores_adm,
    marker_color="#ff79c6",
    text=[f"{v:.1f}" for v in scores_adm],
    textposition="outside",
    textfont=dict(color="#ff79c6", size=14),
))

fig2.update_layout(
    title=dict(
        text="Informática avalia melhor em todas as dimensões",
        font=dict(color="#f8f8f2", size=18),
        x=0.5,
    ),
    paper_bgcolor="#282a36",
    plot_bgcolor="#282a36",
    font=dict(color="#f8f8f2", family="Inter, sans-serif"),
    xaxis=dict(automargin=True, 
        gridcolor="#44475a",
        linecolor="#44475a",
        tickfont=dict(size=14),
    ),
    yaxis=dict(automargin=True, 
        title="Nota Média (1-5)",
        gridcolor="#44475a",
        linecolor="#44475a",
        range=[0, 5.5],
        tickfont=dict(size=13),
    ),
    barmode="group",
    bargap=0.25,
    bargroupgap=0.1,
    margin=dict(l=60, r=30, t=80, b=120),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.3,
        xanchor="center",
        x=0.5,
        font=dict(size=14),
    ),
)

html_content2 = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>
  body {{ margin: 0; background: #282a36; }}
  #plot {{ width: 100%; height: 100%; }}
</style>
</head>
<body>
<div id="plot"></div>
<script>
var data = {json.dumps(fig2.to_dict()["data"], default=str)};
var layout = {json.dumps(fig2.to_dict()["layout"], default=str)};
layout.autosize = true;
Plotly.newPlot('plot', data, layout, {{displayModeBar: false, responsive: true}});
</script>
</body>
</html>
"""

output_path2 = Path("aulas/aula15-satisfacao-por-curso.html")
output_path2.write_text(html_content2, encoding="utf-8")
print(f"Written to {output_path2}")
