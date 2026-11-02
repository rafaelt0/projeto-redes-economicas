"""Amostra auditada para publicação, preservando todas as bases originais.

Reexecutar antes de decompor_publicacao.py e estimar_painel.py.
Suplementar é evento nos registros de candidatura, mesmo sem vencedor ELEITO.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import unicodedata

import duckdb

RAIZ = Path(__file__).resolve().parent.parent
LIMPOS = RAIZ / 'dados/limpos'
SAIDA = LIMPOS / 'publicacao'


def normalizar(nome):
    nome = ''.join(c for c in unicodedata.normalize('NFKD', nome.upper()) if not unicodedata.combining(c))
    return re.sub('[^A-Z0-9]+', ' ', nome).strip()


def contar_eventos(linhas, eleicao, mapa):
    eventos = {}
    for r in linhas:
        if r['DS_CARGO'] != 'PREFEITO' or 'SUPLEMENTAR' not in r['NM_TIPO_ELEICAO']:
            continue
        nome = normalizar(r['NM_UE'])
        if nome not in mapa:
            raise ValueError(f'Município não mapeado em suplementar: {nome}')
        codigo = mapa[nome]
        if codigo == '3550308':
            continue
        chave = (codigo, r['DT_ELEICAO'])
        if chave not in eventos:
            eventos[chave] = dict(eleicao=eleicao, codigo_ibge=codigo, municipio=r['NM_UE'],
                data_eleicao=r['DT_ELEICAO'], candidaturas=0, eleitos=0)
        eventos[chave]['candidaturas'] += 1
        eventos[chave]['eleitos'] += r['DS_SIT_TOT_TURNO'] == 'ELEITO'
    return sorted(eventos.values(), key=lambda x: (x['eleicao'], x['codigo_ibge'], x['data_eleicao']))


def transicoes_afetadas(eventos):
    return {(r['codigo_ibge'], t) for r in eventos for t in [r['eleicao'], r['eleicao']+4]
        if t in (2012, 2016, 2020)}


def gravar_csv(caminho, linhas):
    with caminho.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)


def main():
    SAIDA.mkdir(exist_ok=True, parents=True)
    publicacao = RAIZ / 'docs/publicacao'
    publicacao.mkdir(exist_ok=True)
    mapa = {normalizar(m['nome']): str(m['id']) for m in json.loads((RAIZ / 'dados/brutos/ibge/municipios_sp.json').read_text(encoding='utf-8'))}
    mapa['EMBU'] = mapa[normalizar('Embu das Artes')]
    mapa[normalizar('São Luís do Paraitinga')] = mapa[normalizar('São Luiz do Paraitinga')]
    eventos, suspeitos, reeleitos = [], set(), []
    def examinar(linhas, ano):
        for r in linhas:
            if r['DS_CARGO']=='PREFEITO' and 'SUPLEMENTAR' not in r['NM_TIPO_ELEICAO']:
                codigo=mapa.get(normalizar(r['NM_UE']))
                if codigo and codigo!='3550308':
                    if r.get('DS_DETALHE_SITUACAO_CAND') in ('CASSADO','CASSADO COM RECURSO','CANCELADO'):
                        suspeitos.add((ano,codigo))
                    if ano==2016 and r['DS_SIT_TOT_TURNO']=='ELEITO' and r.get('ST_REELEICAO')=='S':
                        reeleitos.append(codigo)
            yield r
    for ano in (2008, 2012, 2016, 2020):
        with (RAIZ / f'dados/brutos/tse/{ano}/consulta_cand_{ano}_SP.csv').open(encoding='cp1252', newline='') as f:
            eventos.extend(contar_eventos(examinar(csv.DictReader(f, delimiter=';'),ano), ano, mapa))
    gravar_csv(publicacao / 'eventos_suplementares.csv', eventos)
    con = duckdb.connect()
    con.execute("SET memory_limit='700MB'; SET threads=2; SET enable_progress_bar=false")
    con.execute('CREATE TABLE eventos (eleicao INT, codigo_ibge VARCHAR)')
    con.executemany('INSERT INTO eventos VALUES (?,?)', sorted({(r['eleicao'], r['codigo_ibge']) for r in eventos}))
    con.execute('CREATE TABLE suspeitos (eleicao INT, codigo_ibge VARCHAR)')
    con.executemany('INSERT INTO suspeitos VALUES (?,?)',sorted(suspeitos))
    con.execute('CREATE TABLE reeleitos_2016 (codigo_ibge VARCHAR)')
    con.executemany('INSERT INTO reeleitos_2016 VALUES (?)',[(c,) for c in sorted(set(reeleitos))])
    con.execute(f"CREATE VIEW original AS SELECT * FROM '{LIMPOS}/permanencia.parquet'")
    con.execute(f"CREATE VIEW mandatos AS SELECT * FROM '{LIMPOS}/mandatos.parquet'")
    con.execute(f"CREATE VIEW transicoes AS SELECT * FROM '{LIMPOS}/transicoes.parquet'")
    con.execute(f"CREATE VIEW correcoes AS SELECT * FROM read_csv('{publicacao}/correcoes_identidade.csv', all_varchar=true)")
    # Medidas de alcance da rede permanecem estaduais. Para exposição partidária,
    # só entram clientes cujo mandato anterior tem identidade partidária estável
    # segundo todos os eventos observados (não o mandato inteiro comprovado).
    con.execute(f"""CREATE TABLE clientes_seguros AS SELECT a.eleicao, a.raiz, m.partido_inicio AS partido, count(*) AS n
        FROM '{LIMPOS}/arestas_mandato.parquet' a JOIN mandatos m USING(eleicao,codigo_ibge)
        WHERE m.partido_inicio IS NOT NULL AND m.n_suplementares=0
        AND NOT EXISTS (SELECT 1 FROM eventos e WHERE e.eleicao=a.eleicao AND e.codigo_ibge=a.codigo_ibge)
        AND NOT EXISTS (SELECT 1 FROM suspeitos e WHERE e.eleicao=a.eleicao AND e.codigo_ibge=a.codigo_ibge)
        AND NOT EXISTS (SELECT 1 FROM original p JOIN reeleitos_2016 r USING(codigo_ibge)
            WHERE p.eleicao_transicao=2016 AND NOT p.mesmo_prefeito AND a.eleicao=2012 AND a.codigo_ibge=p.codigo_ibge)
        GROUP BY ALL""")
    con.execute("""CREATE TABLE auditada AS SELECT p.* REPLACE (
        coalesce(c.mesmo_prefeito_corrigido::BOOLEAN,p.mesmo_prefeito) AS mesmo_prefeito,
        coalesce(novo.n,0)>0 AS atende_partido_novo,
        coalesce(antigo.n,0)-1>0 AS atende_partido_antigo)
        FROM original p LEFT JOIN correcoes c ON p.codigo_ibge=c.codigo_ibge
            AND p.eleicao_transicao=c.eleicao_transicao::INT
        LEFT JOIN clientes_seguros novo ON novo.eleicao=p.eleicao AND novo.raiz=p.raiz AND novo.partido=p.partido_depois
        LEFT JOIN clientes_seguros antigo ON antigo.eleicao=p.eleicao AND antigo.raiz=p.raiz AND antigo.partido=p.partido_antes
        WHERE p.mandatos_inteiros AND p.alternancia IS NOT NULL
        AND NOT EXISTS (SELECT 1 FROM eventos e WHERE e.codigo_ibge=p.codigo_ibge
            AND e.eleicao IN (p.eleicao,p.eleicao_transicao))""")
    # Na ausência de alternância, o município focal também pertence ao partido
    # novo: deve sair da contagem de clientes externos, assim como do antigo.
    con.execute("""UPDATE auditada SET atende_partido_novo = coalesce(n.n,0)-1>0
        FROM clientes_seguros n WHERE NOT auditada.alternancia
        AND auditada.partido_antes=auditada.partido_depois
        AND n.eleicao=auditada.eleicao AND n.raiz=auditada.raiz AND n.partido=auditada.partido_depois""")
    # Capturar explicitamente a incerteza observável, sem inferir posse a partir
    # de um status eleitoral retrospectivo. A referência intermediária é mantida.
    con.execute("""CREATE TABLE transicoes_suspeitas AS SELECT DISTINCT p.codigo_ibge,p.eleicao_transicao,
        CASE WHEN EXISTS (SELECT 1 FROM suspeitos s WHERE s.codigo_ibge=p.codigo_ibge
            AND s.eleicao IN (p.eleicao,p.eleicao_transicao)) THEN 'candidatura_cassada_ou_cancelada'
            ELSE 'reeleicao_2016_inconsistente' END AS motivo
        FROM auditada p WHERE EXISTS (SELECT 1 FROM suspeitos s WHERE s.codigo_ibge=p.codigo_ibge
            AND s.eleicao IN (p.eleicao,p.eleicao_transicao))
        OR (p.eleicao_transicao=2016 AND NOT p.mesmo_prefeito
            AND p.codigo_ibge IN (SELECT codigo_ibge FROM reeleitos_2016))""")
    con.execute(f"COPY (SELECT * FROM auditada ORDER BY eleicao_transicao,codigo_ibge,raiz) TO '{SAIDA}/permanencia_intermediaria.parquet'")
    con.execute("""CREATE TABLE identidade_excluida AS SELECT t.codigo_ibge,t.eleicao_transicao,t.motivo,
        count(*) AS arestas FROM transicoes_suspeitas t JOIN auditada USING(codigo_ibge,eleicao_transicao) GROUP BY ALL""")
    con.execute("""DELETE FROM auditada p WHERE EXISTS (SELECT 1 FROM transicoes_suspeitas s
        WHERE s.codigo_ibge=p.codigo_ibge AND s.eleicao_transicao=p.eleicao_transicao)""")
    con.execute(f"""CREATE TABLE clientes_ambiguos AS SELECT DISTINCT a.eleicao,a.raiz
        FROM '{LIMPOS}/arestas_mandato.parquet' a LEFT JOIN mandatos m USING(eleicao,codigo_ibge)
        WHERE m.partido_inicio IS NULL OR m.n_suplementares>0
        OR EXISTS (SELECT 1 FROM eventos e WHERE e.eleicao=a.eleicao AND e.codigo_ibge=a.codigo_ibge)
        OR EXISTS (SELECT 1 FROM suspeitos e WHERE e.eleicao=a.eleicao AND e.codigo_ibge=a.codigo_ibge)
        OR EXISTS (SELECT 1 FROM transicoes_suspeitas s WHERE s.motivo='reeleicao_2016_inconsistente'
            AND s.codigo_ibge=a.codigo_ibge AND a.eleicao=2012)""")
    def registros(sql):
        r = con.execute(sql)
        return [dict(zip([d[0] for d in r.description], row)) for row in r.fetchall()]
    removidas = registros("""SELECT p.codigo_ibge,t.municipio,p.eleicao_transicao,count(*) AS arestas
        FROM original p JOIN transicoes t ON t.codigo_ibge=p.codigo_ibge AND t.eleicao=p.eleicao_transicao
        WHERE p.mandatos_inteiros AND p.alternancia IS NOT NULL
        AND EXISTS (SELECT 1 FROM eventos e WHERE e.codigo_ibge=p.codigo_ibge AND e.eleicao IN (p.eleicao,p.eleicao_transicao))
        GROUP BY ALL ORDER BY 1,3""")
    if removidas:
        gravar_csv(publicacao / 'transicoes_excluidas_adicionais.csv', removidas)
    resumo = registros("""SELECT eleicao_transicao,count(*) AS n,count(DISTINCT codigo_ibge) AS municipios,
        count(DISTINCT raiz) AS fornecedores,avg(continua::INT)*100 AS continua_pct
        FROM auditada GROUP BY ALL ORDER BY 1""")
    exposicoes = registros("""SELECT count(*) AS n,
        count(*) FILTER (a.atende_partido_novo<>p.atende_partido_novo) AS novo_reclassificadas,
        count(*) FILTER (a.atende_partido_antigo<>p.atende_partido_antigo) AS antigo_reclassificadas
        FROM auditada a JOIN original p USING(codigo_ibge,raiz,eleicao_transicao)
        WHERE a.alternancia AND a.n_clientes>=2""")
    total = registros("""SELECT count(*) AS n,count(DISTINCT codigo_ibge) AS municipios,
        count(DISTINCT raiz) AS fornecedores FROM auditada""")[0]
    municipios_fora=registros("""SELECT codigo_ibge,min(municipio) AS municipio
        FROM transicoes t WHERE NOT EXISTS
        (SELECT 1 FROM auditada a WHERE a.codigo_ibge=t.codigo_ibge) GROUP BY 1 ORDER BY 1""")
    gravar_csv(publicacao/'municipios_sem_transicao.csv',municipios_fora)
    identidade=registros('SELECT * FROM identidade_excluida ORDER BY 1,2')
    gravar_csv(publicacao/'transicoes_identidade_suspeita.csv',identidade)
    gravar_csv(publicacao/'mandatos_identidade_duvidosa.csv',
        [dict(eleicao=e,codigo_ibge=c) for e,c in sorted(suspeitos)])
    destino = SAIDA / 'permanencia_auditada.parquet'
    anual_sql = ' UNION ALL '.join(f"SELECT {a} AS ano,codigo_ibge,left(cnpj,8) AS raiz FROM '{LIMPOS}/rede_{a}.parquet'"
        for a in (2014,2015,2016,2018,2019,2020,2022,2023,2024))
    con.execute('CREATE TABLE anos_posteriores AS SELECT DISTINCT * FROM ('+anual_sql+')')
    con.execute(f"""COPY (SELECT p.*, EXISTS (SELECT 1 FROM clientes_ambiguos c WHERE c.raiz=p.raiz
        AND c.eleicao=p.eleicao) AS cliente_ambiguo, EXISTS (SELECT 1 FROM anos_posteriores a
        WHERE a.codigo_ibge=p.codigo_ibge AND a.raiz=p.raiz
        AND a.ano BETWEEN p.eleicao_transicao+2 AND p.eleicao_transicao+4) AS continua_anos2a4
        FROM auditada p ORDER BY eleicao_transicao,codigo_ibge,raiz) TO '{destino}'""")
    sha = hashlib.sha256(destino.read_bytes()).hexdigest()
    payload = dict(eventos=len(eventos), mandatos_com_evento=len({(r['eleicao'],r['codigo_ibge']) for r in eventos}),
        total=total, resumo=resumo, removidas=removidas, exposicoes=exposicoes,
        filtro_identidade_conservador=True,identidade_excluida=identidade,
        identidade_excluida_arestas=sum(r['arestas'] for r in identidade),
        municipios_sem_transicao=municipios_fora,
        sha256_arquivo=sha, fonte='Parquets legados + todas as candidaturas TSE locais')
    (SAIDA / 'preparacao_resumo.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    (publicacao / 'amostra-auditada.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(payload, ensure_ascii=False, indent=2), flush=True)
    con.close()


if __name__ == '__main__':
    main()
