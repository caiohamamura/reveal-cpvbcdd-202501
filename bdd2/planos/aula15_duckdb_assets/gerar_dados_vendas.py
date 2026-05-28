from pathlib import Path

import duckdb
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


vendas = pd.DataFrame(
    [
        ("2026-01-05", "Mouse", "Periferico", "Capivari", 50.00),
        ("2026-01-12", "Teclado", "Periferico", "Elias Fausto", 120.00),
        ("2026-01-20", "Monitor", "Video", "Rafard", 900.00),
        ("2026-02-03", "Mouse", "Periferico", "Capivari", 70.00),
        ("2026-02-10", "Webcam", "Periferico", "Rafard", 180.00),
        ("2026-02-18", "Cabo HDMI", "Acessorio", "Capivari", 35.00),
        ("2026-03-02", "Monitor", "Video", "Rafard", 850.00),
        ("2026-03-08", "SSD 1TB", "Armazenamento", "Capivari", 420.00),
        ("2026-03-20", "Teclado", "Periferico", "Elias Fausto", 130.00),
        ("2026-04-04", "Notebook", "Computador", "Capivari", 3200.00),
        ("2026-04-12", "Mouse", "Periferico", "Rafard", 65.00),
        ("2026-04-22", "Hub USB", "Acessorio", "Elias Fausto", 95.00),
    ],
    columns=["data", "produto", "categoria", "cidade", "valor"],
)
vendas["data"] = pd.to_datetime(vendas["data"])
vendas["ano"] = vendas["data"].dt.year
vendas["mes"] = vendas["data"].dt.month.map(lambda mes: f"{mes:02d}")


def main() -> None:
    (ROOT / "dados").mkdir(exist_ok=True)
    (ROOT / "saida").mkdir(exist_ok=True)
    vendas.drop(columns=["ano", "mes"]).to_csv(ROOT / "vendas.csv", index=False)

    con = duckdb.connect()
    con.register("vendas_df", vendas.drop(columns=["ano", "mes"]))
    con.sql(f"""
        COPY vendas_df
        TO '{ROOT / "vendas.parquet"}'
        (FORMAT PARQUET)
    """)

    for (ano, mes), particao in vendas.groupby(["ano", "mes"]):
        parquet_dir = ROOT / "dados" / "vendas" / f"ano={ano}" / f"mes={mes}"
        csv_dir = ROOT / "dados" / "vendas_csv" / f"ano={ano}" / f"mes={mes}"
        parquet_dir.mkdir(parents=True, exist_ok=True)
        csv_dir.mkdir(parents=True, exist_ok=True)

        particao_sem_particoes = particao.drop(columns=["ano", "mes"])
        particao_sem_particoes.to_csv(csv_dir / f"vendas_{mes}.csv", index=False)
        con.register("particao_df", particao_sem_particoes)
        con.sql(f"""
            COPY particao_df
            TO '{parquet_dir / f"vendas_{mes}.parquet"}'
            (FORMAT PARQUET)
        """)

    entrada = ROOT / "entrada"
    entrada.mkdir(exist_ok=True)
    vendas.drop(columns=["ano", "mes"]).to_csv(entrada / "vendas_2026.csv", index=False)


if __name__ == "__main__":
    main()
