"""Modelos observacionais de continuidade; execute da raiz com Python da .venv.

Lê somente dados/limpos/publicacao/permanencia_auditada.parquet (preparar_publicacao.py).
Absorção por projeções alternadas. A covariância agrupa por município e raiz,
incluindo correção de interseção e correções de amostra finita. Não infere causa.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '2')
os.environ.setdefault('OMP_NUM_THREADS', '2')

import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import LinearOperator, cg
from scipy.stats import norm, t as student
import duckdb

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / 'dados/limpos/publicacao'


class NaoIdentificado(ValueError):
    """O desfecho é constante dentro dos efeitos fixos: não resta variação para estimar."""


def codificar(a):
    _, inv = np.unique(a, return_inverse=True)
    return inv.astype(np.int32)


def posto_dois_efeitos(a, b):
    """Posto exato das dummies de dois efeitos: níveis menos componentes."""
    a, b = codificar(a), codificar(b)
    na, nb = int(a.max()) + 1, int(b.max()) + 1
    graph = coo_matrix((np.ones(len(a), dtype=np.int8), (a, b + na)),
                       shape=(na + nb, na + nb)).tocsr()
    componentes = connected_components(graph, directed=False, return_labels=False)
    return na + nb - componentes


def descartar_singletons(grupos):
    """Máscara das linhas que restam após remover níveis de efeito fixo com uma só linha.

    Uma linha sozinha em algum nível é ajustada exatamente pela própria dummy:
    não altera os coeficientes nem os escores da covariância, só os graus de liberdade.
    """
    manter = np.ones(len(grupos[0]), dtype=bool)
    mudou = True
    while mudou:
        mudou = False
        for g in grupos:
            cont = np.bincount(g[manter], minlength=int(g.max()) + 1)
            ruim = manter & (cont[g] < 2)
            if ruim.any():
                manter &= ~ruim
                mudou = True
    return manter


def absorver(v, efeitos, tol=1e-10, max_iter=1000):
    """Retorna resíduo, iterações e maior média de grupo relativa à escala."""
    v = np.array(v, dtype=float, copy=True)
    efeitos = [codificar(g) for g in efeitos]
    contagens = [np.bincount(g) for g in efeitos]
    escala = max(1., np.max(np.abs(v)))
    if len(efeitos) == 2:
        # Elimina primeiro o efeito de alta cardinalidade e resolve a equação
        # normal do primeiro efeito por gradientes conjugados. A matriz nunca
        # é materializada; a solução residual é única mesmo com componentes
        # desconexos e normalizações arbitrárias dos efeitos.
        a, b = efeitos
        ca, cb = contagens
        def sem_b(z):
            return z - (np.bincount(b, weights=z) / cb)[b]
        def matvec(z):
            return np.bincount(a, weights=sem_b(z[a]), minlength=len(ca))
        operador = LinearOperator((len(ca), len(ca)), matvec=matvec, dtype=float)
        maior_it = 0
        for j in range(v.shape[1]):
            z = sem_b(v[:, j])
            rhs = np.bincount(a, weights=z, minlength=len(ca))
            cont = [0]
            def contar(_):
                cont[0] += 1
            alpha, status = cg(operador, rhs, rtol=tol * .01, atol=tol * .01,
                               maxiter=max_iter, callback=contar)
            if status != 0:
                raise RuntimeError(f'Gradientes conjugados não convergiram: {status}')
            v[:, j] = sem_b(z - alpha[a])
            maior_it = max(maior_it, cont[0])
        erro = max(float(np.max(np.abs(np.bincount(g, weights=v[:, j]) / count)))
                   for g, count in zip(efeitos, contagens) for j in range(v.shape[1])) / escala
        if erro > tol:
            raise RuntimeError(f'Resíduo de absorção acima da tolerância: {erro:g}')
        return v, maior_it, erro
    for it in range(1, max_iter + 1):
        maior = 0.
        for g, count in zip(efeitos, contagens):
            for j in range(v.shape[1]):
                media = np.bincount(g, weights=v[:, j]) / count
                maior = max(maior, float(np.max(np.abs(media))))
                v[:, j] -= media[g]
        if maior / escala < tol:
            return v, it, maior / escala
    raise RuntimeError(f'Absorção não convergiu em {max_iter} iterações: {maior / escala:g}')


def posto_fe(grupos):
    # Os efeitos adicionais podem ser aninhados ou redundantes. Somar níveis-1
    # é um limite superior, conservador para o fator de graus de liberdade.
    return posto_dois_efeitos(grupos[0], grupos[1]) + sum(len(np.unique(g)) - 1 for g in grupos[2:])


def covariancia(xr, resid, bread, aglomerados, n, posto, totais):
    """CGM em duas dimensões; cada componente usa o seu número de grupos `totais`."""
    k = xr.shape[1]
    meats = []
    for g, ng in zip(aglomerados, totais):
        if ng < 2:
            raise ValueError('Menos de dois clusters')
        scores = np.column_stack([np.bincount(g, weights=xr[:, j] * resid, minlength=int(g.max()) + 1)
                                  for j in range(k)])
        fator = ng / (ng - 1) * (n - 1) / (n - posto - k)
        meats.append(fator * scores.T @ scores)
    cov = bread @ (meats[0] + meats[1] - meats[2]) @ bread
    return (cov + cov.T) / 2


def estimar(y, x, efeitos, municipio, fornecedor, nomes):
    """MQO com efeitos absorvidos. Convenção principal: descarta níveis singleton e conta
    só o posto dos efeitos restantes. `cov_conservadora` repete a correção contando
    todas as linhas e níveis originais (convenção anterior, mais ampla)."""
    n_original, k = x.shape
    grupos_total = [codificar(g) for g in efeitos]
    m_total, f_total = codificar(municipio), codificar(fornecedor)
    inter_total = codificar(m_total.astype(np.int64) * (int(f_total.max()) + 1) + f_total)
    posto_total = posto_fe(grupos_total)
    totais_conservadores = [int(g.max()) + 1 for g in (m_total, f_total, inter_total)]
    if n_original <= posto_total + k:
        raise ValueError('Graus de liberdade insuficientes')
    manter = descartar_singletons(grupos_total)
    y, x = y[manter], x[manter]
    grupos = [codificar(g[manter]) for g in grupos_total]
    m, f = codificar(m_total[manter]), codificar(f_total[manter])
    inter = codificar(inter_total[manter])
    n = len(y)
    posto = posto_fe(grupos)
    if n <= posto + k:
        raise ValueError('Graus de liberdade insuficientes')
    w, it, erro = absorver(np.column_stack([y, x]), grupos)
    yr, xr = w[:, 0], w[:, 1:]
    if np.max(np.abs(yr)) < 1e-9:
        raise NaoIdentificado('Desfecho absorvido integralmente pelos efeitos fixos')
    xx = xr.T @ xr
    posto_x = int(np.linalg.matrix_rank(xx, tol=np.max(np.linalg.eigvalsh(xx)) * 1e-10))
    if posto_x < k:
        raise ValueError(f'Regressores colineares após absorção (posto {posto_x} de {k})')
    bread = np.linalg.inv(xx)
    beta = bread @ (xr.T @ yr)
    resid = yr - xr @ beta
    aglom = [m, f, inter]
    sizes = [int(g.max()) + 1 for g in aglom]
    cov = covariancia(xr, resid, bread, aglom, n, posto, sizes)
    cov_cons = covariancia(xr, resid, bread, aglom, n_original, posto_total, totais_conservadores)
    return {'nomes': nomes, 'beta': beta, 'cov': cov, 'cov_conservadora': cov_cons, 'n': n,
            'n_original': n_original, 'n_singletons_descartados': n_original - n,
            'clusters': sizes, 'clusters_conservadores': totais_conservadores,
            'gl_t': min(sizes[0], sizes[1]) - 1, 'posto_fe_limite': posto, 'posto_regressores': posto_x,
            'n_regressores': k, 'n_municipios': sizes[0], 'n_fornecedores': sizes[1],
            'posto_fe_limite_conservador': posto_total, 'iteracoes': it, 'erro_absorcao': erro,
            'autovalor_minimo_cov': float(np.linalg.eigvalsh(cov).min()),
            'autovalor_minimo_cov_conservadora': float(np.linalg.eigvalsh(cov_cons).min())}


def registrar(out, modelo, contrastes):
    linhas = []
    beta, gl = out['beta'], out['gl_t']
    crit = student.ppf(.975, gl)
    for nome, vetor in contrastes:
        v = np.asarray(vetor, dtype=float)
        estimativa = float(v @ beta)
        ep = {}
        for chave in ('cov', 'cov_conservadora'):
            variancia = float(v @ out[chave] @ v)
            ep[chave] = np.sqrt(variancia) if variancia >= 0 else np.nan
        erro = ep['cov']
        linhas.append({'modelo': modelo, 'contraste': nome, 'estimativa': estimativa,
                       'erro_padrao': float(erro), 'ic95_inferior': float(estimativa - crit * erro),
                       'ic95_superior': float(estimativa + crit * erro),
                       'p_t': float(2 * student.sf(abs(estimativa / erro), gl)) if erro > 0 else None,
                       'p_normal': float(2 * norm.sf(abs(estimativa / erro))) if erro > 0 else None,
                       'gl_t': gl, 'erro_padrao_conservador': float(ep['cov_conservadora']),
                       'p_t_conservador': float(2 * student.sf(abs(estimativa / ep['cov_conservadora']), gl))
                       if ep['cov_conservadora'] > 0 else None})
    return linhas


CAMPOS_OBRIGATORIOS = ('continua_anos2a4', 'cliente_ambiguo')


def validar_fonte(resumo, colunas):
    """Recusa uma fonte sem o filtro de identidade ou sem os campos exigidos (nada de detecção por palpite)."""
    if resumo.get('filtro_identidade_conservador') is not True:
        raise ValueError("preparacao_resumo.json não registra 'filtro_identidade_conservador': true")
    faltam = [c for c in CAMPOS_OBRIGATORIOS if c not in colunas]
    if faltam:
        raise ValueError(f'Campos ausentes em permanencia_auditada.parquet: {faltam}')


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    fonte = SAIDA / 'permanencia_auditada.parquet'
    sha = hashlib.sha256(fonte.read_bytes()).hexdigest()
    resumo = json.loads((SAIDA / 'preparacao_resumo.json').read_text(encoding='utf-8'))
    esperado = resumo['sha256_arquivo']
    if sha != esperado:
        raise ValueError('permanencia_auditada.parquet difere do registrado em preparacao_resumo.json')
    con = duckdb.connect()
    con.execute("SET memory_limit='700MB'; SET threads=2; SET enable_progress_bar=false")
    arquivo = str(fonte).replace("'", "''")
    con.execute(f"CREATE VIEW p AS SELECT * FROM read_parquet('{arquivo}')")
    colunas = {r[0] for r in con.execute('DESCRIBE p').fetchall()}
    validar_fonte(resumo, colunas)
    auditoria = {'sha256_fonte': sha}
    cursor = con.execute("""SELECT count(*) n, count(DISTINCT codigo_ibge) municipios,
        count(DISTINCT raiz) fornecedores, count(*) FILTER (WHERE setor IS NULL) setor_ausente,
        count(*) FILTER (WHERE mesmo_prefeito IS NULL OR partido_antes IS NULL OR partido_depois IS NULL
            OR alternancia IS NULL OR NOT mandatos_inteiros OR atende_partido_novo IS NULL
            OR atende_partido_antigo IS NULL) politica_ausente,
        count(*) FILTER (WHERE valor <= 0 OR valor IS NULL) valor_nao_positivo_ou_ausente,
        count(*) - count(DISTINCT (codigo_ibge, raiz, eleicao_transicao)) chaves_duplicadas,
        count(*) FILTER (WHERE continua_anos2a4 IS NULL OR cliente_ambiguo IS NULL) campos_novos_ausentes,
        count(*) FILTER (WHERE cliente_ambiguo) clientes_ambiguos,
        count(*) FILTER (WHERE continua::INT + (destino = 'perdeu_cliente_segue_na_rede')::INT
            + (NOT segue_na_rede)::INT <> 1) destinos_nao_particionam FROM p""")
    auditoria['comparavel'] = dict(zip([c[0] for c in cursor.description], cursor.fetchone()))
    auditoria['transicoes_politicas'] = con.execute("""SELECT mesmo_prefeito, partido_antes = partido_depois,
        alternancia, count(*), avg(continua::INT) FROM p GROUP BY ALL ORDER BY 1, 2, 3""").fetchall()
    auditoria['exposicoes'] = con.execute("""SELECT atende_partido_novo, atende_partido_antigo, count(*),
        avg(continua::INT) FROM p WHERE alternancia AND n_clientes >= 2
        GROUP BY ALL ORDER BY 1, 2""").fetchall()
    comp = auditoria['comparavel']
    if any(comp[c] for c in ('politica_ausente', 'valor_nao_positivo_ou_ausente', 'chaves_duplicadas',
                             'campos_novos_ausentes', 'destinos_nao_particionam')):
        raise ValueError('Chaves duplicadas, dados ausentes, valores não positivos ou destinos fora da partição: consulte auditoria')
    print('Carregando observações e registros anuais...', flush=True)
    anuais = []
    for ano in (2012, 2013, 2016, 2017, 2020, 2021):
        arquivo_ano = str(RAIZ / f'dados/limpos/rede_{ano}.parquet').replace("'", "''")
        anuais.append(f"SELECT {ano} AS ano, codigo_ibge, left(cnpj, 8) AS raiz FROM read_parquet('{arquivo_ano}')")
    con.execute('CREATE TEMP TABLE presenca_ano AS SELECT DISTINCT * FROM (' + ' UNION ALL '.join(anuais) + ')')
    auditoria['desfecho_anos_2_4'] = 'continua_anos2a4'
    d = con.execute("""SELECT continua::INT y, alternancia::INT alternancia,
        (destino = 'perdeu_cliente_segue_na_rede')::INT perdeu,
        (NOT segue_na_rede)::INT saiu,
        (anterior.raiz IS NOT NULL)::INT ultimo_ano,
        (seguinte.raiz IS NOT NULL)::INT primeiro_ano,
        (NOT mesmo_prefeito)::INT troca_prefeito, (partido_antes <> partido_depois)::INT troca_partido,
        atende_partido_novo::INT novo, atende_partido_antigo::INT antigo,
        (alternancia AND n_clientes >= 2)::INT elegivel,
        anos_ativos::DOUBLE anos, ln(valor::DOUBLE) log_valor,
        p.codigo_ibge AS c_municipio, p.raiz AS c_fornecedor, eleicao_transicao AS c_transicao,
        coalesce(setor, 'ausente') AS c_setor, n_clientes AS c_clientes,
        continua_anos2a4::INT anos_2_4, cliente_ambiguo::INT ambiguo, p.eleicao_transicao AS ano_transicao
        FROM p
        LEFT JOIN presenca_ano anterior ON anterior.ano = p.eleicao_transicao
            AND anterior.codigo_ibge = p.codigo_ibge AND anterior.raiz = p.raiz
        LEFT JOIN presenca_ano seguinte ON seguinte.ano = p.eleicao_transicao + 1
            AND seguinte.codigo_ibge = p.codigo_ibge AND seguinte.raiz = p.raiz
        ORDER BY p.eleicao_transicao, p.codigo_ibge, p.raiz""").fetchnumpy()
    con.close()
    for chave in [k for k in d if k.startswith('c_')]:
        d[chave[2:]] = codificar(np.asarray(d.pop(chave)))
    d['fornecedor_transicao'] = codificar(d['fornecedor'].astype(np.int64) * 8 + d['transicao'])
    d['municipio_transicao'] = codificar(d['municipio'].astype(np.int64) * 8 + d['transicao'])
    resultados, diagnosticos, amostras = [], {}, []
    def rodar(nome, filtro, regressores, efeitos, contrastes_extras=(), desfecho='y', sensibilidade=False):
        """Sensibilidades pré-definidas não podem sumir em silêncio: falha de identificação ou
        colinearidade vira entrada em `painel_diagnosticos.json` e linha em `painel_amostras.csv`."""
        print(f'Estimando {nome}...', flush=True)
        x = np.column_stack([v[filtro] for _, v in regressores]).astype(float)
        nomes = [rotulo for rotulo, _ in regressores]
        base = {'modelo': nome, 'n_selecionadas': int(filtro.sum())}
        try:
            out = estimar(d[desfecho][filtro], x, [d[e][filtro] for e in efeitos],
                          d['municipio'][filtro], d['fornecedor'][filtro], nomes)
        except NaoIdentificado as erro:
            diagnosticos[nome] = {'nao_identificado': str(erro), 'efeitos': efeitos, 'desfecho': desfecho}
            amostras.append({**base, 'status': 'nao_identificado', 'motivo': str(erro)})
            print(f'  não identificado: {erro}', flush=True)
            return
        except ValueError as erro:
            if not sensibilidade:
                raise
            diagnosticos[nome] = {'nao_estimado': str(erro), 'efeitos': efeitos, 'desfecho': desfecho}
            amostras.append({**base, 'status': 'nao_estimado', 'motivo': str(erro)})
            print(f'  não estimado: {erro}', flush=True)
            return
        contrastes = [(label, np.eye(len(nomes))[i]) for i, label in enumerate(nomes)]
        contrastes.extend(contrastes_extras)
        resultados.extend(registrar(out, nome, contrastes))
        diagnosticos[nome] = {k: v for k, v in out.items()
                              if k not in ('beta', 'cov', 'cov_conservadora')}
        diagnosticos[nome]['efeitos'] = efeitos
        diagnosticos[nome]['covariancia'] = out['cov'].tolist()
        diagnosticos[nome]['covariancia_conservadora'] = out['cov_conservadora'].tolist()
        amostras.append({**base, 'status': 'estimado', 'motivo': '', 'n': out['n'],
                         'n_singletons_descartados': out['n_singletons_descartados'],
                         'n_municipios': out['n_municipios'], 'n_fornecedores': out['n_fornecedores'],
                         'posto_fe_limite': out['posto_fe_limite'], 'posto_regressores': out['posto_regressores'],
                         'n_regressores': out['n_regressores'], 'gl_t': out['gl_t']})
        print(f"  n={out['n']} (de {out['n_original']}), iterações={out['iteracoes']}, clusters={out['clusters']}", flush=True)
    todos = np.ones(len(d['y']), dtype=bool)
    prefeito, partido = d['troca_prefeito'], d['troca_partido']
    padrao = ['municipio', 'transicao', 'setor', 'clientes']
    rodar('M1_alternancia', todos, [('alternancia', d['alternancia'])], padrao)
    rodar('M2_trocas_separadas', todos, [('troca_prefeito', prefeito), ('troca_partido', partido)], padrao)
    categorias = [('so_prefeito', prefeito * (1 - partido)), ('so_partido', (1 - prefeito) * partido),
                  ('prefeito_e_partido', prefeito * partido)]
    rodar('M3_quatro_transicoes', todos, categorias, padrao,
          [('muda_ambos_menos_so_prefeito', [-1, 0, 1]),
           ('interacao_ambos_menos_somente', [-1, -1, 1])])
    controle = [('anos_ativos', d['anos']), ('log_valor', d['log_valor'])]
    rodar('M4_fornecedor_transicao', todos, categorias + controle,
          ['municipio', 'fornecedor_transicao'],
          [('muda_ambos_menos_so_prefeito', [-1, 0, 1, 0, 0]),
           ('interacao_ambos_menos_somente', [-1, -1, 1, 0, 0])])
    elegivel = d['elegivel'].astype(bool)
    novo, antigo = d['novo'], d['antigo']
    exp = [('so_novo', novo * (1 - antigo)), ('so_antigo', antigo * (1 - novo)),
           ('ambos', novo * antigo)]
    rodar('E1_exposicoes', elegivel, exp + controle,
          ['municipio_transicao', 'setor', 'clientes'], [('so_novo_menos_so_antigo', [1, -1, 0, 0, 0])])
    rodar('E2_exposicoes_fornecedor_transicao', elegivel, exp + controle,
          ['municipio_transicao', 'fornecedor_transicao'], [('so_novo_menos_so_antigo', [1, -1, 0, 0, 0])])
    ultimo = d['ultimo_ano'].astype(bool)
    inter3 = [('muda_ambos_menos_so_prefeito', [-1, 0, 1]),
              ('interacao_ambos_menos_somente', [-1, -1, 1])]
    inter4 = [('muda_ambos_menos_so_prefeito', [-1, 0, 1, 0, 0]),
              ('interacao_ambos_menos_somente', [-1, -1, 1, 0, 0])]
    janelas = [('primeiro_ano', 'primeiro'), ('anos_2_4', 'anos_2_4'), ('y', 'mandato')]
    for desfecho, titulo in janelas:
        rodar(f'J3_{titulo}', ultimo, categorias, padrao, inter3, desfecho)
        rodar(f'J4_{titulo}', ultimo, categorias + controle,
              ['municipio', 'fornecedor_transicao'], inter4, desfecho)
    for desfecho in ('perdeu', 'saiu'):
        rodar(f'D1_{desfecho}', todos, [('alternancia', d['alternancia'])], padrao, desfecho=desfecho)
        rodar(f'D4_{desfecho}', todos, categorias + controle,
              ['municipio', 'fornecedor_transicao'], inter4, desfecho)
    # Sensibilidades pré-definidas (mesmos contrastes e controles dos modelos de origem).
    depois_2012 = d['ano_transicao'] != 2012
    rodar('S4_sem2012', depois_2012, categorias + controle, ['municipio', 'fornecedor_transicao'],
          inter4, sensibilidade=True)
    rodar('SE2_sem2012', elegivel & depois_2012, exp + controle,
          ['municipio_transicao', 'fornecedor_transicao'], [('so_novo_menos_so_antigo', [1, -1, 0, 0, 0])],
          sensibilidade=True)
    rodar('SE2_sem_ambiguos', elegivel & (d['ambiguo'] == 0), exp + controle,
          ['municipio_transicao', 'fornecedor_transicao'], [('so_novo_menos_so_antigo', [1, -1, 0, 0, 0])],
          sensibilidade=True)
    with (SAIDA / 'painel_amostras.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['modelo', 'status', 'motivo', 'n_selecionadas', 'n',
                                               'n_singletons_descartados', 'n_municipios', 'n_fornecedores',
                                               'posto_fe_limite', 'posto_regressores', 'n_regressores', 'gl_t'])
        writer.writeheader(); writer.writerows(amostras)
    with (SAIDA / 'painel_resultados.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys()); writer.writeheader(); writer.writerows(resultados)
    with (SAIDA / 'painel_diagnosticos.json').open('w', encoding='utf-8', newline='') as f:
        json.dump({'auditoria': auditoria, 'modelos': diagnosticos}, f, ensure_ascii=False, indent=2, allow_nan=False)
    print('Saídas:', SAIDA / 'painel_resultados.csv', SAIDA / 'painel_diagnosticos.json', flush=True)


if __name__ == '__main__':
    main()
