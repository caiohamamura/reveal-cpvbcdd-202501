from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from statsmodels.tsa.seasonal import seasonal_decompose


DATA_DIR = Path(__file__).resolve().parents[1] / "dados" / "aula14"


def titulo(texto):
    print("\n" + "=" * 72)
    print(texto)
    print("=" * 72)


def aula14_dados_inspecao():
    df = pd.read_csv(DATA_DIR / "dados.csv")

    titulo("Resultado da inspeção")
    print(f"df.shape -> {df.shape}\n")
    print("df.head(3)")
    print(df.head(3).to_string(index=False))

    numericas = df.describe().T[["mean", "std", "min", "max"]]
    print("\ndescribe numerico")
    print(numericas.round(2).to_string())

    faltantes = df.isna().mean().sort_values(ascending=False)
    alvo_classes = df["evadiu"].nunique()
    print(
        "\nfaltantes: "
        f"frequencia = {faltantes['frequencia']:.1%}".replace(".", ",")
        + f"; alvo: evadiu tem {alvo_classes} classes"
    )


def aula14_serie_temporal():
    df = pd.read_csv(DATA_DIR / "emprestimos.csv", parse_dates=["semana"])
    serie = df.set_index("semana")["emprestimos"]
    media_movel = serie.rolling(4).mean()

    titulo("Resultado da série temporal")
    print("serie.tail(6)")
    print(serie.tail(6))
    print("\nmedia_movel.tail(6)")
    print(media_movel.tail(6).round(1))

    decomp = seasonal_decompose(serie, model="additive", period=4)
    ultimas = serie.tail(4)
    passo = (ultimas.iloc[-1] - ultimas.iloc[0]) / 3
    forecast = [serie.iloc[-1] + passo * i for i in range(1, 5)]
    forecast_index = pd.date_range(serie.index[-1] + pd.Timedelta(days=7), periods=4, freq="7D")
    forecast_simples = pd.Series(forecast, index=forecast_index, name="forecast")

    tendencia = decomp.trend.dropna()
    sazonal = decomp.seasonal.iloc[:4]

    titulo("Resultado da decomposição e forecast")
    print("decomp.trend.dropna().tail(6).round(1)")
    print(tendencia.tail(6).round(1))
    print("\ndecomp.seasonal.head(4).round(1).to_numpy()")
    print(np.round(sazonal.to_numpy(), 1))
    print("\nforecast_simples.round().astype(int)")
    print(forecast_simples.round().astype(int))


def aula14_texto_clusters():
    df = pd.read_csv(DATA_DIR / "respostas.csv")
    textos = df["resposta_aberta"].fillna("")

    vetor = TfidfVectorizer(
        lowercase=True,
        stop_words=["de", "da", "do", "e", "a", "o", "para"],
    )
    X = vetor.fit_transform(textos)

    clusters = KMeans(n_clusters=4, random_state=42, n_init="auto").fit_predict(X)
    coords = TruncatedSVD(n_components=2, random_state=42).fit_transform(X)

    df["cluster"] = clusters.astype(str)
    df["x"] = coords[:, 0]
    df["y"] = coords[:, 1]

    titulo("Resultado do TF-IDF + clusters")
    print(f"matriz TF-IDF -> {X.shape}")
    print(f"respostas por cluster -> {df['cluster'].value_counts().sort_index().to_dict()}\n")
    print('df[["cluster", "x", "y"]].head(6)')
    print(df[["cluster", "x", "y"]].head(6).round(3).to_string(index=False))

    titulo("Saída dos termos fortes")
    termos = vetor.get_feature_names_out()
    for cluster_id in sorted(df["cluster"].unique()):
        linhas = (df["cluster"] == cluster_id).to_numpy()
        media_tfidf = X[linhas].mean(axis=0).A1
        top = np.argsort(media_tfidf)[-5:][::-1]
        palavras = ", ".join(termos[i] for i in top)
        print(cluster_id, palavras)


def aula14_questionario():
    df = pd.read_csv(DATA_DIR / "questionario.csv")
    itens = ["q1_satisfacao", "q2_apoio", "q3_estrutura", "q4_clareza"]

    resumo = df[itens].agg(["mean", "median", "std"]).T
    por_curso = df.groupby("curso")[itens].mean()

    df["indice_experiencia"] = df[itens].mean(axis=1)
    indice = df.groupby("curso")["indice_experiencia"].agg(["mean", "min", "max"])

    titulo("Resultado do questionário")
    print("resumo")
    print(resumo.round(2).to_string())
    print("\nmedias por curso")
    print(por_curso.round(2).to_string())
    print("\nindice_experiencia por curso")
    for curso, linha in indice.round(2).iterrows():
        print(f"{curso:<4} mean {linha['mean']:.2f}  min {linha['min']:.2f}  max {linha['max']:.2f}")


if __name__ == "__main__":
    aula14_dados_inspecao()
    aula14_serie_temporal()
    aula14_texto_clusters()
    aula14_questionario()
