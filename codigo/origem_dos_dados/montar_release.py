"""Monta o zip de dados da release a partir dos Parquets da cadeia completa.

Uso: python -I codigo/origem_dos_dados/montar_release.py RAIZ_COM_DADOS SAIDA.zip
RAIZ_COM_DADOS é a pasta que contém dados/limpos e dados/brutos, gerados pela cadeia completa.

Leva só o que a reprodução lê e tira o que é dado pessoal e não entra em nenhuma conta: CPF no nome de
empresário individual (vira ***), título eleitoral dos prefeitos, e do TSE só as linhas e colunas de prefeito usadas.
Falha se sobrar uma sequência de 11 ou 12 dígitos em qualquer coluna de texto.
"""
import csv
import hashlib
import io
import re
import sys
import tempfile
import zipfile
from pathlib import Path

import duckdb

ANOS = range(2009, 2025)
COLUNAS_TSE = ['DT_ELEICAO', 'NM_TIPO_ELEICAO', 'NM_UE', 'DS_CARGO', 'DS_SIT_TOT_TURNO', 'DS_DETALHE_SITUACAO_CAND',
    'ST_REELEICAO']
# CPF (11), título eleitoral (12) ou CPF com pontuação, isolados de outros dígitos.
DOCUMENTO = r'(^|[^0-9])([0-9]{11,12}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2})([^0-9]|$)'
DATA_FIXA = (2026, 11, 2, 0, 0, 0)


def mascarar(coluna):
    # Duas passadas: uma sequência colada à anterior só casa depois que a primeira vira ***.
    uma = f"regexp_replace({coluna}, '{DOCUMENTO}', '\\1***\\3', 'g')"
    return f"regexp_replace({uma}, '{DOCUMENTO}', '\\1***\\3', 'g')"


def main():
    raiz, destino = Path(sys.argv[1]), Path(sys.argv[2])
    limpos, brutos = raiz / 'dados/limpos', raiz / 'dados/brutos'
    con = duckdb.connect()
    con.execute("SET threads=1; SET enable_progress_bar=false")
    tmp = Path(tempfile.mkdtemp())
    arquivos = {}  # caminho dentro do zip -> arquivo local

    for ano in ANOS:
        nome = f'rede_{ano}.parquet'
        con.execute(f"""COPY (SELECT * REPLACE ({mascarar('fornecedor')} AS fornecedor)
            FROM '{limpos / nome}' ORDER BY codigo_ibge, cnpj) TO '{tmp / nome}'""")
        arquivos[f'dados/limpos/{nome}'] = tmp / nome
    for nome in ['arestas_mandato', 'permanencia', 'transicoes']:
        arquivos[f'dados/limpos/{nome}.parquet'] = limpos / f'{nome}.parquet'
    con.execute(f"""COPY (SELECT * EXCLUDE (titulo_inicio, titulo_fim) FROM '{limpos / 'mandatos.parquet'}'
        ORDER BY codigo_ibge, eleicao) TO '{tmp / 'mandatos.parquet'}'""")
    arquivos['dados/limpos/mandatos.parquet'] = tmp / 'mandatos.parquet'
    redes = [str(limpos / f'rede_{a}.parquet') for a in ANOS]
    con.execute(f"""COPY (SELECT * FROM '{limpos / 'receita_empresas.parquet'}'
        WHERE cnpj_basico IN (SELECT DISTINCT left(cnpj, 8) FROM read_parquet({redes}))
        ORDER BY cnpj_basico) TO '{tmp / 'receita_empresas.parquet'}'""")
    arquivos['dados/limpos/receita_empresas.parquet'] = tmp / 'receita_empresas.parquet'

    for ano in (2008, 2012, 2016, 2020):
        nome = f'tse/{ano}/consulta_cand_{ano}_SP.csv'
        with (brutos / nome).open(encoding='cp1252', newline='') as f:
            leitor = csv.DictReader(f, delimiter=';')
            colunas = [c for c in COLUNAS_TSE if c in leitor.fieldnames]
            linhas = [{c: r[c] for c in colunas} for r in leitor if r['DS_CARGO'] == 'PREFEITO']
        saida = io.StringIO(newline='')
        escritor = csv.DictWriter(saida, fieldnames=colunas, delimiter=';', quoting=csv.QUOTE_ALL)
        escritor.writeheader(); escritor.writerows(linhas)
        (tmp / f'tse_{ano}.csv').write_bytes(saida.getvalue().encode('cp1252'))
        arquivos[f'dados/brutos/{nome}'] = tmp / f'tse_{ano}.csv'
    arquivos['dados/brutos/ibge/municipios_sp.json'] = brutos / 'ibge/municipios_sp.json'

    # Varredura final: nenhuma coluna de texto com documento pessoal.
    for interno, local in arquivos.items():
        if interno.endswith('.parquet'):
            texto = [c for c, t in con.execute(f"SELECT column_name, column_type FROM (DESCRIBE '{local}')").fetchall()
                if t == 'VARCHAR']
            for coluna in texto:
                n = con.execute(f"SELECT count(*) FROM '{local}' WHERE regexp_matches({coluna}, '{DOCUMENTO}')").fetchone()[0]
                if n:
                    raise SystemExit(f'{interno}: {n} linhas com documento pessoal em {coluna}')
            print(f'{interno}: {con.execute(f"SELECT count(*) FROM {chr(39)}{local}{chr(39)}").fetchone()[0]} linhas')
        elif interno.endswith('.csv'):
            if re.search(DOCUMENTO, local.read_text(encoding='cp1252'), re.MULTILINE):
                raise SystemExit(f'{interno}: documento pessoal no CSV')

    # Data fixa e ordem fixa: o mesmo conteúdo gera o mesmo zip. Parquet já é comprimido; vai sem compressão.
    with zipfile.ZipFile(destino, 'w') as z:
        for interno in sorted(arquivos):
            info = zipfile.ZipInfo(interno, DATA_FIXA)
            info.compress_type = zipfile.ZIP_STORED if interno.endswith('.parquet') else zipfile.ZIP_DEFLATED
            z.writestr(info, arquivos[interno].read_bytes())
    sha = hashlib.sha256(destino.read_bytes()).hexdigest()
    print(f'{destino}: {destino.stat().st_size / 1e6:.0f} MB, sha256 {sha}')


if __name__ == '__main__':
    main()
