"""Hash do conteúdo de Parquets, independente da ordem das linhas (o DuckDB grava em paralelo).

Uso: .venv/bin/python -I codigo/hash_conteudo.py dados/limpos/empenhos_2013.parquet ...
"""

import sys

import duckdb

duckdb.sql("SET enable_progress_bar = false")
for caminho in sys.argv[1:]:
    linhas, soma = duckdb.execute("SELECT count(*), sum(hash(x)::HUGEINT) FROM read_parquet(?) x", [caminho]).fetchall()[0]
    print(f"{linhas}\t{soma}\t{caminho}")
