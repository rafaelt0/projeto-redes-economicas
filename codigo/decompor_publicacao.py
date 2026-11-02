"""Decomposições retrospectivas; preserva os relatórios e Parquets legados.

Uso: .venv/bin/python -I codigo/decompor_publicacao.py
Saídas: dados/limpos/publicacao/decomposicao_*.{json,csv,npz}, relatório em docs/.
"""
import os
os.environ["OPENBLAS_NUM_THREADS"] = "2"
import csv
import hashlib
import json
from pathlib import Path

import duckdb
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "dados/limpos/publicacao"
DESTINOS = ["continua", "perdeu_cliente_segue_na_rede", "saiu_da_rede_baixada", "saiu_da_rede_ativa"]
REPLICAS = 1999


def mantel_haenszel(n, k):
    """n: estrato × grupo; k: estrato × grupo × resultado. Grupo 1 menos 0."""
    ok = (n[:, 0] > 0) & (n[:, 1] > 0)
    if not ok.any():
        return np.full(k.shape[-1], np.nan)
    n, k = n[ok], k[ok]
    peso = n[:, 0] * n[:, 1] / n.sum(axis=1)
    dif = k[:, 1] / n[:, 1, None] - k[:, 0] / n[:, 0, None]
    return (peso[:, None] * dif).sum(axis=0) / peso.sum()


def bootstrap(n, k, replicas=REPLICAS, semente=2026):
    """Município × estrato × grupo [× resultado]; sorteios comuns aos destinos."""
    rng = np.random.default_rng(semente)
    m = n.shape[0]
    saida = []
    for inicio in range(0, replicas, 32):
        sorteio = rng.multinomial(m, np.full(m, 1/m), size=min(32, replicas-inicio)).astype(float)
        ns = (sorteio @ n.reshape(m, -1)).reshape(-1, *n.shape[1:])
        ks = (sorteio @ k.reshape(m, -1)).reshape(-1, *k.shape[1:])
        saida.extend(mantel_haenszel(a, b) for a, b in zip(ns, ks))
    return np.asarray(saida)


def _celulas(con, filtro, grupo, resultados):
    """Contagens município × estrato × grupo para os resultados pedidos."""
    ys = ", ".join(f"sum(({expr})::INT)::DOUBLE AS y{i}" for i, (_, expr) in enumerate(resultados))
    linhas = con.execute(f"""SELECT codigo_ibge, concat_ws('|', coalesce(faixa_clientes, '??'),
        coalesce(setor, '??'), eleicao_transicao) AS estrato, ({grupo})::INT AS grupo,
        count(*)::DOUBLE, {ys} FROM base WHERE {filtro} GROUP BY ALL ORDER BY 1, 2, 3""").fetchall()
    municipios = sorted({r[0] for r in linhas})
    estratos = sorted({r[1] for r in linhas})
    mi, ei = {v: i for i, v in enumerate(municipios)}, {v: i for i, v in enumerate(estratos)}
    n = np.zeros((len(mi), len(ei), 2))
    k = np.zeros((*n.shape, len(resultados)))
    for mun, est, g, total, *y in linhas:
        n[mi[mun], ei[est], g] = total
        k[mi[mun], ei[est], g] = y
    return n, k


def _pesos_mh(total):
    """Pesos dos estratos com os dois grupos; fora disso, zero."""
    ok = (total[:, 0] > 0) & (total[:, 1] > 0)
    peso = np.zeros(len(total))
    peso[ok] = total[ok, 0] * total[ok, 1] / total[ok].sum(axis=1)
    return ok, peso


def condicional_estratos(n, k):
    """Condiciona as taxas padronizadas MH e decompõe seu contraste.

    Saída: três valores por destino não contínuo (parcela no grupo 0, no
    grupo 1 e diferença), seguidos de nível/composição por destino. A mesma
    população padronizada entra nas razões e na identidade de ponto médio;
    não se excluem estratos em função de seus desfechos.
    """
    total, kt = (n.sum(axis=0), k.sum(axis=0)) if n.ndim == 3 else (n, k)
    ok, peso = _pesos_mh(total)
    if not ok.any():
        return np.full(5*(len(DESTINOS)-1), np.nan)
    taxas = (peso[ok, None, None] * kt[ok] / total[ok, :, None]).sum(axis=0) / peso.sum()
    c0, c1 = taxas[:, 0]
    nao = 1 - taxas[:, 0]
    valores, componentes = [], []
    for j in range(1, len(DESTINOS)):
        sh0, sh1 = np.divide(taxas[:, j], nao, out=np.full(2, np.nan), where=nao > 0)
        valores.extend([sh0, sh1, sh1-sh0])
        componentes.extend([(c0-c1)*(sh0+sh1)/2,
                            (sh1-sh0)*(1-(c0+c1)/2)])
    return np.asarray(valores + componentes)


def bootstrap_condicional(n, k, replicas=REPLICAS, semente=2026):
    """Reamostragem municipal conjunta para as parcelas condicionais."""
    rng = np.random.default_rng(semente)
    m = n.shape[0]
    saida = []
    for inicio in range(0, replicas, 32):
        sorteio = rng.multinomial(m, np.full(m, 1/m), size=min(32, replicas-inicio)).astype(float)
        ns = (sorteio @ n.reshape(m, -1)).reshape(-1, *n.shape[1:])
        ks = (sorteio @ k.reshape(m, -1)).reshape(-1, *k.shape[1:])
        saida.extend(condicional_estratos(a, b) for a, b in zip(ns, ks))
    return np.asarray(saida)


def resumir_condicional(con, nome, filtro, grupo, replicas=REPLICAS):
    """Tabela dos destinos condicionais e da decomposição nível/composição."""
    destinos = [(d, f"destino='{d}'") for d in DESTINOS]
    n, k = _celulas(con, filtro, grupo, destinos)
    estimativa = condicional_estratos(n, k)
    bs = bootstrap_condicional(n, k, replicas=replicas)
    total = n.sum(axis=0)
    suporte, _ = _pesos_mh(total)
    saida = []
    for j, (destino, _) in enumerate(destinos[1:], 1):
        sh0, sh1, dif = estimativa[3*(j-1):3*(j-1)+3]
        nivel, composicao = estimativa[3*(len(destinos)-1)+2*(j-1):3*(len(destinos)-1)+2*(j-1)+2]
        def intervalo(v):
            low, high = np.quantile(v[np.isfinite(v)], [.025, .975])
            return float(100*low), float(100*high)
        ic_dif, ic_nivel, ic_comp = intervalo(bs[:, 3*(j-1)+2]), intervalo(bs[:, 3*(len(destinos)-1)+2*(j-1)]), intervalo(bs[:, 3*(len(destinos)-1)+2*(j-1)+1])
        saida.append(dict(analise=nome, destino=destino,
            parcela_grupo0_pct=float(100*sh0), parcela_grupo1_pct=float(100*sh1),
            diferenca_pp=float(100*dif), diferenca_ic95_inf_pp=ic_dif[0], diferenca_ic95_sup_pp=ic_dif[1],
            nivel_pp=float(100*nivel), nivel_ic95_inf_pp=ic_nivel[0], nivel_ic95_sup_pp=ic_nivel[1],
            composicao_pp=float(100*composicao), composicao_ic95_inf_pp=ic_comp[0],
            composicao_ic95_sup_pp=ic_comp[1], municipios=int(n.shape[0]),
            estratos=int(suporte.sum()), suporte=int(total[suporte].sum()), replicas=int(np.isfinite(bs[:, 0]).sum())))
    return saida


def resumir_bruta(con, nome, filtro, grupo):
    """Parcelas condicionais brutas, sem padronização por estratos."""
    r = con.execute(f"""SELECT ({grupo})::INT AS grupo, count(*)::BIGINT AS n,
        sum((NOT continua)::INT) AS nao_continua,
        sum((destino='perdeu_cliente_segue_na_rede')::INT) AS segue
        FROM base WHERE {filtro} GROUP BY 1 ORDER BY 1""")
    colunas = [d[0] for d in r.description]
    saida = []
    for linha in r.fetchall():
        d = dict(zip(colunas, linha))
        d.update(analise=nome, parcela_cond_pct=100*d['segue']/d['nao_continua'] if d['nao_continua'] else None)
        saida.append(d)
    return saida


def resumir_portfolio(con, nome, filtro, grupo):
    """Parcelas condicionais brutas por tamanho da carteira anterior."""
    r = con.execute(f"""SELECT CASE WHEN n_clientes=1 THEN '1' ELSE '2+' END AS carteira,
        ({grupo})::INT AS grupo, count(*)::BIGINT AS n,
        sum((NOT continua)::INT) AS nao_continua,
        sum((destino='perdeu_cliente_segue_na_rede')::INT) AS segue
        FROM base WHERE {filtro} GROUP BY 1, 2 ORDER BY 1, 2""")
    colunas = [d[0] for d in r.description]
    saida = []
    for linha in r.fetchall():
        d = dict(zip(colunas, linha))
        d.update(analise=nome, parcela_cond_pct=100*d['segue']/d['nao_continua'] if d['nao_continua'] else None)
        saida.append(d)
    return saida


def resumir(con, nome, filtro, grupo, resultados, replicas=REPLICAS):
    """Constrói células do estimando a partir de linhas; sem imputar estratos."""
    n, k = _celulas(con, filtro, grupo, resultados)
    total = n.sum(axis=0)
    suporte = (total[:, 0] > 0) & (total[:, 1] > 0)
    estimativa = mantel_haenszel(total, k.sum(axis=0))
    bs = bootstrap(n, k, replicas=replicas)
    np.savez_compressed(SAIDA / f"decomposicao_boot_{nome}.npz", replicas=bs, estimativa=estimativa)
    print(nome, np.round(100*estimativa, 4), flush=True)
    saida = []
    for j, (resultado, _) in enumerate(resultados):
        validas = np.isfinite(bs[:, j])
        low, high = np.quantile(bs[validas, j], [.025, .975])
        saida.append(dict(analise=nome, resultado=resultado, estimativa_pp=float(100*estimativa[j]),
            ic95_inf_pp=float(100*low), ic95_sup_pp=float(100*high), n=int(n.sum()),
            n1=int(total[:, 1].sum()), n0=int(total[:, 0].sum()), municipios=int(n.shape[0]),
            suporte=int(total[suporte].sum()), estratos=int(suporte.sum()), replicas=int(validas.sum())))
    return saida


def main():
    SAIDA.mkdir(exist_ok=True, parents=True)
    sha=hashlib.sha256((SAIDA/'permanencia_auditada.parquet').read_bytes()).hexdigest()
    if sha!=json.loads((SAIDA/'preparacao_resumo.json').read_text(encoding='utf-8'))['sha256_arquivo']:
        raise ValueError('Amostra diverge da preparação auditada')
    con = duckdb.connect()
    con.execute("SET memory_limit='700MB'; SET threads=2; SET enable_progress_bar=false")
    con.execute(f"CREATE TABLE p AS SELECT * FROM '{SAIDA}/permanencia_auditada.parquet'")
    # Só a existência anual da raiz na prefeitura, sem somar linhas de filiais.
    con.execute(f"""CREATE TABLE anual AS SELECT DISTINCT
        regexp_extract(filename, 'rede_(\\d{{4}})\\.parquet', 1)::INT AS ano,
        codigo_ibge, left(cnpj,8) AS raiz
        FROM read_parquet('{RAIZ}/dados/limpos/rede_*.parquet', filename=true)""")
    con.execute("""CREATE TABLE base AS SELECT p.*,
        NOT mesmo_prefeito AND partido_antes=partido_depois AS troca_so_prefeito,
        mesmo_prefeito AND partido_antes<>partido_depois AS troca_so_partido,
        CASE WHEN NOT mesmo_prefeito AND partido_antes<>partido_depois THEN 'muda_ambos'
          WHEN NOT mesmo_prefeito THEN 'muda_prefeito'
          WHEN partido_antes<>partido_depois THEN 'muda_partido' ELSE 'mantem_ambos' END AS categoria,
        a.raiz IS NOT NULL AS ultimo_ano, b.raiz IS NOT NULL AS primeiro_ano
        FROM p LEFT JOIN anual a ON a.codigo_ibge=p.codigo_ibge AND a.raiz=p.raiz
            AND a.ano=p.eleicao_transicao
        LEFT JOIN anual b ON b.codigo_ibge=p.codigo_ibge AND b.raiz=p.raiz
            AND b.ano=p.eleicao_transicao+1""")
    def registros(sql):
        r = con.execute(sql)
        return [dict(zip([d[0] for d in r.description], linha)) for linha in r.fetchall()]
    descritivas = registros("""SELECT categoria, count(*) AS n, count(DISTINCT codigo_ibge) AS municipios,
        count(DISTINCT (codigo_ibge,eleicao_transicao)) AS municipio_eleicoes,
        avg(continua::INT)*100 AS continua_pct, avg(ultimo_ano::INT)*100 AS ultimo_ano_pct,
        avg(primeiro_ano::INT)*100 AS primeiro_ano_pct FROM base GROUP BY ALL ORDER BY 1""")
    temporal = registros("""SELECT eleicao_transicao, alternancia, ultimo_ano, count(*) AS n,
        avg(continua::INT)*100 AS continua_pct, avg(primeiro_ano::INT)*100 AS primeiro_ano_pct
        FROM base GROUP BY ALL ORDER BY 1,2,3""")
    destinos = [(d, f"destino='{d}'") for d in DESTINOS]
    resultado = resumir(con, "alternancia_destinos", "true", "alternancia", destinos)
    janela = [("qualquer_ano_seguinte", "continua"), ("primeiro_ano_seguinte", "primeiro_ano"),
        ("anos2a4_seguinte", "continua_anos2a4")]
    resultado += resumir(con, "alternancia_ultimo_ano", "ultimo_ano", "alternancia", janela)
    resultado += resumir(con, "sucessao_partido", "NOT mesmo_prefeito", "partido_antes<>partido_depois", destinos)
    resultado += resumir(con, "prefeito_mesmo_partido", "partido_antes=partido_depois", "NOT mesmo_prefeito", destinos)
    resultado += resumir(con, "partido_mesmo_prefeito", "mesmo_prefeito", "partido_antes<>partido_depois", destinos)
    # Suporte comum observado: só fornecedores com um dos dois vínculos.
    politica = "alternancia AND n_clientes>=2 AND atende_partido_novo<>atende_partido_antigo"
    resultado += resumir(con, "apenas_novo_menos_apenas_antigo", politica, "atende_partido_novo", destinos)
    condicionais = resumir_condicional(con, "alternancia_destinos", "true", "alternancia")
    condicionais += resumir_condicional(con, "sucessao_partido", "NOT mesmo_prefeito", "partido_antes<>partido_depois")
    brutas = resumir_bruta(con, "alternancia_destinos", "true", "alternancia")
    brutas += resumir_bruta(con, "sucessao_partido", "NOT mesmo_prefeito", "partido_antes<>partido_depois")
    portfolio = resumir_portfolio(con, "alternancia_destinos", "true", "alternancia")
    payload = dict(replicas=REPLICAS, semente=2026, sha256_fonte=sha, correcao_identidade="São João da Boa Vista/2016",
        amostra="permanencia_auditada.parquet (filtro conservador de identidade, suplementares registradas e vínculos externos elegíveis)",
        descritivas=descritivas, temporal=temporal, resultados=resultado,
        condicionais=condicionais, condicionais_brutas=brutas, portfolio=portfolio)
    (SAIDA / "decomposicao_resultados.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding='utf-8', newline='\n')
    with (SAIDA / "decomposicao_resultados.csv").open("w", encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(resultado[0])); w.writeheader(); w.writerows(resultado)
    with (SAIDA / "decomposicao_condicionais.csv").open("w", encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(condicionais[0])); w.writeheader(); w.writerows(condicionais)
    texto = ["# Decomposição e janela temporal — resultados retrospectivos\n",
        "Gerado por `codigo/decompor_publicacao.py`; protocolo em `docs/protocolo-publicacao.md`. "
        "Diferenças em pontos percentuais. IC percentil de 95%, 1.999 reamostragens municipais. "
        "Os destinos são mutuamente exclusivos, sem condicionamento em sobreviver na rede. "
        "O bootstrap municipal não resolve toda dependência por fornecedor compartilhado. "
        "O modelo de painel complementa esta inferência com agrupamento por município e fornecedor.\n",
        "## Contrastes ajustados\n",
        "| Análise | Resultado | Diferença pp | IC95 | N | Suporte | Municípios |\n"
        "|---|---|---:|---|---:|---:|---:|"]
    for r in resultado:
        texto.append(f"| {r['analise']} | {r['resultado']} | {r['estimativa_pp']:.3f} | "
            f"{r['ic95_inf_pp']:.3f}; {r['ic95_sup_pp']:.3f} | {r['n']} | {r['suporte']} | {r['municipios']} |")
    texto += ["\n## Destinos condicionais entre quem não continua\n",
        "Para cada contraste, a parcela de cada destino é calculada apenas entre as arestas que não "
        "continuam na mesma prefeitura, com os mesmos estratos e pesos. As parcelas dos três destinos "
        "não contínuos somam 100% em cada grupo. A coluna de diferença é grupo 1 menos grupo 0. "
        "A decomposição da diferença na taxa de `perdeu_cliente_segue_na_rede` separa o componente de "
        "nível (mais quebras no grupo 1) do componente de composição (destinos diferentes entre quem quebra); "
        "a soma reproduz exatamente a diferença padronizada do destino no mesmo suporte MH. "
        "As parcelas condicionais são razões de taxas padronizadas, não médias de contagens ou de razões por estrato.\n",
        "| Análise | Destino | Parcela grupo 0 | Parcela grupo 1 | Diferença pp | IC95 | Nível pp | Composição pp |\n"
        "|---|---|---:|---:|---:|---|---:|---:|"]
    for r in condicionais:
        texto.append(f"| {r['analise']} | {r['destino']} | {r['parcela_grupo0_pct']:.2f}% | "
            f"{r['parcela_grupo1_pct']:.2f}% | {r['diferenca_pp']:.2f} | "
            f"{r['diferenca_ic95_inf_pp']:.2f}; {r['diferenca_ic95_sup_pp']:.2f} | "
            f"{r['nivel_pp']:.2f} [{r['nivel_ic95_inf_pp']:.2f}; {r['nivel_ic95_sup_pp']:.2f}] | "
            f"{r['composicao_pp']:.2f} [{r['composicao_ic95_inf_pp']:.2f}; {r['composicao_ic95_sup_pp']:.2f}] |")
    texto += ["\nParcelas brutas, sem padronização, para conferência direta com a tabela de destinos:\n",
        "| Análise | Grupo | Não continuam | Seguem na rede | Parcela condicional |\n"
        "|---|---|---:|---:|---:|"]
    for r in brutas:
        grupo = "Alternância" if r['grupo'] == 1 else "Demais"
        texto.append(f"| {r['analise']} | {grupo} | {r['nao_continua']} | {r['segue']} | "
            f"{r['parcela_cond_pct']:.2f}% |")
    texto += ["\nParcelas condicionais por tamanho da carteira anterior:\n",
        "| Carteira | Grupo | Não continuam | Seguem na rede | Parcela condicional |\n"
        "|---|---|---:|---:|---:|"]
    for r in portfolio:
        grupo = "Alternância" if r['grupo'] == 1 else "Demais"
        texto.append(f"| {r['carteira']} cliente(s) | {grupo} | {r['nao_continua']} | {r['segue']} | "
            f"{r['parcela_cond_pct']:.2f}% |")
    texto += ["\n## Definições e limites\n",
        "Estratos: faixa de clientes × divisão CNAE × transição, pesos n1*n0/(n1+n0). "
        "Comparações políticas são de categorias observadas, não tratamentos aleatórios. "
        "Sucessão_partido compara partidos diferentes vs iguais apenas quando muda o prefeito; "
        "prefeito_mesmo_partido compara sucessão vs permanência do prefeito quando o partido se mantém; "
        "partido_mesmo_prefeito compara mudança de legenda vs manutenção quando o prefeito permanece. "
        "Os destinos de cada contraste usam o mesmo suporte e somam zero. "
        "Último_ano restringe o risco a fornecedores com despesa no ano da eleição; "
        "primeiro_ano significa presença no ano seguinte. "
        "Novo versus antigo compara diretamente vínculos exclusivos, com suporte próprio. "
        "Não identifica equivalência nem efeito causal. Correção auditada: São João da Boa Vista/2016 "
        "é continuidade do prefeito e partido, apesar de título ocultado no TSE. "
        "Suplementares detectadas em todas as candidaturas (incluindo eventos sem vencedor registrado) "
        "excluem ambas as transições adjacentes. Vínculos partidários usam somente clientes externos "
        "sem suplementar registrada no mandato anterior. A amostra única está em permanencia_auditada.parquet. "
        "Nenhum arquivo legado foi sobrescrito.\n"]
    (RAIZ / "docs/resultados-decomposicao.md").write_text("\n".join(texto)+"\n", encoding='utf-8', newline='\n')
    con.close()


if __name__ == "__main__":
    main()
