"""Taxas anuais, mesmo peso municipal; diagnóstico descritivo, não efeito causal."""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
import csv
import hashlib
import json
from pathlib import Path
import duckdb
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / 'dados/limpos/publicacao'


def main():
    sha=hashlib.sha256((SAIDA/'permanencia_auditada.parquet').read_bytes()).hexdigest()
    if sha!=json.loads((SAIDA/'preparacao_resumo.json').read_text(encoding='utf-8'))['sha256_arquivo']:
        raise ValueError('Amostra diverge da preparação auditada')
    con = duckdb.connect()
    con.execute("SET memory_limit='700MB'; SET threads=2; SET enable_progress_bar=false")
    con.execute(f"""CREATE TABLE anual AS SELECT DISTINCT
        regexp_extract(filename, 'rede_(\\d{{4}})\\.parquet', 1)::INT AS ano,
        codigo_ibge, left(cnpj,8) AS raiz FROM read_parquet('{RAIZ}/dados/limpos/rede_*.parquet', filename=true)""")
    con.execute("""CREATE TABLE taxa AS SELECT a.ano,a.codigo_ibge,count(*) AS n,
        avg((b.raiz IS NOT NULL)::INT) AS taxa FROM anual a LEFT JOIN anual b
        ON b.ano=a.ano+1 AND b.codigo_ibge=a.codigo_ibge AND b.raiz=a.raiz
        WHERE a.ano<2024 GROUP BY ALL""")
    con.execute(f"""CREATE TABLE politica AS SELECT DISTINCT codigo_ibge,eleicao_transicao,
        CASE WHEN NOT mesmo_prefeito AND partido_antes<>partido_depois THEN 'muda_ambos'
        WHEN NOT mesmo_prefeito THEN 'muda_prefeito' WHEN partido_antes<>partido_depois THEN 'muda_partido'
        ELSE 'mantem_ambos' END AS categoria FROM '{SAIDA}/permanencia_auditada.parquet'""")
    linhas = con.execute("""SELECT p.codigo_ibge,p.eleicao_transicao,p.categoria,
        a.ano-p.eleicao_transicao AS tempo,a.n,a.taxa FROM politica p JOIN taxa a
        ON a.codigo_ibge=p.codigo_ibge AND a.ano BETWEEN p.eleicao_transicao-3 AND p.eleicao_transicao+3
        ORDER BY 1,2,4""").fetchall()
    with (SAIDA / 'temporal_municipios.csv').open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['codigo_ibge','eleicao','categoria','tempo','n','taxa']); w.writerows(linhas)
    municipios = sorted({r[0] for r in linhas}); categorias=sorted({r[2] for r in linhas})
    mi={v:i for i,v in enumerate(municipios)}; ci={v:i for i,v in enumerate(categorias)}
    numerador=np.zeros((len(mi),len(ci),7)); denominador=np.zeros_like(numerador)
    taxas={}
    for m,e,c,t,n,r in linhas:
        numerador[mi[m],ci[c],t+3] += r
        denominador[mi[m],ci[c],t+3] += 1
        taxas.setdefault((m,e,c),{})[t]=r
    # Uma observação município-eleição da diferença fronteira - média dos três pré.
    dn=np.zeros((len(mi),len(ci))); dd=np.zeros_like(dn)
    for (m,e,c),r in taxas.items():
        if all(t in r for t in [-3,-2,-1,0]):
            dn[mi[m],ci[c]] += r[0]-np.mean([r[t] for t in [-3,-2,-1]])
            dd[mi[m],ci[c]] += 1
    rng=np.random.default_rng(2026)
    sorteios=rng.multinomial(len(mi),np.full(len(mi),1/len(mi)),size=1999).astype(float)
    pontos=numerador.sum(0)/denominador.sum(0)
    bs=(sorteios@numerador.reshape(len(mi),-1))/(sorteios@denominador.reshape(len(mi),-1))
    bs=bs.reshape(1999,len(ci),7)
    deltas=dn.sum(0)/dd.sum(0); bd=(sorteios@dn)/(sorteios@dd)
    perfis=[]; saltos=[]
    for c,j in ci.items():
        for t in range(-3,4):
            lo,hi=np.quantile(bs[:,j,t+3],[.025,.975])
            perfis.append(dict(categoria=c,tempo=t,taxa_pct=float(100*pontos[j,t+3]),
                ic95_inf_pct=float(100*lo),ic95_sup_pct=float(100*hi),n_municipio_eleicoes=int(denominador[:,j,t+3].sum())))
        lo,hi=np.quantile(bd[:,j],[.025,.975])
        saltos.append(dict(categoria=c,delta_pp=float(100*deltas[j]),ic95_inf_pp=float(100*lo),ic95_sup_pp=float(100*hi)))
    j=ci['muda_ambos']; k=ci['muda_prefeito']
    lo,hi=np.quantile(bd[:,j]-bd[:,k],[.025,.975])
    contraste=dict(estimativa_pp=float(100*(deltas[j]-deltas[k])),ic95_inf_pp=float(100*lo),ic95_sup_pp=float(100*hi))
    payload=dict(perfis=perfis,saltos=saltos,contraste_sucessao=contraste,replicas=1999,sha256_fonte=sha,
        descricao='Taxa anual; cada município-eleição com mesmo peso. Janelas sobrepostas, agrupamento municipal. Não causal.')
    (SAIDA/'temporal_resultados.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(saltos=saltos,contraste=contraste),ensure_ascii=False,indent=2),flush=True)
    con.close()


if __name__ == '__main__':
    main()
