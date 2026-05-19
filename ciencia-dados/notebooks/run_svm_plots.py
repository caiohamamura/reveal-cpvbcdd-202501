import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.utils import PlotlyJSONEncoder
from pathlib import Path
import json

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

DRACULA = {
    'bg': '#282a36',
    'fg': '#f8f8f2',
    'cyan': '#8be9fd',
    'green': '#50fa7b',
    'pink': '#ff79c6',
    'red': '#ff5555',
    'yellow': '#f1fa8c',
    'purple': '#bd93f9',
    'muted': '#6272a4',
}

def apply_dracula(fig, title=None):
    fig.update_layout(
        title=title,
        template=None,
        paper_bgcolor=DRACULA['bg'],
        plot_bgcolor=DRACULA['bg'],
        font=dict(color=DRACULA['fg']),
        margin=dict(l=60, r=30, t=60, b=55),
        showlegend=True,
        legend=dict(orientation='h', y=-0.25),
    )
    fig.update_xaxes(gridcolor='#44475a', zerolinecolor=DRACULA['muted'])
    fig.update_yaxes(gridcolor='#44475a', zerolinecolor=DRACULA['muted'])
    return fig

def clean_none(obj):
    if isinstance(obj, dict):
        return {k: clean_none(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [clean_none(v) for v in obj]
    return obj

def slide_export_path():
    cwd = Path.cwd().resolve()
    if cwd.name == 'notebooks' and cwd.parent.name == 'ciencia-dados':
        return cwd.parent / 'images' / 'plotly' / 'aula13_oneclass_svm_figures.js'
    return cwd / 'ciencia-dados' / 'images' / 'plotly' / 'aula13_oneclass_svm_figures.js'

def write_plotly_js(figures, output_path):
    lines = []
    for name, fig in figures.items():
        payload = clean_none(fig.to_dict())
        payload['layout'].pop('template', None)
        traces = json.dumps(payload['data'], ensure_ascii=False, cls=PlotlyJSONEncoder)
        layout = json.dumps(payload['layout'], ensure_ascii=False, cls=PlotlyJSONEncoder)
        lines.append(f"const {name}_TRACES = {traces};\n")
        lines.append(f"const {name}_LAYOUT = {layout};\n")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(lines), encoding='utf-8')

# ============================================================
# 1. Dados sintéticos: círculos concêntricos
# ============================================================
n_normal = 80
n_anom = 15

theta_n = np.random.uniform(0, 2*np.pi, n_normal)
r_n = np.random.uniform(1.0, 2.5, n_normal) + np.random.normal(0, 0.12, n_normal)
X_normal = np.column_stack([r_n * np.cos(theta_n), r_n * np.sin(theta_n)])

theta_a = np.random.uniform(0, 2*np.pi, n_anom)
r_a = np.random.uniform(4.0, 5.5, n_anom) + np.random.normal(0, 0.18, n_anom)
X_anom = np.column_stack([r_a * np.cos(theta_a), r_a * np.sin(theta_a)])

print(f"Total: {len(X_normal)+len(X_anom)} pontos | Normais: {n_normal} | Anomalias: {n_anom}")

# ============================================================
# 2. Figura: Dados originais — não linearmente separáveis
# ============================================================
fig_original = go.Figure()
fig_original.add_trace(go.Scatter(
    x=X_normal[:, 0], y=X_normal[:, 1],
    mode='markers', name='Normal (raio pequeno)',
    marker=dict(color=DRACULA['cyan'], size=9, opacity=0.7),
))
fig_original.add_trace(go.Scatter(
    x=X_anom[:, 0], y=X_anom[:, 1],
    mode='markers', name='Anomalia (raio grande)',
    marker=dict(color=DRACULA['red'], size=11, symbol='x', line=dict(width=2, color=DRACULA['red'])),
))
fig_original.add_shape(type='line', x0=-6, y0=0, x1=6, y1=0,
                       line=dict(color=DRACULA['yellow'], width=2, dash='dash'))
fig_original.add_annotation(x=4, y=0.5, text='Reta linear não separa',
                           font=dict(color=DRACULA['yellow'], size=13), showarrow=False)
fig_original.update_xaxes(title='x₁', range=[-6.5, 6.5])
fig_original.update_yaxes(title='x₂', range=[-6.5, 6.5])
fig_original.update_layout(width=680, height=580)
fig_original = apply_dracula(fig_original, 'Dados originais: círculos concêntricos não são linearmente separáveis')

# ============================================================
# 3. Figura: Transformação polinomial — agora é separável
# ============================================================
r2_normal = X_normal[:, 0]**2 + X_normal[:, 1]**2
r2_anom = X_anom[:, 0]**2 + X_anom[:, 1]**2

fig_transform = go.Figure()
fig_transform.add_trace(go.Scatter(
    x=X_normal[:, 0], y=r2_normal,
    mode='markers', name='Normal',
    marker=dict(color=DRACULA['cyan'], size=9, opacity=0.7),
))
fig_transform.add_trace(go.Scatter(
    x=X_anom[:, 0], y=r2_anom,
    mode='markers', name='Anomalia',
    marker=dict(color=DRACULA['red'], size=11, symbol='x', line=dict(width=2, color=DRACULA['red'])),
))
fig_transform.add_hline(y=10, line_color=DRACULA['green'], line_width=3)
fig_transform.add_annotation(x=4, y=11.5, text='Agora separável por uma reta!',
                           font=dict(color=DRACULA['green'], size=14), showarrow=False)
fig_transform.update_xaxes(title='x₁ (original)')
fig_transform.update_yaxes(title='r² = x₁² + x₂² (transformado)', range=[0, 35])
fig_transform.update_layout(width=680, height=580)
fig_transform = apply_dracula(fig_transform, 'Espaço transformado: distância ao centro torna os grupos separáveis')

# ============================================================
# 4. Figura: O truque do kernel (kernel trick)
# ============================================================
fig_kernel = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Cálculo direto (φ explícito)', 'Via kernel K(a,b) = (a·b)²'),
    horizontal_spacing=0.12
)

a = X_normal[0]
b_pt = X_normal[5]

phi = lambda v: np.array([v[0]**2, np.sqrt(2)*v[0]*v[1], v[1]**2])
phi_a = phi(a)
phi_b = phi(b_pt)
dot_direct = float(np.dot(phi_a, phi_b))
dot_kernel = float(np.dot(a, b_pt)**2)

categories = ['φ₁=a₁²', 'φ₂=√2·a₁a₂', 'φ₃=a₂²']
fig_kernel.add_trace(go.Bar(
    x=categories, y=phi_a, name='φ(a)', marker_color=DRACULA['cyan'], opacity=0.7
), row=1, col=1)
fig_kernel.add_trace(go.Bar(
    x=categories, y=phi_b, name='φ(b)', marker_color=DRACULA['pink'], opacity=0.7
), row=1, col=1)
fig_kernel.add_annotation(
    x=1, y=max(max(phi_a), max(phi_b))*1.15,
    text=f'φ(a)·φ(b) = {dot_direct:.2f}',
    showarrow=False, font=dict(color=DRACULA['fg'], size=13), row=1, col=1
)

cats2 = ['a₁', 'a₂', 'b₁', 'b₂']
vals2 = [a[0], a[1], b_pt[0], b_pt[1]]
colors2 = [DRACULA['cyan'], DRACULA['cyan'], DRACULA['pink'], DRACULA['pink']]
fig_kernel.add_trace(go.Bar(
    x=cats2, y=vals2, showlegend=False,
    marker_color=colors2, opacity=0.7
), row=1, col=2)
fig_kernel.add_annotation(
    x=1.5, y=max(vals2)*2.8,
    text=f'(a·b)² = {dot_kernel:.2f}',
    showarrow=False, font=dict(color=DRACULA['fg'], size=13), row=1, col=2
)
fig_kernel.add_annotation(
    x=1.5, y=max(vals2)*2.0,
    text='Mesmo resultado, menos operações!',
    showarrow=False, font=dict(color=DRACULA['green'], size=12), row=1, col=2
)

fig_kernel.update_layout(
    title_text='Kernel trick: evita calcular φ(x) explicitamente',
    paper_bgcolor=DRACULA['bg'], plot_bgcolor=DRACULA['bg'],
    font=dict(color=DRACULA['fg']),
    showlegend=True, legend=dict(orientation='h', y=-0.15),
    margin=dict(l=60, r=30, t=80, b=60),
)
fig_kernel.update_xaxes(gridcolor='#44475a')
fig_kernel.update_yaxes(gridcolor='#44475a')
fig_kernel.update_layout(width=900, height=420)

# ============================================================
# Helper: círculo paramétrico para fronteira
# ============================================================
def circle_trace(cx, cy, r, n=200):
    theta = np.linspace(0, 2*np.pi, n)
    return go.Scatter(
        x=cx + r*np.cos(theta), y=cy + r*np.sin(theta),
        mode='lines', line=dict(color=DRACULA['fg'], width=2, dash='dash'),
        name='Fronteira de decisão', hoverinfo='skip',
    )

# ============================================================
# 5. Figura: Support Vectors — pontos na fronteira
# ============================================================
# Selecionar os ~10 pontos normais mais distantes do centro = borda da região normal
raios_norm = np.sqrt(X_normal[:, 0]**2 + X_normal[:, 1]**2)
# Pegar os 10 com maior raio (mais próximos da fronteira)
n_sv = 10
sv_indices = np.argsort(raios_norm)[-n_sv:]

fig_svs = go.Figure()

# Normais que NÃO são SVs (opacidade baixa)
not_sv = np.setdiff1d(np.arange(n_normal), sv_indices)
fig_svs.add_trace(go.Scatter(
    x=X_normal[not_sv, 0], y=X_normal[not_sv, 1],
    mode='markers', name='Normal (α = 0)',
    marker=dict(color=DRACULA['cyan'], size=7, opacity=0.35),
))

# Anomalias
fig_svs.add_trace(go.Scatter(
    x=X_anom[:, 0], y=X_anom[:, 1],
    mode='markers', name='Anomalia',
    marker=dict(color=DRACULA['red'], size=10, symbol='x', line=dict(width=2, color=DRACULA['red'])),
))

# Fronteira de decisão (círculo em r=3.0)
fig_svs.add_trace(circle_trace(0, 0, 3.0))

# Support vectors: amarelos, pequenos, com borda escura
fig_svs.add_trace(go.Scatter(
    x=X_normal[sv_indices, 0], y=X_normal[sv_indices, 1],
    mode='markers', name='Support Vector (α > 0)',
    marker=dict(
        color=DRACULA['yellow'],
        size=10,
        line=dict(color=DRACULA['fg'], width=1.5)
    ),
))

fig_svs.update_xaxes(title='x₁', range=[-6.5, 6.5])
fig_svs.update_yaxes(title='x₂', range=[-6.5, 6.5])
fig_svs.update_layout(width=680, height=580)
fig_svs = apply_dracula(fig_svs, 'Support Vectors: pontos da borda definem o modelo')

# ============================================================
# 6. Figura: Classificando novos pontos
# ============================================================
fig_front = go.Figure()

# Fronteira de decisão (círculo em r=3.0)
fig_front.add_trace(circle_trace(0, 0, 3.0))

# Pontos normais
fig_front.add_trace(go.Scatter(
    x=X_normal[:, 0], y=X_normal[:, 1],
    mode='markers', name='Normal',
    marker=dict(color=DRACULA['cyan'], size=8, opacity=0.8),
))

# Anomalias
fig_front.add_trace(go.Scatter(
    x=X_anom[:, 0], y=X_anom[:, 1],
    mode='markers', name='Anomalia',
    marker=dict(color=DRACULA['red'], size=10, symbol='x', line=dict(width=2, color=DRACULA['red'])),
))

# Novo ponto normal (dentro do círculo)
fig_front.add_trace(go.Scatter(
    x=[1.5], y=[1.0], mode='markers+text',
    name='Novo ponto → Normal', text=['Novo ponto → Normal'],
    textposition='top center',
    marker=dict(color=DRACULA['green'], size=14, symbol='diamond',
                line=dict(color=DRACULA['fg'], width=1.5)),
    textfont=dict(color=DRACULA['green'], size=12),
))

# Novo ponto anômalo (fora do círculo)
fig_front.add_trace(go.Scatter(
    x=[4.0], y=[3.0], mode='markers+text',
    name='Novo ponto → Anomalia', text=['Novo ponto → Anomalia'],
    textposition='top center',
    marker=dict(color=DRACULA['red'], size=14, symbol='diamond',
                line=dict(color=DRACULA['fg'], width=1.5)),
    textfont=dict(color=DRACULA['red'], size=12),
))

fig_front.update_xaxes(title='x₁', range=[-6.5, 6.5])
fig_front.update_yaxes(title='x₂', range=[-6.5, 6.5])
fig_front.update_layout(width=680, height=580)
fig_front = apply_dracula(fig_front, 'Classificação: similaridade com SVs menos o limiar ρ')

# ============================================================
# 7. Exportar
# ============================================================
figures = {
    'AULA13_SVM_ORIGINAL': fig_original,
    'AULA13_SVM_TRANSFORMADO': fig_transform,
    'AULA13_SVM_KERNEL_TRICK': fig_kernel,
    'AULA13_SVM_SUPPORT_VECTORS': fig_svs,
    'AULA13_SVM_FRONTEIRA': fig_front,
}

write_plotly_js(figures, slide_export_path())
print(f"Exported {len(figures)} figures to {slide_export_path()}")
