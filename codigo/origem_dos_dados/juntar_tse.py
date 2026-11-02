"""Junta os prefeitos eleitos (TSE) aos municípios do IBGE e marca as trocas de partido.

Uso: .venv/bin/python -I codigo/origem_dos_dados/juntar_tse.py
Entrada: dados/brutos/tse/{ano}/consulta_cand_{ano}_SP.csv (eleições de 2008, 2012, 2016 e 2020).
Saída: dados/limpos/prefeitos.parquet (um por eleição vencida), dados/limpos/transicoes.parquet
(um por município e eleição de 2012, 2016 e 2020), dados/limpos/mandatos.parquet (um por município e eleição)
e relatorios/relatorio_tse.md.
"""

import json
from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parents[2]
TSE = RAIZ / "dados/brutos/tse"
IBGE = RAIZ / "dados/brutos/ibge/municipios_sp.json"
LIMPOS = RAIZ / "dados/limpos"
PREFEITOS = LIMPOS / "prefeitos.parquet"
TRANSICOES = LIMPOS / "transicoes.parquet"
MANDATOS = LIMPOS / "mandatos.parquet"
RELATORIO = RAIZ / "relatorios/relatorio_tse.md"
ELEICOES = [2008, 2012, 2016, 2020]  # cada uma abre o mandato que começa no ano seguinte
CAPITAL = "3550308"  # fora do TCESP

# Grafias do TSE que não batem com o nome atual do IBGE.
APELIDOS = {"EMBU": "Embu das Artes", "SÃO LUÍS DO PARAITINGA": "São Luiz do Paraitinga"}

# O partido é comparado pelo número, que sobrevive às trocas de sigla (PMDB e MDB são 15, PR e PL são 22).
# Fusões mudam o número: PHS (31) virou Podemos (19), PRP (44) virou Patriota (51), PPL (54) virou PC do B (65),
# todas em 2019. Um prefeito do PHS em 2016 que se elege pelo Podemos em 2020 conta como troca.

relatorio = ["# Prefeitos eleitos (TSE) e trocas de partido\n"]


def secao(titulo, texto=""):
    relatorio.append(f"\n## {titulo}\n\n{texto}")


def tabela(sql):
    res = con.execute(sql)
    cols = [d[0] for d in res.description]
    fmt = lambda v: f"{v:,}".replace(",", ".") if isinstance(v, int) else str(v)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(fmt(v) for v in linha) + " |" for linha in res.fetchall()]
    relatorio.append("\n".join(out) + "\n")


con = duckdb.connect()
con.execute("CREATE MACRO norm(s) AS trim(regexp_replace(upper(strip_accents(s)), '[^A-Z0-9]+', ' ', 'g'))")
con.execute("CREATE TABLE ibge (codigo_ibge VARCHAR, nome_ibge VARCHAR)")
con.executemany("INSERT INTO ibge VALUES (?, ?)", [(str(m["id"]), m["nome"]) for m in json.loads(IBGE.read_text())])
con.execute("CREATE TABLE apelido (tse VARCHAR, ibge VARCHAR)")
con.executemany("INSERT INTO apelido VALUES (?, ?)", list(APELIDOS.items()))

# Os CSVs do TSE são cp1252; o DuckDB só lê latin-1 e recusa os bytes 0x80-0x9F, então passam por UTF-8 antes.
(LIMPOS / "tmp").mkdir(parents=True, exist_ok=True)
for ano in ELEICOES:
    origem = TSE / str(ano) / f"consulta_cand_{ano}_SP.csv"
    (LIMPOS / "tmp" / f"cand_{ano}.csv").write_text(origem.read_text(encoding="cp1252"), encoding="utf-8")

con.execute(f"""CREATE TABLE eleito AS
SELECT ANO_ELEICAO::INT AS eleicao, SG_UE AS ue_tse, NM_UE AS municipio_tse,
    NM_TIPO_ELEICAO = 'ELEIÇÃO SUPLEMENTAR' AS suplementar, strptime(DT_ELEICAO, '%d/%m/%Y')::DATE AS data_eleicao,
    NR_TURNO::INT AS turno, NR_PARTIDO AS nr_partido, SG_PARTIDO AS sg_partido, NM_CANDIDATO AS prefeito,
    NM_URNA_CANDIDATO AS nome_urna, NR_TITULO_ELEITORAL_CANDIDATO AS titulo_eleitor
FROM read_csv('{LIMPOS / "tmp"}/cand_*.csv', delim=';', all_varchar=true, union_by_name=true)
WHERE DS_CARGO = 'PREFEITO' AND DS_SIT_TOT_TURNO = 'ELEITO'""")
con.execute("""CREATE TABLE prefeito AS
SELECT i.codigo_ibge, i.nome_ibge AS municipio, e.*
FROM eleito e LEFT JOIN apelido a ON a.tse = e.municipio_tse
LEFT JOIN ibge i ON norm(i.nome_ibge) = norm(coalesce(a.ibge, e.municipio_tse))""")

secao("Casamento com o IBGE")
tabela("SELECT DISTINCT eleicao, ue_tse, municipio_tse FROM prefeito WHERE codigo_ibge IS NULL ORDER BY 1, 3")
tabela("""SELECT eleicao, count(DISTINCT codigo_ibge) FILTER (NOT suplementar) AS municipios_com_eleito_ordinario,
    count(*) FILTER (suplementar) AS suplementares, count(DISTINCT codigo_ibge) AS municipios
FROM prefeito GROUP BY 1 ORDER BY 1""")
secao("Mais de um eleito na mesma eleição ordinária", "Deve ficar vazia.\n")
tabela("""SELECT eleicao, codigo_ibge, municipio, count(*) AS eleitos FROM prefeito WHERE NOT suplementar
GROUP BY ALL HAVING count(*) > 1 ORDER BY 1, 3""")
secao("Municípios sem eleito na eleição ordinária",
      "Votos anulados (candidato com registro indeferido). O mandato fica com o vencedor da suplementar. "
      "Sem suplementar, o vencedor estava sub judice e o arquivo do TSE não registra quem assumiu: "
      "o mandato fica sem partido e as transições dele saem da comparação.\n")
tabela("""SELECT i.codigo_ibge, i.nome_ibge AS municipio, e.eleicao,
    (SELECT string_agg(strftime(data_eleicao, '%d/%m/%Y') || ' ' || sg_partido, ', ' ORDER BY data_eleicao) FROM prefeito p
     WHERE p.codigo_ibge = i.codigo_ibge AND p.eleicao = e.eleicao) AS suplementares
FROM ibge i CROSS JOIN (SELECT unnest(?::INT[]) AS eleicao) e
WHERE NOT EXISTS (SELECT 1 FROM prefeito p WHERE p.codigo_ibge = i.codigo_ibge AND p.eleicao = e.eleicao AND NOT p.suplementar)
ORDER BY 3, 2""".replace("?", str(ELEICOES)))

# Um mandato por município e eleição: quem assume no começo e quem termina. Com suplementar no meio, os dois diferem.
con.execute(f"""CREATE TABLE mandato AS
SELECT codigo_ibge, min(municipio) AS municipio, eleicao,
    arg_min(nr_partido, (data_eleicao, turno)) AS partido_inicio, arg_min(sg_partido, (data_eleicao, turno)) AS sigla_inicio,
    arg_min(titulo_eleitor, (data_eleicao, turno)) AS titulo_inicio,
    arg_max(nr_partido, (data_eleicao, turno)) AS partido_fim, arg_max(sg_partido, (data_eleicao, turno)) AS sigla_fim,
    arg_max(titulo_eleitor, (data_eleicao, turno)) AS titulo_fim,
    bool_and(suplementar) AS sem_eleito_ordinario, count(*) FILTER (suplementar) AS n_suplementares
FROM prefeito WHERE codigo_ibge IS NOT NULL AND codigo_ibge <> '{CAPITAL}' GROUP BY codigo_ibge, eleicao""")

# Transição na eleição t: o mandato que termina (eleição t-4) contra o que começa (eleição t).
# Uma linha por município do TCESP e eleição, mesmo sem prefeito conhecido de um dos lados (partidos NULL).
# alternancia: o partido muda e o prefeito também. O reeleito que trocou de legenda segue o mesmo grupo político.
# mandatos_inteiros: nenhum dos dois mandatos teve suplementar, então cada lado é um só prefeito eleito.
con.execute(f"""CREATE TABLE transicao AS
SELECT i.codigo_ibge, i.nome_ibge AS municipio, t.eleicao,
    a.sigla_fim AS sigla_antes, d.sigla_inicio AS sigla_depois, a.partido_fim AS partido_antes, d.partido_inicio AS partido_depois,
    a.titulo_fim = d.titulo_inicio AS mesmo_prefeito,
    a.partido_fim <> d.partido_inicio AND a.titulo_fim <> d.titulo_inicio AS alternancia,
    coalesce(a.n_suplementares = 0 AND d.n_suplementares = 0 AND NOT d.sem_eleito_ordinario, false) AS mandatos_inteiros
FROM ibge i CROSS JOIN (SELECT unnest({ELEICOES[1:]}) AS eleicao) t
LEFT JOIN mandato d ON d.codigo_ibge = i.codigo_ibge AND d.eleicao = t.eleicao
LEFT JOIN mandato a ON a.codigo_ibge = i.codigo_ibge AND a.eleicao = t.eleicao - 4
WHERE i.codigo_ibge <> '{CAPITAL}'""")

secao("Transições", "Uma linha por município e eleição. `mandatos_inteiros`: sem suplementar antes nem depois.\n")
tabela("""SELECT eleicao, count(*) AS municipios, count(*) FILTER (alternancia IS NULL) AS sem_prefeito_conhecido,
    count(*) FILTER (alternancia) AS alternancia,
    count(*) FILTER (mesmo_prefeito) AS reeleito_ou_mesmo_prefeito,
    count(*) FILTER (NOT mesmo_prefeito AND partido_antes = partido_depois) AS mesmo_partido_outro_prefeito,
    count(*) FILTER (mandatos_inteiros) AS mandatos_inteiros,
    count(*) FILTER (mandatos_inteiros AND alternancia) AS inteiros_com_alternancia
FROM transicao GROUP BY 1 ORDER BY 1""")
secao("Mesmo prefeito com partido diferente", "Prefeito que trocou de legenda: não conta como alternância.\n")
tabela("""SELECT eleicao, count(*) AS municipios FROM transicao WHERE mesmo_prefeito AND partido_antes <> partido_depois
GROUP BY 1 ORDER BY 1""")
secao("Partidos dos prefeitos (eleição ordinária e suplementar sem eleito ordinário)")
tabela(f"""PIVOT (SELECT eleicao, partido_inicio || ' ' || sigla_inicio AS partido FROM mandato) ON eleicao USING count(*)
ORDER BY "{ELEICOES[-1]}" DESC, 1""")
secao("Siglas diferentes com o mesmo número", "Renomeações, que o número trata como o mesmo partido.\n")
tabela("""SELECT nr_partido, string_agg(DISTINCT sg_partido, ', ' ORDER BY sg_partido) AS siglas FROM prefeito GROUP BY 1
HAVING count(DISTINCT sg_partido) > 1 ORDER BY 1""")

con.execute(f"COPY (SELECT * FROM prefeito WHERE codigo_ibge <> '{CAPITAL}' ORDER BY codigo_ibge, data_eleicao, turno) TO '{PREFEITOS}'")
con.execute(f"COPY (SELECT * FROM transicao ORDER BY codigo_ibge, eleicao) TO '{TRANSICOES}'")
con.execute(f"COPY (SELECT * FROM mandato ORDER BY codigo_ibge, eleicao) TO '{MANDATOS}'")
RELATORIO.write_text("\n".join(relatorio))
for ano in ELEICOES:
    (LIMPOS / "tmp" / f"cand_{ano}.csv").unlink()
print(f"relatório: {RELATORIO}\nprefeitos: {PREFEITOS}\ntransições: {TRANSICOES}\nmandatos: {MANDATOS}")
