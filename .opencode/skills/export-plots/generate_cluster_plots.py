#!/usr/bin/env python3
"""
Generate all Dracula-themed plots for the Cluster Analysis lecture (Aula 12).

Prerequisites:
    pip install pandas matplotlib seaborn scikit-learn scipy

Output: PNG files in ciencia-dados/images/
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Add the export-plots script path so we can use apply_dracula_theme
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_plots import apply_dracula_theme, DRACULA, DEFAULT_PALETTE

apply_dracula_theme()


_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
OUTPUT_DIR = os.path.join(_REPO_ROOT, "ciencia-dados", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PAL = DEFAULT_PALETTE
N_CLUSTERS = 5


def load_and_preprocess():
    """Load and preprocess the marketing campaign dataset."""
    print("Loading data...")
    dados = pd.read_csv(
        'https://gist.githubusercontent.com/caiohamamura/56e2ac1e37ddc1885dc31055a794c272/raw/42ca58d73e9b9634ca9a660429d7be837354bb97/marketing_campaign.csv',
        sep='\t'
    )

    # Convert date
    dados['Dt_Customer'] = pd.to_datetime(dados['Dt_Customer'], dayfirst=True)

    # Map categoricals
    dados["Marital_Status"] = dados["Marital_Status"].map({
        'Married': 'Together', 'Divorced': 'Single', 'Widow': 'Single',
        'Alone': 'Single', 'Absurd': 'Single', 'YOLO': 'Single',
        'Together': 'Together', 'Single': 'Single'
    })
    dados["Education"] = dados["Education"].map({
        'Basic': 'Basic', '2nd Cycle': 'Basic',
        'Graduation': 'Graduated', 'Master': 'Graduated', 'PhD': 'Graduated'
    })

    # Encode categoricals
    for categoria in ['Education', 'Marital_Status']:
        dados[categoria] = dados[categoria].astype('category')
        dados[categoria] = dados[categoria].cat.codes

    # Drop NAs
    dados = dados.dropna()

    # Feature engineering
    dados['Idade'] = 2014 - dados['Year_Birth']
    dados['Tempo_cliente'] = (pd.to_datetime('2015-01-01') - dados["Dt_Customer"]).dt.days.astype('int32')

    colunas_mnt = [c for c in dados.columns if c.startswith("Mnt")]
    dados["Gasto_total"] = dados[colunas_mnt].sum(axis=1)

    dados['Filhos'] = dados['Kidhome'] + dados['Teenhome']
    dados["Tamanho_familia"] = dados["Filhos"] + dados['Marital_Status'].replace({0: 1, 1: 2})
    dados["Tem_filhos"] = (dados["Filhos"] > 0).astype(int)

    # Remove outliers
    dados = dados[dados["Income"] < 600000]
    dados = dados[dados["Idade"] < 90]

    # Drop redundant columns
    dados = dados.drop(['Z_Revenue', 'Z_CostContact', 'Dt_Customer', 'Year_Birth', 'ID'], axis=1, errors='ignore')

    # Separate response columns
    colunas_resposta = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3',
                        'AcceptedCmp4', 'AcceptedCmp5', 'Response', 'Complain']
    dados_perfil_raw = dados.drop(colunas_resposta, axis=1)

    # Standardize
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    dados_perfil = pd.DataFrame(
        scaler.fit_transform(dados_perfil_raw),
        columns=dados_perfil_raw.columns
    )

    return dados, dados_perfil


def plot_elbow_method(dados_perfil):
    """Generate the elbow method plot."""
    print("Generating elbow method plot...")

    from sklearn.cluster import AgglomerativeClustering

    max_clusters = 15
    variancia_interna_media = np.zeros(max_clusters)

    for ii in range(1, max_clusters + 1):
        cluster = AgglomerativeClustering(n_clusters=ii, linkage='ward')
        cluster.fit(dados_perfil)
        labels = cluster.labels_

        internal_var_mean = 0
        for label in np.unique(labels):
            internal_var = np.var(dados_perfil.values[labels == label], axis=0).mean()
            if not np.isnan(internal_var):
                internal_var_mean += internal_var / ii
        variancia_interna_media[ii - 1] = internal_var_mean

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(1, max_clusters + 1), variancia_interna_media, marker='o',
            color=DRACULA["purple"], markersize=8, linewidth=2.5)
    ax.set_xticks(range(1, max_clusters + 1))
    ax.set_title('Método do Cotovelo — Número Ótimo de Clusters', fontsize=16,
                 color=DRACULA["foreground"], pad=15)
    ax.set_xlabel('Número de Clusters', fontsize=13, color=DRACULA["foreground"])
    ax.set_ylabel('Variância Média Interna', fontsize=13, color=DRACULA["foreground"])
    ax.grid(True, alpha=0.3, color=DRACULA["current_line"])

    # Highlight N_CLUSTERS
    ax.axvline(x=N_CLUSTERS, color=DRACULA["pink"], linestyle='--', linewidth=2, alpha=0.7)
    ax.text(N_CLUSTERS + 0.2, variancia_interna_media[N_CLUSTERS - 1],
            f'k = {N_CLUSTERS}', color=DRACULA["pink"], fontsize=12, fontweight='bold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    path = os.path.join(OUTPUT_DIR, "cotovelo.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=DRACULA["background"], edgecolor='none')
    plt.close(fig)
    print(f"  -> {path} ({os.path.getsize(path)} bytes)")


def plot_scatter_clusters(dados):
    """Generate scatter plot: Gasto_total vs Income colored by cluster."""
    print("Generating scatter cluster plot...")
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.scatterplot(data=dados, x='Gasto_total', y='Income', hue='cluster',
                    palette=PAL[:dados['cluster'].nunique()], ax=ax, alpha=0.7, s=40)

    ax.set_title('Renda vs Gasto Total por Cluster', fontsize=16,
                 color=DRACULA["foreground"], pad=15)
    ax.set_xlabel('Gasto Total (2 anos)', fontsize=13, color=DRACULA["foreground"])
    ax.set_ylabel('Renda Anual', fontsize=13, color=DRACULA["foreground"])
    ax.legend(title='Cluster', loc='upper left')
    ax.grid(True, alpha=0.3, color=DRACULA["current_line"])

    path = os.path.join(OUTPUT_DIR, "scatter-gasto-income.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=DRACULA["background"], edgecolor='none')
    plt.close(fig)
    print(f"  -> {path} ({os.path.getsize(path)} bytes)")


def plot_boxplots(dados):
    """Generate boxplot comparison of key metrics by cluster."""
    print("Generating boxplot comparisons...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    import seaborn as sns

    metrics = [
        ('NumDealsPurchases', 'Compras em Oferta'),
        ('NumWebVisitsMonth', 'Visitas ao Site (mês)'),
        ('NumWebPurchases', 'Compras pela Web'),
        ('Gasto_total', 'Gasto Total'),
    ]

    for ax, (col, title) in zip(axes.flat, metrics):
        sns.boxplot(data=dados, x='cluster', y=col, hue='cluster',
                    palette=PAL[:dados['cluster'].nunique()], ax=ax, legend=False)
        ax.set_title(title, fontsize=13, color=DRACULA["foreground"])
        ax.set_xlabel('Cluster', color=DRACULA["foreground"])
        ax.set_ylabel(col, color=DRACULA["foreground"])
        ax.grid(True, alpha=0.3, color=DRACULA["current_line"])

    fig.suptitle('Perfis de Consumo por Cluster', fontsize=16,
                 color=DRACULA["foreground"], y=1.01)
    fig.tight_layout()

    path = os.path.join(OUTPUT_DIR, "boxplot-consumo.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=DRACULA["background"], edgecolor='none')
    plt.close(fig)
    print(f"  -> {path} ({os.path.getsize(path)} bytes)")


def plot_kmeans_inertia(dados_perfil):
    """Generate K-Means inertia vs K plot."""
    print("Generating K-Means inertia plot...")

    from sklearn.cluster import KMeans

    max_k = 12
    inertias = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(dados_perfil)
        inertias.append(kmeans.inertia_)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(1, max_k + 1), inertias, marker='o',
            color=DRACULA["green"], markersize=8, linewidth=2.5)
    ax.set_xticks(range(1, max_k + 1))
    ax.set_title('K-Means — Inércia vs Número de Clusters', fontsize=16,
                 color=DRACULA["foreground"], pad=15)
    ax.set_xlabel('Número de Clusters (K)', fontsize=13, color=DRACULA["foreground"])
    ax.set_ylabel('Inércia (soma dos quadrados)', fontsize=13, color=DRACULA["foreground"])
    ax.grid(True, alpha=0.3, color=DRACULA["current_line"])

    # Highlight the elbow
    ax.axvline(x=N_CLUSTERS, color=DRACULA["pink"], linestyle='--', linewidth=2, alpha=0.7)
    ax.text(N_CLUSTERS + 0.2, inertias[N_CLUSTERS - 1],
            f'K = {N_CLUSTERS}', color=DRACULA["pink"], fontsize=12, fontweight='bold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    path = os.path.join(OUTPUT_DIR, "kmeans-inertia.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=DRACULA["background"], edgecolor='none')
    plt.close(fig)
    print(f"  -> {path} ({os.path.getsize(path)} bytes)")


def plot_dbscan_demo():
    """Generate a DBSCAN demonstration plot with sample 2D data."""
    print("Generating DBSCAN demo plot...")

    from sklearn.cluster import DBSCAN
    from sklearn.datasets import make_moons

    X, y_true = make_moons(n_samples=300, noise=0.08, random_state=42)

    dbscan = DBSCAN(eps=0.15, min_samples=5)
    labels = dbscan.fit_predict(X)

    unique_labels = set(labels)
    n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
    n_noise = list(labels).count(-1)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Original data
    axes[0].scatter(X[:, 0], X[:, 1], c=DRACULA["comment"], s=25, alpha=0.7)
    axes[0].set_title('Dados Originais (duas luas)', fontsize=14, color=DRACULA["foreground"])
    axes[0].set_xlabel('Feature 1', color=DRACULA["foreground"])
    axes[0].set_ylabel('Feature 2', color=DRACULA["foreground"])

    # DBSCAN result
    colors = [DRACULA["purple"], DRACULA["green"], DRACULA["cyan"], DRACULA["pink"],
              DRACULA["orange"], DRACULA["yellow"], DRACULA["red"]]
    for i, label in enumerate(sorted(unique_labels)):
        if label == -1:
            c = DRACULA["red"]
            mark = 'x'
        else:
            c = colors[i % len(colors)]
            mark = 'o'
        mask = labels == label
        axes[1].scatter(X[mask, 0], X[mask, 1], c=c, marker=mark, s=25,
                        alpha=0.8, label=f'Cluster {label}' if label != -1 else f'Ruído ({n_noise})')

    axes[1].set_title(f'DBSCAN (ε=0.15, {n_clusters} clusters, {n_noise} outliers)',
                      fontsize=14, color=DRACULA["foreground"])
    axes[1].set_xlabel('Feature 1', color=DRACULA["foreground"])
    axes[1].set_ylabel('Feature 2', color=DRACULA["foreground"])
    axes[1].legend(fontsize=10)

    for ax in axes:
        ax.set_facecolor(DRACULA["background"])
        ax.grid(True, alpha=0.3, color=DRACULA["current_line"])
        ax.set_xticklabels([])
        ax.set_yticklabels([])

    path = os.path.join(OUTPUT_DIR, "dbscan-demo.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=DRACULA["background"], edgecolor='none')
    plt.close(fig)
    print(f"  -> {path} ({os.path.getsize(path)} bytes)")


def plot_kmeans_2d_comparison(dados_perfil, dados):
    """Generate a 2D PCA projection colored by Hierarchical vs KMeans labels."""
    print("Generating K-Means vs Hierarchical comparison...")
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans, AgglomerativeClustering

    # KMeans
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    kmeans_labels = kmeans.fit_predict(dados_perfil)

    # Hierarchical
    hier = AgglomerativeClustering(n_clusters=N_CLUSTERS, linkage='ward')
    hier_labels = hier.fit_predict(dados_perfil)

    # PCA for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(dados_perfil)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # K-Means
    ax = axes[0]
    for i in range(N_CLUSTERS):
        mask = kmeans_labels == i
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], c=PAL[i], s=15, alpha=0.6, label=f'Grupo {i}')
    ax.set_title('K-Means (K = 5)', fontsize=14, color=DRACULA["foreground"])
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})', color=DRACULA["foreground"])
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})', color=DRACULA["foreground"])
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, alpha=0.3, color=DRACULA["current_line"])

    # Hierarchical
    ax = axes[1]
    for i in range(N_CLUSTERS):
        mask = hier_labels == i
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], c=PAL[i], s=15, alpha=0.6, label=f'Grupo {i}')
    ax.set_title('Hierárquico (Ward, 5 clusters)', fontsize=14, color=DRACULA["foreground"])
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})', color=DRACULA["foreground"])
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})', color=DRACULA["foreground"])
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, alpha=0.3, color=DRACULA["current_line"])

    fig.suptitle('Comparação: K-Means vs Cluster Hierárquico (PCA 2D)',
                 fontsize=15, color=DRACULA["foreground"], y=1.01)
    fig.tight_layout()

    path = os.path.join(OUTPUT_DIR, "kmeans-hierarchical-comparison.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=DRACULA["background"], edgecolor='none')
    plt.close(fig)
    print(f"  -> {path} ({os.path.getsize(path)} bytes)")


def plot_dendrogram(dados_perfil):
    """Generate a dendrogram from hierarchical clustering."""
    print("Generating dendrogram...")

    from sklearn.cluster import AgglomerativeClustering
    from scipy.cluster.hierarchy import dendrogram, linkage

    cluster = AgglomerativeClustering(n_clusters=N_CLUSTERS, linkage='ward')
    cluster.fit(dados_perfil)

    linked = linkage(cluster.children_, 'ward')

    fig, ax = plt.subplots(figsize=(12, 7))
    dendrogram(linked, no_labels=True, color_threshold=0, ax=ax,
               above_threshold_color=DRACULA["comment"])

    ax.set_title('Dendrograma — Cluster Hierárquico (Ward)', fontsize=16,
                 color=DRACULA["foreground"], pad=15)
    ax.set_xlabel('Amostras', fontsize=13, color=DRACULA["foreground"])
    ax.set_ylabel('Distância', fontsize=13, color=DRACULA["foreground"])
    ax.set_facecolor(DRACULA["background"])

    path = os.path.join(OUTPUT_DIR, "dendrograma.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=DRACULA["background"], edgecolor='none')
    plt.close(fig)
    print(f"  -> {path} ({os.path.getsize(path)} bytes)")


def main():
    print("=" * 60)
    print("Generating cluster analysis plots (Dracula theme)")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)

    # Load and preprocess data
    dados, dados_perfil = load_and_preprocess()

    # Run hierarchical clustering for the main analysis
    from sklearn.cluster import AgglomerativeClustering
    cluster = AgglomerativeClustering(n_clusters=N_CLUSTERS, linkage='ward')
    cluster.fit(dados_perfil)
    dados['cluster'] = cluster.labels_
    dados['Total_Promos'] = (dados['AcceptedCmp1'] + dados.get('AcceptedCmp2', 0) +
                             dados.get('AcceptedCmp3', 0) + dados.get('AcceptedCmp4', 0) +
                             dados.get('AcceptedCmp5', 0))

    # Generate all plots
    print(f"\nUsing {N_CLUSTERS} clusters\n")

    plot_elbow_method(dados_perfil)
    plot_dendrogram(dados_perfil)
    plot_scatter_clusters(dados)
    plot_boxplots(dados)
    plot_kmeans_inertia(dados_perfil)
    plot_kmeans_2d_comparison(dados_perfil, dados)
    plot_dbscan_demo()

    print("\n" + "=" * 60)
    print("All plots generated successfully!")
    print("=" * 60)

    # Run validation
    from export_plots import check_images
    images = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')])
    print(f"\nValidating {len(images)} images...")
    check_images([os.path.join(OUTPUT_DIR, img) for img in images])


if __name__ == "__main__":
    main()
