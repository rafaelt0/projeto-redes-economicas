"""Perfil dos fornecedores da amostra final (permanencia_auditada.parquet).

Unidade principal: fornecedor-mandato (raiz do CNPJ x mandato anterior à eleição).
Gera docs/publicacao/tabelas/perfil_fornecedores.json e a página docs/publicacao/fornecedores.html. Descritivo, sem inferência.
"""
import decimal
import json
import pathlib

import duckdb

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LIMPOS = RAIZ / "dados" / "limpos"
SAIDA = RAIZ / "docs" / "publicacao" / "tabelas" / "perfil_fornecedores.json"
MODELO = RAIZ / "codigo" / "fornecedores_modelo.html"
PAGINA = RAIZ / "docs" / "publicacao" / "fornecedores.html"

# Seções da CNAE 2.0 por faixa de divisão (dois primeiros dígitos).
SECOES = [
    (1, 3, "A", "Agropecuária"),
    (5, 9, "B", "Indústrias extrativas"),
    (10, 33, "C", "Indústria de transformação"),
    (35, 35, "D", "Eletricidade e gás"),
    (36, 39, "E", "Coleta de lixo e resíduos"),
    (41, 43, "F", "Construção"),
    (45, 47, "G", "Comércio (inclui veículos e peças)"),
    (49, 53, "H", "Transporte e correio"),
    (55, 56, "I", "Alojamento e alimentação"),
    (58, 63, "J", "Informação e comunicação"),
    (64, 66, "K", "Financeiras e seguros"),
    (68, 68, "L", "Imobiliárias"),
    (69, 75, "M", "Profissionais, científicas e técnicas"),
    (77, 82, "N", "Administrativas e serviços complementares"),
    (84, 84, "O", "Administração pública"),
    (85, 85, "P", "Educação"),
    (86, 88, "Q", "Saúde e serviços sociais"),
    (90, 93, "R", "Artes, cultura e esporte"),
    (94, 96, "S", "Outros serviços"),
    (97, 97, "T", "Serviços domésticos"),
    (99, 99, "U", "Organismos internacionais"),
]

# Nomes resumidos das divisões CNAE 2.0 que aparecem entre as maiores.
DIVISOES = {
    "01": "Agricultura e pecuária",
    "25": "Produtos de metal",
    "41": "Construção de edifícios",
    "43": "Serviços especializados de construção",
    "45": "Comércio e reparação de veículos e peças",
    "46": "Comércio atacadista",
    "47": "Comércio varejista",
    "49": "Transporte terrestre",
    "56": "Alimentação",
    "77": "Aluguéis não imobiliários",
    "82": "Serviços de escritório e apoio administrativo",
    "85": "Educação",
    "86": "Atenção à saúde humana",
    "90": "Atividades artísticas e de espetáculos",
    "94": "Organizações associativas",
}

# Grupos de natureza jurídica (códigos da Receita).
NATUREZAS = """
CASE
  WHEN natureza_juridica IN ('2062', '2240') THEN 'Sociedade limitada'
  WHEN natureza_juridica = '2135' THEN 'Empresário individual (inclui MEI)'
  WHEN natureza_juridica IN ('2305', '2313', '2321') THEN 'EIRELI ou unipessoal'
  WHEN natureza_juridica IN ('2046', '2054') THEN 'Sociedade anônima'
  WHEN natureza_juridica IN ('2143', '2330') THEN 'Cooperativa'
  WHEN natureza_juridica LIKE '3%' THEN 'Associação, fundação ou OS'
  WHEN natureza_juridica LIKE '1%' OR natureza_juridica IN ('2011', '2038') THEN 'Setor público ou estatal'
  WHEN natureza_juridica IS NULL THEN 'Sem cadastro'
  ELSE 'Outras'
END
"""

PORTES = """
CASE porte WHEN '01' THEN 'Microempresa' WHEN '03' THEN 'Pequeno porte'
           WHEN '05' THEN 'Demais' ELSE 'Não informado' END
"""


def linhas(con, sql):
    rel = con.sql(sql)
    cols = rel.columns
    # Arredonda: a soma paralela do DuckDB varia na 13ª casa entre rodadas.
    arred = lambda v: round(float(v), 6) if isinstance(v, (float, decimal.Decimal)) else v
    return [{c: arred(v) for c, v in zip(cols, r)} for r in rel.fetchall()]


def main():
    con = duckdb.connect()
    con.sql(f"CREATE VIEW p AS SELECT * FROM '{LIMPOS / 'publicacao' / 'permanencia_auditada.parquet'}'")
    secoes = ", ".join(f"({a}, {b}, '{l}', '{n}')" for a, b, l, n in SECOES)
    con.sql(f"CREATE TABLE secoes(ini INT, fim INT, letra VARCHAR, nome VARCHAR); INSERT INTO secoes VALUES {secoes}")

    # Fornecedor-mandato: soma das arestas do mandato.
    con.sql(f"""
        CREATE TABLE fm AS
        SELECT p.raiz, p.eleicao,
               min(p.n_clientes) AS n_clientes,
               min(p.setor) AS setor,
               bool_or(p.baixada) AS baixada,
               sum(p.valor)::DOUBLE AS valor,
               count(*) AS arestas_amostra,
               avg(p.continua::INT) AS taxa_continua,
               {NATUREZAS} AS natureza,
               {PORTES} AS porte
        FROM p
        LEFT JOIN '{LIMPOS / 'receita_empresas.parquet'}' e ON e.cnpj_basico = p.raiz
        GROUP BY p.raiz, p.eleicao, natureza, porte
    """)
    con.sql("""
        CREATE TABLE fm2 AS
        SELECT fm.*, s.letra, coalesce(s.nome, 'Sem CNAE') AS secao
        FROM fm LEFT JOIN secoes s ON TRY_CAST(fm.setor AS INT) BETWEEN s.ini AND s.fim
    """)

    total = linhas(con, """
        SELECT (SELECT count(*) FROM p) AS arestas,
               count(DISTINCT raiz) AS fornecedores,
               count(*) AS fornecedores_mandato,
               sum(valor) / 1e9 AS valor_bi,
               median(n_clientes) AS mediana_clientes,
               avg((n_clientes = 1)::INT) AS parcela_um_cliente,
               avg(baixada::INT) AS parcela_baixada
        FROM fm2
    """)[0]
    total["municipios"] = con.sql("SELECT count(DISTINCT codigo_ibge) FROM p").fetchall()[0][0]

    por_mandato = linhas(con, """
        SELECT eleicao, count(*) AS fornecedores, sum(valor) / 1e9 AS valor_bi,
               (SELECT count(*) FROM p WHERE p.eleicao = fm2.eleicao) AS arestas
        FROM fm2 GROUP BY eleicao ORDER BY eleicao
    """)

    faixa = """CASE WHEN n_clientes = 1 THEN '1' WHEN n_clientes = 2 THEN '2'
                    WHEN n_clientes <= 5 THEN '3-5' WHEN n_clientes <= 10 THEN '6-10'
                    WHEN n_clientes <= 50 THEN '11-50' ELSE '51+' END"""
    clientes = linhas(con, f"""
        SELECT {faixa} AS faixa, min(n_clientes) AS ordem,
               count(*) AS fornecedores, sum(arestas_amostra) AS arestas,
               sum(valor) / 1e9 AS valor_bi,
               sum(taxa_continua * arestas_amostra) / sum(arestas_amostra) AS taxa_continua
        FROM fm2 GROUP BY faixa ORDER BY ordem
    """)

    secao = linhas(con, """
        SELECT letra, secao, count(*) AS fornecedores, sum(valor) / 1e9 AS valor_bi,
               sum(arestas_amostra) AS arestas,
               sum(taxa_continua * arestas_amostra) / sum(arestas_amostra) AS taxa_continua
        FROM fm2 GROUP BY letra, secao ORDER BY fornecedores DESC
    """)

    divisoes = linhas(con, """
        SELECT setor AS divisao, count(*) AS fornecedores, sum(valor) / 1e9 AS valor_bi
        FROM fm2 GROUP BY setor ORDER BY fornecedores DESC, setor LIMIT 15
    """)
    for d in divisoes:
        d["nome"] = DIVISOES.get(d["divisao"])

    natureza = linhas(con, """
        SELECT natureza, count(*) AS fornecedores, sum(valor) / 1e9 AS valor_bi
        FROM fm2 GROUP BY natureza ORDER BY fornecedores DESC
    """)
    porte = linhas(con, """
        SELECT porte, count(*) AS fornecedores, sum(valor) / 1e9 AS valor_bi
        FROM fm2 GROUP BY porte ORDER BY fornecedores DESC
    """)

    concentracao = linhas(con, """
        WITH o AS (SELECT valor, row_number() OVER (ORDER BY valor DESC, raiz, eleicao) AS r,
                          count(*) OVER () AS n, sum(valor) OVER () AS t FROM fm2)
        SELECT sum(valor) FILTER (WHERE r <= n * 0.01) / max(t) AS top1,
               sum(valor) FILTER (WHERE r <= n * 0.10) / max(t) AS top10,
               sum(valor) FILTER (WHERE r > n * 0.50) / max(t) AS metade_menor,
               median(valor) AS mediana_valor
        FROM o
    """)[0]

    # Maiores fornecedores nos três mandatos somados; nome mais frequente no TCESP.
    redes = [str(LIMPOS / f"rede_{a}.parquet") for a in range(2009, 2021)]
    maiores = linhas(con, f"""
        WITH top AS (
            SELECT raiz, sum(valor) / 1e9 AS valor_bi, max(n_clientes) AS max_clientes,
                   count(*) AS mandatos, min(secao) AS secao, min(natureza) AS natureza
            FROM fm2 GROUP BY raiz ORDER BY valor_bi DESC, raiz LIMIT 20),
        nomes AS (
            SELECT left(cnpj, 8) AS raiz, arg_max(fornecedor, valor) AS nome
            FROM read_parquet({redes})
            WHERE left(cnpj, 8) IN (SELECT raiz FROM top) GROUP BY 1)
        SELECT top.*, nomes.nome FROM top LEFT JOIN nomes USING (raiz) ORDER BY valor_bi DESC, raiz
    """)

    dados = json.dumps({
        "total": total, "por_mandato": por_mandato, "clientes": clientes, "secoes": secao,
        "divisoes": divisoes, "natureza": natureza, "porte": porte,
        "concentracao": concentracao, "maiores": maiores,
        "nota": "Fornecedor-mandato = raiz do CNPJ x mandato (2009-12, 2013-16, 2017-20). "
                "Valores nominais em R$ bilhões. Porte e natureza do cadastro da Receita de 2026-10.",
    }, ensure_ascii=False, indent=1, default=float)
    SAIDA.write_text(dados, encoding="utf-8", newline='\n')
    PAGINA.write_text(MODELO.read_text(encoding="utf-8").replace("__DADOS__", dados), encoding="utf-8", newline='\n')
    print(SAIDA, PAGINA)


if __name__ == "__main__":
    main()
