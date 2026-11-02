"""Extrai dos zips da Receita só as colunas que a limpeza usa, para todo o Brasil, em dois Parquets.

Substitui a varredura dos zips (6,4 GB) a cada ano. Uso: .venv/bin/python -I codigo/origem_dos_dados/extrair_receita.py
"""

import os
import subprocess
from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parents[2]
RECEITA = RAIZ / "dados/brutos/receita"
LIMPOS = RAIZ / "dados/limpos"
(LIMPOS / "tmp").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()
con.execute(f"SET memory_limit='1500MB'; SET temp_directory='{LIMPOS / 'tmp'}'; SET preserve_insertion_order=false")


def tabela_auxiliar(zip_):
    texto = subprocess.run(["unzip", "-p", str(RECEITA / zip_)], capture_output=True, check=True).stdout.decode("latin-1")
    return [tuple(c.strip('"') for c in linha.split('";"')) for linha in texto.splitlines() if linha.strip()]


def extrair(prefixo, n_colunas, select, destino, depois=""):
    # Os CSVs não têm cabeçalho; o unzip concatena os dez arquivos num só fluxo. O iconv passa para UTF-8 porque o
    # leitor latin-1 do DuckDB recusa os bytes 0x80-0x9F que aparecem em nomes.
    zips = sorted(str(z) for z in RECEITA.glob(f"{prefixo}[0-9].zip"))
    assert len(zips) == 10, zips
    fifo = LIMPOS / "tmp" / f"{prefixo}.fifo"
    fifo.unlink(missing_ok=True)
    os.mkfifo(fifo)
    with open(LIMPOS / "tmp" / f"{prefixo}.unzip.log", "w") as log:
        proc = subprocess.Popen(f"set -o pipefail; for z in {' '.join(zips)}; do unzip -p \"$z\" || exit 1; done | iconv -f latin1 -t utf-8 > '{fifo}'", shell=True, executable="/bin/bash", stderr=log)
        nomes = ", ".join(f"'c{i}': 'VARCHAR'" for i in range(n_colunas))
        con.execute(f"""COPY (SELECT {select} FROM read_csv('{fifo}', delim=';', quote='"', escape='"', header=false,
                          columns={{{nomes}}}) {depois})
                     TO '{destino}' (FORMAT parquet, COMPRESSION zstd)""")
        if proc.wait():
            raise RuntimeError(f"unzip falhou em {prefixo}")
    fifo.unlink()


# Uma raiz (08314885) vem duas vezes, uma com natureza 0000 (inexistente); fica a linha com natureza válida.
extrair("Empresas", 7, "c0 AS cnpj_basico, c2 AS natureza_juridica, c5 AS porte", LIMPOS / "receita_empresas.parquet",
        "QUALIFY row_number() OVER (PARTITION BY c0 ORDER BY c2 = '0000', c2, c5) = 1")
extrair("Estabelecimentos", 30, "c0 || c1 || c2 AS cnpj, c5 AS situacao_cadastral, c10 AS data_inicio_atividade, c11 AS cnae_principal",
        LIMPOS / "receita_estabelecimentos.parquet")

naturezas = tabela_auxiliar("Naturezas.zip")
cnaes = tabela_auxiliar("Cnaes.zip")
con.execute("CREATE TABLE n (codigo VARCHAR, descricao VARCHAR); CREATE TABLE c (codigo VARCHAR, descricao VARCHAR)")
con.executemany("INSERT INTO n VALUES (?, ?)", naturezas)
con.executemany("INSERT INTO c VALUES (?, ?)", cnaes)
con.execute(f"COPY n TO '{LIMPOS / 'receita_naturezas.parquet'}' (FORMAT parquet)")
con.execute(f"COPY c TO '{LIMPOS / 'receita_cnaes.parquet'}' (FORMAT parquet)")

chaves = {"receita_empresas": "cnpj_basico", "receita_estabelecimentos": "cnpj", "receita_naturezas": "codigo", "receita_cnaes": "codigo"}
for nome, chave in chaves.items():
    linhas, distintas = con.execute(f"SELECT count(*), count(DISTINCT {chave}) FROM '{LIMPOS / nome}.parquet'").fetchall()[0]
    print(f"{nome}: {linhas} linhas, {distintas} chaves distintas")
