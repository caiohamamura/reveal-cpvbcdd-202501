from datetime import datetime
import os
from pathlib import Path

import duckdb
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def assert_rows(query: str, expected: list[tuple], *, relation: duckdb.DuckDBPyConnection | None = None) -> None:
    con = relation or duckdb.connect()
    rows = con.execute(query).fetchall()
    if rows != expected:
        raise AssertionError(f"\nQuery:\n{query}\nEsperado: {expected}\nObtido:   {rows}")


def assert_rowset(query: str, expected: set[tuple], *, relation: duckdb.DuckDBPyConnection | None = None) -> None:
    con = relation or duckdb.connect()
    rows = set(con.execute(query).fetchall())
    if rows != expected:
        raise AssertionError(f"\nQuery:\n{query}\nEsperado: {expected}\nObtido:   {rows}")


def main() -> None:
    os.chdir(ROOT)

    df = pd.DataFrame(
        {
            "produto": ["Mouse", "Teclado", "Mouse", "Monitor"],
            "categoria": ["Periferico", "Periferico", "Periferico", "Video"],
            "valor": [50, 120, 70, 900],
        }
    )
    resultado = duckdb.sql(
        """
        SELECT produto, SUM(valor) AS total
        FROM df
        GROUP BY produto
        ORDER BY total DESC
        """
    ).fetchall()
    assert resultado == [("Monitor", 900), ("Mouse", 120), ("Teclado", 120)]

    assert_rows(
        """
        SELECT categoria, COUNT(*) AS qtd, SUM(valor) AS total
        FROM read_csv_auto('vendas.csv')
        GROUP BY categoria
        ORDER BY total DESC
        """,
        [
            ("Computador", 1, 3200.0),
            ("Video", 2, 1750.0),
            ("Periferico", 6, 615.0),
            ("Armazenamento", 1, 420.0),
            ("Acessorio", 2, 130.0),
        ],
    )

    assert_rows(
        """
        SELECT categoria, COUNT(*) AS qtd, SUM(valor) AS total
        FROM read_parquet('vendas.parquet')
        WHERE data >= DATE '2026-01-01'
        GROUP BY categoria
        ORDER BY total DESC
        """,
        [
            ("Computador", 1, 3200.0),
            ("Video", 2, 1750.0),
            ("Periferico", 6, 615.0),
            ("Armazenamento", 1, 420.0),
            ("Acessorio", 2, 130.0),
        ],
    )

    assert_rows(
        """
        SELECT cidade,
               DATE_TRUNC('month', data) AS mes,
               SUM(valor) AS total
        FROM read_parquet('dados/vendas/ano=2026/mes=*/vendas_*.parquet')
        WHERE categoria = 'Periferico'
        GROUP BY cidade, DATE_TRUNC('month', data)
        ORDER BY mes, total DESC
        """,
        [
            ("Elias Fausto", datetime(2026, 1, 1), 120.0),
            ("Capivari", datetime(2026, 1, 1), 50.0),
            ("Rafard", datetime(2026, 2, 1), 180.0),
            ("Capivari", datetime(2026, 2, 1), 70.0),
            ("Elias Fausto", datetime(2026, 3, 1), 130.0),
            ("Rafard", datetime(2026, 4, 1), 65.0),
        ],
    )

    assert_rows(
        """
        SELECT ano, mes, cidade, SUM(valor) AS total
        FROM read_parquet(
            'dados/vendas/ano=*/mes=*/*.parquet',
            hive_partitioning = true
        )
        WHERE ano = 2026
        GROUP BY ano, mes, cidade
        ORDER BY mes, total DESC
        """,
        [
            (2026, "01", "Rafard", 900.0),
            (2026, "01", "Elias Fausto", 120.0),
            (2026, "01", "Capivari", 50.0),
            (2026, "02", "Rafard", 180.0),
            (2026, "02", "Capivari", 105.0),
            (2026, "03", "Rafard", 850.0),
            (2026, "03", "Capivari", 420.0),
            (2026, "03", "Elias Fausto", 130.0),
            (2026, "04", "Capivari", 3200.0),
            (2026, "04", "Elias Fausto", 95.0),
            (2026, "04", "Rafard", 65.0),
        ],
    )

    assert_rows(
        """
        SELECT ano, mes, categoria, COUNT(*) AS qtd
        FROM read_csv(
            'dados/vendas_csv/ano=*/mes=*/*.csv',
            header = true,
            hive_partitioning = true
        )
        WHERE categoria = 'Periferico'
        GROUP BY ano, mes, categoria
        ORDER BY ano, mes
        """,
        [
            (2026, "01", "Periferico", 2),
            (2026, "02", "Periferico", 2),
            (2026, "03", "Periferico", 1),
            (2026, "04", "Periferico", 1),
        ],
    )

    con = duckdb.connect()
    con.execute(
        """
        CREATE OR REPLACE TABLE vendas AS
        SELECT *
        FROM read_csv_auto('vendas.csv')
        """
    )
    colunas = [row[0] for row in con.execute("DESCRIBE vendas").fetchall()]
    assert colunas == ["data", "produto", "categoria", "cidade", "valor"]
    assert_rows("SELECT COUNT(*) AS total_linhas FROM vendas", [(12,)], relation=con)
    assert con.execute("SELECT * FROM vendas LIMIT 10").fetchall()
    assert_rows(
        """
        SELECT categoria, AVG(valor) AS media, SUM(valor) AS total
        FROM vendas
        GROUP BY categoria
        ORDER BY total DESC
        """,
        [
            ("Computador", 3200.0, 3200.0),
            ("Video", 875.0, 1750.0),
            ("Periferico", 102.5, 615.0),
            ("Armazenamento", 420.0, 420.0),
            ("Acessorio", 65.0, 130.0),
        ],
        relation=con,
    )
    assert_rowset(
        """
        SELECT produto, COUNT(*) AS quantidade
        FROM vendas
        GROUP BY produto
        ORDER BY quantidade DESC
        """,
        {
            ("Mouse", 3),
            ("Monitor", 2),
            ("Teclado", 2),
            ("Cabo HDMI", 1),
            ("Notebook", 1),
            ("Hub USB", 1),
            ("Webcam", 1),
            ("SSD 1TB", 1),
        },
        relation=con,
    )
    assert_rows(
        """
        SELECT
            DATE_TRUNC('month', data) AS mes,
            SUM(valor) AS total
        FROM vendas
        GROUP BY mes
        ORDER BY mes
        """,
        [
            (datetime(2026, 1, 1), 1070.0),
            (datetime(2026, 2, 1), 285.0),
            (datetime(2026, 3, 1), 1400.0),
            (datetime(2026, 4, 1), 3360.0),
        ],
        relation=con,
    )
    assert_rows("SELECT COUNT(*) AS total_linhas FROM vendas", [(12,)], relation=con)
    assert_rowset(
        """
        SELECT categoria, COUNT(*) AS qtd
        FROM vendas
        GROUP BY categoria
        ORDER BY qtd DESC
        """,
        {
            ("Periferico", 6),
            ("Video", 2),
            ("Acessorio", 2),
            ("Computador", 1),
            ("Armazenamento", 1),
        },
        relation=con,
    )
    assert_rows(
        """
        SELECT cidade, AVG(valor) AS media
        FROM vendas
        GROUP BY cidade
        HAVING COUNT(*) >= 2
        ORDER BY media DESC
        """,
        [("Capivari", 755.0), ("Rafard", 498.75), ("Elias Fausto", 115.0)],
        relation=con,
    )

    con.execute(
        """
        COPY (
            SELECT categoria, SUM(valor) AS total
            FROM vendas
            GROUP BY categoria
        ) TO 'resumo_categorias.csv' (HEADER, DELIMITER ',')
        """
    )
    con.execute(
        """
        COPY (
            SELECT categoria, SUM(valor) AS total
            FROM vendas
            GROUP BY categoria
        ) TO 'resumo_categorias.parquet' (FORMAT PARQUET)
        """
    )
    con.execute(
        """
        CREATE OR REPLACE TABLE vendas_limpas AS
        SELECT
            CAST(data AS DATE) AS data,
            cidade,
            categoria,
            produto,
            CAST(valor AS DECIMAL(10, 2)) AS valor
        FROM read_csv_auto('entrada/vendas_*.csv')
        WHERE valor IS NOT NULL
          AND data >= DATE '2026-01-01'
        """
    )
    (ROOT / "saida").mkdir(exist_ok=True)
    con.execute("COPY vendas_limpas TO 'saida/vendas_limpas.parquet' (FORMAT PARQUET)")
    assert (ROOT / "resumo_categorias.csv").exists()
    assert (ROOT / "resumo_categorias.parquet").exists()
    assert (ROOT / "saida" / "vendas_limpas.parquet").exists()
    con.close()

    print("OK: exemplos DuckDB/CSV/Parquet/Hive da aula 15 executados com sucesso.")


if __name__ == "__main__":
    main()
