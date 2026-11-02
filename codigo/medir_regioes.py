"""Repete os contrastes principais de permanência por região intermediária do IBGE.

Uso: .venv/bin/python -I codigo/medir_regioes.py
Lê dados/limpos/permanencia.parquet e dados/brutos/ibge/municipios_sp.json, sem downloads.
Gera somente relatorios/relatorio_regioes.md; não recalcula as medidas estaduais da rede.
"""

import json
import random
from collections import Counter
from pathlib import Path
from time import monotonic

import duckdb

RAIZ = Path(__file__).resolve().parent.parent
LIMPOS = RAIZ / "dados/limpos"
RELATORIO = RAIZ / "relatorios/relatorio_regioes.md"
REPLICAS, SEMENTE = 200, 2026
CONTRASTES = {"partido novo": ("atende_partido_novo", "populacao"),
              "partido antigo": ("atende_partido_antigo", "populacao"),
              "alternância": ("alternancia", "comparavel")}
DIFERENCA = "diferença (novo - antigo)"


def mapa_regioes(municipios):
    mapa, nomes = {}, {}
    for m in municipios:
        codigo = str(m["id"])
        r = m["regiao-imediata"]["regiao-intermediaria"]
        if (codigo in mapa or len(codigo) != 7 or not codigo.startswith("35")
                or r["UF"]["id"] != 35 or not r["id"] or not r["nome"]):
            raise ValueError(f"Município duplicado ou classificação IBGE inválida: {codigo}")
        if r["id"] in nomes and nomes[r["id"]] != r["nome"]:
            raise ValueError(f"Nomes conflitantes para a região {r['id']}")
        nomes[r["id"]] = r["nome"]
        mapa[codigo] = (r["id"], r["nome"])
    if len(mapa) != 645 or "3550308" not in mapa:
        raise ValueError("O mapa IBGE deve conter os 645 municípios de SP, inclusive a capital")
    del mapa["3550308"]
    return [(codigo, *r) for codigo, r in sorted(mapa.items())]


def tabela(con, sql):
    res = con.execute(sql)
    def fmt(v):
        if v is None:
            return "NA"
        return f"{v:,}".replace(",", ".") if isinstance(v, int) else str(v)
    linhas = ["| " + " | ".join(d[0] for d in res.description) + " |",
              "|" + "---|" * len(res.description)]
    linhas += ["| " + " | ".join(map(fmt, linha)) + " |" for linha in res.fetchall()]
    return "\n".join(linhas) + "\n"


def main():
    inicio = monotonic()
    mapa = mapa_regioes(json.loads((RAIZ / "dados/brutos/ibge/municipios_sp.json").read_text(encoding='utf-8')))
    (LIMPOS / "tmp_regioes").mkdir(exist_ok=True)
    con = duckdb.connect()
    con.execute(f"SET memory_limit = '1500MB'; SET temp_directory = '{LIMPOS / 'tmp_regioes'}'")
    con.execute("SET preserve_insertion_order = false; SET enable_progress_bar = false")
    con.execute(f"CREATE VIEW permanencia AS SELECT * FROM '{LIMPOS}/permanencia.parquet'")
    esperados = {m[0] for m in mapa}
    observados = {m for (m,) in con.execute("SELECT DISTINCT codigo_ibge FROM permanencia").fetchall()}
    if observados != esperados:
        raise ValueError(f"Cobertura diferente dos 644 municípios esperados: "
                         f"ausentes={sorted(esperados - observados)}, extras={list(observados - esperados)}")
    if con.execute("""SELECT count(*) FROM (
        SELECT eleicao, codigo_ibge, raiz FROM permanencia GROUP BY ALL HAVING count(*) > 1
        OR eleicao IS NULL OR raiz IS NULL)""").fetchone()[0]:
        raise ValueError("Permanência contém chaves de aresta duplicadas ou nulas")
    con.execute("CREATE TABLE mapa (codigo_ibge VARCHAR PRIMARY KEY, regiao_id INT, regiao VARCHAR)")
    con.executemany("INSERT INTO mapa VALUES (?, ?, ?)", mapa)
    # A igualdade dos conjuntos e a chave única são conferidas ANTES do filtro de comparabilidade.
    con.execute("CREATE VIEW regional AS SELECT p.*, m.regiao_id FROM permanencia p JOIN mapa m USING (codigo_ibge)")
    con.execute("CREATE VIEW comparavel AS SELECT * FROM regional WHERE mandatos_inteiros AND alternancia IS NOT NULL")
    con.execute("""CREATE VIEW populacao AS SELECT * FROM comparavel WHERE alternancia AND n_clientes >= 2
        AND atende_partido_novo IS NOT NULL AND atende_partido_antigo IS NOT NULL""")
    n_comparaveis = con.execute("SELECT count(DISTINCT codigo_ibge) FROM comparavel").fetchone()[0]
    print(f"Cobertura validada: 644/644 municípios antes dos filtros; {n_comparaveis} comparáveis", flush=True)

    con.execute("""CREATE TABLE contagem (regiao_id INT, contraste VARCHAR, codigo_ibge VARCHAR,
        estrato VARCHAR, atende BOOLEAN, n BIGINT, k BIGINT)""")
    for contraste, (coluna, populacao) in CONTRASTES.items():
        con.execute(f"""INSERT INTO contagem SELECT regiao_id, '{contraste}', codigo_ibge,
            concat_ws('|', faixa_clientes, coalesce(setor, '??'), eleicao_transicao), {coluna},
            count(*), sum((destino = 'continua')::INT)
            FROM {populacao} GROUP BY ALL""")
    con.execute("""CREATE TABLE amostra AS SELECT regiao_id, contraste, sum(n)::BIGINT AS n,
        coalesce(sum(n) FILTER (atende), 0)::BIGINT AS n1,
        coalesce(sum(n) FILTER (NOT atende), 0)::BIGINT AS n0,
        count(DISTINCT codigo_ibge) AS municipios FROM contagem GROUP BY ALL""")
    con.execute("CREATE TABLE sorteio (replica INT, codigo_ibge VARCHAR, vezes INT)")
    con.execute("""CREATE TABLE diferenca (regiao_id INT, contraste VARCHAR, replica INT,
        dif DOUBLE, estratos BIGINT, n_suporte BIGINT)""")
    regioes = con.execute("SELECT DISTINCT regiao_id, regiao FROM mapa ORDER BY 1").fetchall()
    for regiao_id, regiao in regioes:
        for populacao in ("populacao", "comparavel"):
            municipios = [m for (m,) in con.execute(f"""SELECT DISTINCT codigo_ibge FROM {populacao}
                WHERE regiao_id = {regiao_id} ORDER BY 1""").fetchall()]
            sorteio = [(0, m, 1) for m in municipios]
            rng = random.Random(SEMENTE)
            for replica in range(1, REPLICAS + 1):
                sorteio += [(replica, m, vezes) for m, vezes in sorted(
                    Counter(rng.choices(municipios, k=len(municipios))).items())]
            con.execute("DELETE FROM sorteio")
            if sorteio:
                con.executemany("INSERT INTO sorteio VALUES (?, ?, ?)", sorteio)
            for contraste, (_, p) in CONTRASTES.items():
                if p != populacao:
                    continue
                con.execute(f"""INSERT INTO diferenca
                WITH por_estrato AS (
                    SELECT s.replica, c.estrato,
                        sum(c.n * s.vezes) FILTER (atende) AS n1,
                        sum(c.k * s.vezes) FILTER (atende) AS k1,
                        sum(c.n * s.vezes) FILTER (NOT atende) AS n0,
                        sum(c.k * s.vezes) FILTER (NOT atende) AS k0
                    FROM contagem c JOIN sorteio s USING (codigo_ibge)
                    WHERE c.regiao_id = {regiao_id} AND c.contraste = '{contraste}' GROUP BY ALL)
                SELECT {regiao_id}, '{contraste}', replica,
                    sum(n1*n0/(n1+n0) * (k1/n1-k0/n0)) / sum(n1*n0/(n1+n0)),
                    count(*), sum(n1+n0)::BIGINT
                FROM por_estrato WHERE n1 > 0 AND n0 > 0 GROUP BY replica""")
        print(f"{regiao_id} — {regiao}: estimativas e bootstrap concluídos", flush=True)
    # Só há diferença quando ambos os contrastes existem na MESMA réplica.
    con.execute(f"""INSERT INTO diferenca SELECT n.regiao_id, '{DIFERENCA}', n.replica,
        n.dif - a.dif, NULL, NULL FROM diferenca n JOIN diferenca a USING (regiao_id, replica)
        WHERE n.contraste = 'partido novo' AND a.contraste = 'partido antigo'
        AND n.dif IS NOT NULL AND a.dif IS NOT NULL""")
    con.execute(f"""INSERT INTO amostra SELECT regiao_id, '{DIFERENCA}', n, NULL, NULL, municipios
        FROM amostra WHERE contraste = 'partido novo'""")
    con.execute("""CREATE TABLE intervalo AS SELECT regiao_id, contraste,
        quantile_cont(dif, 0.025) AS inferior, quantile_cont(dif, 0.975) AS superior,
        count(dif) AS replicas_validas FROM diferenca WHERE replica > 0 GROUP BY ALL""")

    relatorio = ["# Permanência dos fornecedores por região intermediária do IBGE\n",
        "## Cobertura e método\n\n"
        f"Mapa único por código IBGE: 644/644 municípios esperados de SP, excluída a capital, conferidos "
        f"em toda a permanência antes de filtrar; {n_comparaveis} municípios têm arestas comparáveis. "
        "Chaves de aresta também conferidas sem duplicatas. Região = município focal da aresta; a partição "
        "do IBGE disponível hoje (quadro de 2017) é aplicada retrospectivamente às transições de 2012, 2016 e 2020.\n\n"
        "São reutilizados n_clientes, vínculos com partidos, setor e faixa_clientes calculados na rede estadual; "
        "a rede não é recalculada dentro de cada região. Comparáveis: mandatos inteiros e alternância conhecida. "
        "Partidos novo/antigo: mesma população com alternância, 2+ clientes e ambos os vínculos conhecidos. "
        "Alternância: todas as arestas comparáveis, inclusive empresas com 1 cliente; muda partido e prefeito.\n\n"
        "Resultado principal: destino = continua. Em cada região, Mantel-Haenszel por faixa de clientes × divisão "
        "CNAE (ausente = ??) × transição: média das diferenças de taxas com peso n1*n0/(n1+n0). "
        "n1/n0 = arestas com/sem o vínculo de partido, ou com/sem alternância. Só estratos com n1>0 e n0>0 "
        "contribuem; n_suporte é o total de arestas nesses estratos. Cada contraste usa seu suporte, que pode "
        "diferir mesmo para a mesma população. A diferença novo − antigo compara essas duas estimativas; "
        "não tem exposição ou suporte próprios (NA nessas colunas); n e municípios são da população comum.\n\n"
        f"Bootstrap: {REPLICAS} réplicas, semente {SEMENTE}, reiniciada por região e população. Sorteiam-se "
        "municípios com reposição dentro de cada região e população, levando todas as suas transições. "
        "Novo e antigo compartilham os sorteios; sua diferença é calculada réplica a réplica somente quando "
        "ambos são estimáveis. Alternância tem seu sorteio na própria população. IC95 pelos percentis 2,5 e 97,5 "
        "das réplicas válidas; conta de válidas explícita, inclusive zero. Estimativa/IC sem suporte = NA. "
        "Diferenças e IC em pontos percentuais.\n",
        tabela(con, """SELECT m.regiao_id, m.regiao, count(*) AS municipios_mapa,
            count(p.codigo_ibge) AS municipios_permanencia, count(c.codigo_ibge) AS municipios_comparaveis
            FROM mapa m LEFT JOIN (SELECT DISTINCT codigo_ibge FROM permanencia) p USING (codigo_ibge)
            LEFT JOIN (SELECT DISTINCT codigo_ibge FROM comparavel) c USING (codigo_ibge) GROUP BY ALL ORDER BY 1""")]
    for regiao_id, regiao in regioes:
        relatorio.append(f"\n## {regiao_id} — {regiao}\n")
        relatorio.append(tabela(con, f"""SELECT g.contraste, coalesce(a.n, 0) AS n, a.n1, a.n0,
            coalesce(a.municipios, 0) AS municipios,
            CASE WHEN g.contraste != '{DIFERENCA}' THEN coalesce(o.estratos, 0) END AS estratos_usados,
            CASE WHEN g.contraste != '{DIFERENCA}' THEN coalesce(o.n_suporte, 0) END AS n_suporte,
            round(100*o.dif, 2) AS diferenca_pp, round(100*i.inferior, 2) AS ic95_inf_pp,
            round(100*i.superior, 2) AS ic95_sup_pp, coalesce(i.replicas_validas, 0) AS replicas_validas
            FROM (VALUES ('partido novo', 1), ('partido antigo', 2), ('{DIFERENCA}', 3), ('alternância', 4))
                g(contraste, ordem)
            LEFT JOIN amostra a ON a.regiao_id = {regiao_id} AND a.contraste = g.contraste
            LEFT JOIN diferenca o ON o.regiao_id = {regiao_id} AND o.contraste = g.contraste AND o.replica = 0
            LEFT JOIN intervalo i ON i.regiao_id = {regiao_id} AND i.contraste = g.contraste ORDER BY g.ordem"""))
    relatorio.append("\n## Limites de interpretação\n\n"
        "Associações observacionais: os controles não identificam efeito causal ou favorecimento. "
        "As comparações regionais são exploratórias e múltiplas, sem ajuste dos intervalos por multiplicidade. "
        "Fornecedores compartilhados geram dependência entre municípios e regiões, não resolvida pelo bootstrap "
        "por município. Suportes e composições diferem; não se testa diferença entre regiões comparando seus ICs "
        "separados (nem porque um inclui zero e outro não). A partição atual pode não representar a organização "
        "regional dos períodos antigos. Permanecem os limites da rede estadual: capital excluída, cadastro/CNAE "
        "posteriores e seleção dos fornecedores já presentes no mandato anterior.\n")
    RELATORIO.write_text("\n".join(relatorio), encoding="utf-8", newline='\n')
    con.close()
    print(f"relatório: {RELATORIO}\ntempo: {monotonic() - inicio:.1f}s")


if __name__ == "__main__":
    main()
