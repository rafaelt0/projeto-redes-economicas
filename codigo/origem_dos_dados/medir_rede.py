"""Mede a rede prefeitura-fornecedor por mandato e testa se o fornecedor que já atendia o partido que assume continua.

Para a aresta (município m, empresa f) do mandato antes da transição, `atende_partido_novo` diz se f vendeu, no mesmo
mandato, a outro município governado pelo partido que assume em m. O placebo `atende_partido_antigo` faz o mesmo com o
partido que sai: se a ligação política importa, a diferença do partido novo supera a do antigo.

Uso: .venv/bin/python -I codigo/origem_dos_dados/medir_rede.py
Entrada (dados/limpos/): rede_{2009..2024}.parquet, mandatos.parquet, transicoes.parquet, receita_estabelecimentos.parquet.
Saída: dados/limpos/arestas_mandato.parquet (uma linha por mandato, município e empresa),
dados/limpos/permanencia.parquet (uma linha por aresta do mandato antes de cada transição) e relatorios/relatorio_rede.md.
"""

import random
from collections import Counter
from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parents[2]
LIMPOS = RAIZ / "dados/limpos"
ARESTAS = LIMPOS / "arestas_mandato.parquet"
PERMANENCIA = LIMPOS / "permanencia.parquet"
RELATORIO = RAIZ / "relatorios/relatorio_rede.md"
REPLICAS = 200
SEMENTE = 2026

# Faixas finas porque, mesmo dentro de 21+, o tamanho ainda confunde. Empresa de 1 cliente não atende outro município
# e fica fora das comparações de partido.
FAIXAS = ["1", "2", "3", "4-5", "6-10", "11-20", "21-50", "51+"]
FAIXA = """CASE WHEN n_clientes <= 3 THEN n_clientes::VARCHAR WHEN n_clientes <= 5 THEN '4-5'
    WHEN n_clientes <= 10 THEN '6-10' WHEN n_clientes <= 20 THEN '11-20' WHEN n_clientes <= 50 THEN '21-50' ELSE '51+' END"""

# Cada análise define quais arestas entram, o resultado (1 = continua) e o peso de cada aresta.
# Cada contraste roda todas as análises na sua população (view): os de partido em `populacao`, a alternância em
# `comparavel`.
ANALISES = {
    "continua": ("true", "destino = 'continua'", "1"),
    "continua entre as que seguem na rede": ("segue_na_rede", "destino = 'continua'", "1"),
    "continua, ponderado pelo valor": ("true", "destino = 'continua'", "valor"),
    "continua, anos_ativos >= 2": ("anos_ativos >= 2", "destino = 'continua'", "1"),
}
# Subgrupos: a mesma análise "continua" separada por transição e por tamanho, para ver se algum grupo destoa.
SUBGRUPOS = {f"transição {e}": f"eleicao_transicao = {e}" for e in (2012, 2016, 2020)} | {
    "2 a 3 clientes": "n_clientes BETWEEN 2 AND 3", "4 a 10 clientes": "n_clientes BETWEEN 4 AND 10",
    "11 a 50 clientes": "n_clientes BETWEEN 11 AND 50", "51+ clientes": "n_clientes > 50"}
ANALISES |= {f"continua, {nome}": (filtro, "destino = 'continua'", "1") for nome, filtro in SUBGRUPOS.items()}
CONTRASTES = {"partido novo": ("atende_partido_novo", "populacao"), "partido antigo": ("atende_partido_antigo", "populacao"),
    "alternância": ("alternancia", "comparavel")}
DIF_CONTRASTES = "diferença (novo - antigo)"

relatorio = ["# Medidas de rede e permanência dos fornecedores depois da troca de partido\n"]


def secao(titulo, texto=""):
    relatorio.append(f"\n## {titulo}\n\n{texto}")


def tabela(sql):
    res = con.execute(sql)
    cols = [d[0] for d in res.description]
    def fmt(v):
        if v is None or isinstance(v, bool):
            return {None: "", True: "sim", False: "não"}[v]
        return f"{v:,}".replace(",", ".") if isinstance(v, int) else str(v)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(fmt(v) for v in linha) + " |" for linha in res.fetchall()]
    relatorio.append("\n".join(out) + "\n")


(LIMPOS / "tmp").mkdir(parents=True, exist_ok=True)
con = duckdb.connect()
con.execute(f"SET memory_limit = '1500MB'; SET temp_directory = '{LIMPOS / 'tmp'}'; SET preserve_insertion_order = false")
con.execute("SET enable_progress_bar = false")

# Mandato da eleição e = anos e+1 a e+4.
con.execute(f"""CREATE TABLE venda AS
SELECT ((ano - 1) // 4) * 4 AS eleicao, ano, codigo_ibge, cnpj, left(cnpj, 8) AS raiz, cnae_principal, empenhos, valor
FROM (SELECT *, regexp_extract(filename, 'rede_(\\d{{4}})\\.parquet', 1)::INT AS ano
      FROM read_parquet('{LIMPOS}/rede_*.parquet', filename = true))""")

con.execute("""CREATE TABLE aresta AS
SELECT eleicao, codigo_ibge, raiz, sum(valor) AS valor, sum(empenhos) AS empenhos, count(DISTINCT ano) AS anos_ativos
FROM venda GROUP BY ALL""")

# Raiz baixada: todos os CNPJs dela que já apareceram na rede estão baixados hoje. Sem cadastro, baixa não confirmada.
con.execute(f"""CREATE TABLE raiz_baixada AS
SELECT left(c.cnpj, 8) AS raiz, bool_and(coalesce(r.situacao_cadastral = '08', false)) AS baixada
FROM (SELECT DISTINCT cnpj FROM venda) c LEFT JOIN '{LIMPOS}/receita_estabelecimentos.parquet' r USING (cnpj)
GROUP BY 1""")

con.execute(f"""CREATE TABLE empresa_mandato AS
WITH clientes AS (
    SELECT a.eleicao, a.raiz, count(*) AS n_clientes, count(DISTINCT m.partido_inicio) AS n_partidos
    FROM aresta a LEFT JOIN '{LIMPOS}/mandatos.parquet' m USING (codigo_ibge, eleicao) GROUP BY ALL),
setor AS (
    SELECT eleicao, raiz, left(arg_max(cnae_principal, (valor, cnpj)), 2) AS setor
    FROM (SELECT eleicao, raiz, cnpj, min(cnae_principal) AS cnae_principal, sum(valor) AS valor FROM venda GROUP BY ALL)
    GROUP BY ALL)
SELECT c.*, s.setor, b.baixada
FROM clientes c JOIN setor s USING (eleicao, raiz) JOIN raiz_baixada b USING (raiz)""")

con.execute(f"""CREATE TABLE clientes_por_partido AS
SELECT a.eleicao, a.raiz, m.partido_inicio AS partido, count(*) AS clientes
FROM aresta a JOIN '{LIMPOS}/mandatos.parquet' m USING (codigo_ibge, eleicao)
WHERE m.partido_inicio IS NOT NULL GROUP BY ALL""")

# Clientes de f no partido P fora de m = clientes de f em P, menos 1 se o próprio m é de P.
def atende(partido, alias):
    return f"""CASE WHEN {partido} IS NOT NULL THEN coalesce({alias}.clientes, 0)
        - coalesce(proprio.partido_inicio = {partido}, false)::INT > 0 END"""


con.execute(f"""CREATE TABLE permanencia AS
SELECT a.eleicao, a.eleicao + 4 AS eleicao_transicao, a.codigo_ibge, a.raiz, a.valor, a.empenhos, a.anos_ativos,
    t.alternancia, t.mesmo_prefeito, t.mandatos_inteiros, t.partido_antes, t.partido_depois,
    {atende('t.partido_depois', 'novo')} AS atende_partido_novo,
    {atende('t.partido_antes', 'antigo')} AS atende_partido_antigo,
    e.n_clientes, e.n_partidos, e.setor, e.baixada, {FAIXA} AS faixa_clientes,
    CASE WHEN depois.raiz IS NOT NULL THEN 'continua'
        WHEN segue.raiz IS NOT NULL THEN 'perdeu_cliente_segue_na_rede'
        WHEN e.baixada THEN 'saiu_da_rede_baixada'
        ELSE 'saiu_da_rede_ativa' END AS destino,
    destino = 'continua' AS continua,
    destino IN ('continua', 'perdeu_cliente_segue_na_rede') AS segue_na_rede
FROM aresta a
JOIN empresa_mandato e USING (eleicao, raiz)
LEFT JOIN '{LIMPOS}/transicoes.parquet' t ON t.codigo_ibge = a.codigo_ibge AND t.eleicao = a.eleicao + 4
LEFT JOIN '{LIMPOS}/mandatos.parquet' proprio ON proprio.codigo_ibge = a.codigo_ibge AND proprio.eleicao = a.eleicao
LEFT JOIN clientes_por_partido novo ON novo.eleicao = a.eleicao AND novo.raiz = a.raiz AND novo.partido = t.partido_depois
LEFT JOIN clientes_por_partido antigo ON antigo.eleicao = a.eleicao AND antigo.raiz = a.raiz
    AND antigo.partido = t.partido_antes
LEFT JOIN aresta depois ON depois.eleicao = a.eleicao + 4 AND depois.codigo_ibge = a.codigo_ibge AND depois.raiz = a.raiz
LEFT JOIN (SELECT DISTINCT eleicao, raiz FROM aresta) segue ON segue.eleicao = a.eleicao + 4 AND segue.raiz = a.raiz
WHERE a.eleicao IN (2008, 2012, 2016)""")
con.execute("CREATE VIEW comparavel AS SELECT * FROM permanencia WHERE mandatos_inteiros AND alternancia IS NOT NULL")
# Os dois contrastes na mesma população, para que a diferença entre eles compare as mesmas arestas.
con.execute("""CREATE VIEW populacao AS SELECT * FROM comparavel
WHERE alternancia AND n_clientes >= 2 AND atende_partido_novo IS NOT NULL AND atende_partido_antigo IS NOT NULL""")

dois_partidos = dict(con.execute("""SELECT n_clientes = 2, round(100 * avg((n_partidos >= 2)::INT))::INT
FROM empresa_mandato WHERE n_clientes = 2 OR n_clientes >= 6 GROUP BY 1""").fetchall())
secao("Tamanho da rede por mandato",
      "Nó empresa = raiz do CNPJ (8 dígitos). Partido do município = partido do prefeito eleito no início do mandato; "
      "município sem prefeito conhecido não conta partido. Mandato 2008 = anos 2009 a 2012. Ter clientes de 2 ou mais "
      f"partidos é quase o mesmo que ter 2 ou mais clientes ({dois_partidos[True]}% das empresas com 2 clientes e "
      f"{dois_partidos[False]}% das com 6 ou mais), por isso essa medida não serve de ponte.\n")
tabela("""SELECT a.eleicao::VARCHAR AS mandato, a.arestas, e.empresas, a.municipios, e.pct_empresas_2_partidos,
    e.mediana_clientes
FROM (SELECT eleicao, count(*) AS arestas, count(DISTINCT codigo_ibge) AS municipios FROM aresta GROUP BY 1) a
JOIN (SELECT eleicao, count(*) AS empresas, round(100 * avg((n_partidos >= 2)::INT), 1) AS pct_empresas_2_partidos,
        median(n_clientes) AS mediana_clientes
    FROM empresa_mandato GROUP BY 1) e USING (eleicao)
ORDER BY a.eleicao""")

secao("Destino das arestas por transição e alternância",
      "Só municípios com mandatos inteiros (sem suplementar) e prefeito conhecido nos dois lados. "
      "Alternância: muda o partido e o prefeito. `pct_*`: % das arestas da linha. Sem baixa confirmada não significa "
      "cadastro ativo: inclui outras situações cadastrais e cadastro ausente. No Parquet, o nome legado desse "
      "destino é `saiu_da_rede_ativa`.\n")
tabela("""SELECT coalesce(eleicao_transicao::VARCHAR, 'todas') AS transicao, alternancia, count(*) AS arestas,
    count(*) FILTER (destino = 'continua') AS continua,
    count(*) FILTER (destino = 'perdeu_cliente_segue_na_rede') AS perdeu_cliente_segue_na_rede,
    count(*) FILTER (destino = 'saiu_da_rede_ativa') AS saiu_sem_baixa_confirmada,
    count(*) FILTER (destino = 'saiu_da_rede_baixada') AS saiu_da_rede_baixada,
    round(100 * avg((destino = 'continua')::INT), 1) AS pct_continua,
    round(100 * avg((destino = 'perdeu_cliente_segue_na_rede')::INT), 1) AS pct_perdeu_segue,
    round(100 * avg((destino = 'saiu_da_rede_ativa')::INT), 1) AS pct_saiu_sem_baixa_confirmada,
    round(100 * avg((destino = 'saiu_da_rede_baixada')::INT), 1) AS pct_saiu_baixada
FROM comparavel GROUP BY GROUPING SETS ((eleicao_transicao, alternancia), (alternancia))
ORDER BY eleicao_transicao NULLS LAST, alternancia""")

secao("Atende o partido novo, por faixa de clientes",
      "População das comparações: mandatos inteiros, alternância e empresa com 2 ou mais clientes. `atende_partido_novo`: "
      "a empresa vendeu no mesmo mandato a outro município governado pelo partido que assume. `atende_partido_antigo`: "
      "o mesmo com o partido que sai. `pct_continua_com` e `pct_continua_sem`: % das arestas que continuam, com e sem "
      "`atende_partido_novo`.\n")
taxas = """count(*) AS arestas, round(100 * avg(atende_partido_novo::INT), 1) AS pct_atende_partido_novo,
    round(100 * avg(continua::INT) FILTER (atende_partido_novo), 1) AS pct_continua_com,
    round(100 * avg(continua::INT) FILTER (NOT atende_partido_novo), 1) AS pct_continua_sem,
    round(100 * avg(atende_partido_antigo::INT), 1) AS pct_atende_partido_antigo"""
tabela(f"""SELECT * FROM (
    SELECT '2+' AS faixa_clientes, {taxas} FROM populacao
    UNION ALL SELECT faixa_clientes, {taxas} FROM populacao GROUP BY ALL)
ORDER BY list_position({['2+'] + FAIXAS}, faixa_clientes)""")

# Contagens por município x grupo (análise, contraste, estrato, atende), para a estimativa e o bootstrap.
# O grupo vira um inteiro porque agrupar ~130 milhões de linhas por texto leva minutos e por inteiro, segundos.
con.execute("CREATE TABLE contagem (analise VARCHAR, contraste VARCHAR, codigo_ibge VARCHAR, estrato VARCHAR, "
            "atende BOOLEAN, n DOUBLE, k DOUBLE)")
for nome, (filtro, resultado, peso) in ANALISES.items():
    for contraste, (coluna, populacao) in CONTRASTES.items():
        con.execute(f"""INSERT INTO contagem
SELECT '{nome}', '{contraste}', codigo_ibge, concat_ws('|', faixa_clientes, coalesce(setor, '??'), eleicao_transicao),
    {coluna}, sum({peso})::DOUBLE, sum(CASE WHEN {resultado} THEN {peso} ELSE 0 END)::DOUBLE
FROM {populacao} WHERE {filtro} GROUP BY ALL""")
con.execute("""CREATE TABLE grupo AS
SELECT row_number() OVER (ORDER BY analise, contraste, estrato, atende)::INT AS grupo, *
FROM (SELECT DISTINCT analise, contraste, estrato, atende FROM contagem)""")
con.execute("CREATE TABLE celula AS SELECT g.grupo, c.codigo_ibge, c.n, c.k FROM contagem c JOIN grupo g "
            "USING (analise, contraste, estrato, atende)")
# Réplica 0 é a amostra original; as outras reamostram municípios com reposição (vezes = quantas vezes saiu).
# Um sorteio por população, cada um com a mesma semente: os contrastes de partido mantêm as réplicas de antes.
sorteio = []
for populacao in sorted({p for _, p in CONTRASTES.values()}):
    municipios = [m for (m,) in con.execute(f"SELECT DISTINCT codigo_ibge FROM {populacao} ORDER BY 1").fetchall()]
    sorteio += [(populacao, 0, m, 1) for m in municipios]
    rng = random.Random(SEMENTE)
    for replica in range(1, REPLICAS + 1):
        sorteio += [(populacao, replica, m, vezes)
                    for m, vezes in sorted(Counter(rng.choices(municipios, k=len(municipios))).items())]
con.execute("CREATE TABLE sorteio (populacao VARCHAR, replica INT, codigo_ibge VARCHAR, vezes INT)")
con.executemany("INSERT INTO sorteio VALUES (?, ?, ?, ?)", sorteio)

# Diferença atende - não atende de Mantel-Haenszel: média das diferenças dos estratos com peso w = n1*n0/(n1+n0).
# Um contraste por vez: os três juntos estouram o disco no agregado por réplica e grupo.
con.execute("CREATE TABLE diferenca (replica INT, analise VARCHAR, contraste VARCHAR, dif DOUBLE, estratos BIGINT)")
for contraste, (_, populacao) in CONTRASTES.items():
    con.execute(f"""INSERT INTO diferenca
WITH somado AS (
    SELECT s.replica, c.grupo, sum(c.n * s.vezes) AS n, sum(c.k * s.vezes) AS k
    FROM celula c JOIN sorteio s ON s.codigo_ibge = c.codigo_ibge AND s.populacao = '{populacao}'
    WHERE c.grupo IN (SELECT grupo FROM grupo WHERE contraste = '{contraste}') GROUP BY ALL),
por_estrato AS (
    SELECT replica, analise, contraste, estrato,
        sum(n) FILTER (atende) AS n1, sum(k) FILTER (atende) AS k1, sum(n) FILTER (NOT atende) AS n0,
        sum(k) FILTER (NOT atende) AS k0
    FROM somado JOIN grupo USING (grupo) GROUP BY ALL)
SELECT replica, analise, contraste,
    sum(n1 * n0 / (n1 + n0) * (k1 / n1 - k0 / n0)) / sum(n1 * n0 / (n1 + n0)) AS dif, count(*) AS estratos
FROM por_estrato WHERE n1 > 0 AND n0 > 0 GROUP BY ALL""")
con.execute(f"""INSERT INTO diferenca
SELECT replica, analise, '{DIF_CONTRASTES}', sum(CASE WHEN contraste = 'partido novo' THEN dif ELSE -dif END), NULL
FROM diferenca WHERE contraste IN ('partido novo', 'partido antigo') GROUP BY ALL HAVING count(*) = 2""")

def tabela_diferenca(analises, com_ic):
    lista = ", ".join(f"'{a}'" for a in analises)
    ic = f"""round(100 * quantile_cont(b.dif, 0.025), 2) AS ic95_inf_pp, round(100 * quantile_cont(b.dif, 0.975), 2)
        AS ic95_sup_pp, count(b.dif) AS replicas,""" if com_ic else ""
    tabela(f"""SELECT o.analise AS resultado, o.contraste, round(100 * o.dif, 2) AS dif_atende_menos_nao_pp, {ic}
    o.estratos AS estratos_usados
FROM diferenca o LEFT JOIN diferenca b ON b.replica > 0 AND b.analise = o.analise AND b.contraste = o.contraste
WHERE o.replica = 0 AND o.analise IN ({lista})
GROUP BY o.analise, o.contraste, o.dif, o.estratos
ORDER BY list_position([{lista}], o.analise),
    list_position(['partido novo', 'partido antigo', '{DIF_CONTRASTES}', 'alternância'], o.contraste)""")


secao("Diferença atende - não atende, estratificada (Mantel-Haenszel)",
      "Estrato = faixa de clientes x divisão CNAE do setor x transição. Nos contrastes de partido, entram empresas "
      "com 2 ou mais clientes. Em cada estrato, diferença entre a "
      "taxa de continuar das arestas que atendem o partido e das que não atendem; a média usa o peso "
      "w = n1*n0/(n1+n0). Estratos sem um dos dois grupos ficam fora, e cada contraste usa os seus. O placebo troca o "
      "partido que assume pelo que sai: se a ligação política importa, a diferença do partido novo é maior que a do "
      f"antigo (linha `{DIF_CONTRASTES}`). 'Continua entre as que seguem na rede' exclui as arestas de empresas que não "
      "aparecem na rede observada no mandato seguinte, e separa isso de perder "
      "o cliente. O contraste 'alternância' compara as arestas de municípios com e sem alternância, em todas as "
      "arestas comparáveis (inclusive de empresas com 1 cliente) e com os mesmos critérios de estratificação: mede a "
      "associação entre alternância e continuidade. O desenho não identifica um efeito causal. Em pontos percentuais.\n")
tabela("""SELECT analise AS resultado, contraste, sum(n)::BIGINT AS arestas, sum(n) FILTER (atende)::BIGINT AS arestas_atende,
    count(DISTINCT estrato) AS estratos, count(DISTINCT codigo_ibge) AS municipios
FROM contagem WHERE analise IN ('continua', 'continua entre as que seguem na rede')
GROUP BY ALL ORDER BY 1, 2 DESC""")
tabela_diferenca(["continua", "continua entre as que seguem na rede"], com_ic=False)

secao("Intervalo de confiança de 95% (bootstrap por município)",
      f"Reamostra os municípios com reposição ({REPLICAS} réplicas, semente {SEMENTE}); cada município leva todas as "
      "suas arestas das três transições. Os dois contrastes de partido usam as mesmas réplicas, e a diferença entre "
      "eles é calculada réplica a réplica; a alternância sorteia à parte entre os seus municípios. Intervalo pelos "
      "percentis 2,5 e 97,5.\n")
tabela_diferenca(["continua", "continua entre as que seguem na rede"], com_ic=True)

secao("Robustez",
      "A mesma diferença da seção de Mantel-Haenszel, com cada real empenhado no mandato anterior contando como uma "
      "observação (peso = valor da aresta), e restrita às arestas com venda em 2 ou mais anos do mandato.\n")
tabela_diferenca(["continua", "continua, ponderado pelo valor", "continua, anos_ativos >= 2"], com_ic=True)

secao("Por transição e por tamanho",
      "A análise \"continua\" separada em subgrupos, com os mesmos estratos e as mesmas réplicas do bootstrap. "
      "Com 7 subgrupos, um intervalo que exclui o zero por acaso já é esperado de vez em quando.\n")
tabela_diferenca([f"continua, {nome}" for nome in SUBGRUPOS], com_ic=True)

con.execute(f"COPY (SELECT * FROM aresta ORDER BY eleicao, codigo_ibge, raiz) TO '{ARESTAS}'")
con.execute(f"COPY (SELECT * FROM permanencia ORDER BY eleicao, codigo_ibge, raiz) TO '{PERMANENCIA}'")
RELATORIO.write_text("\n".join(relatorio))
print(f"relatório: {RELATORIO}\narestas: {ARESTAS}\npermanência: {PERMANENCIA}")
