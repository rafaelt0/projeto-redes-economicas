"""Copia as tabelas finais para docs/publicacao/tabelas/ e grava a correção de multiplicidade e o manifesto.

Uso: python -I codigo/tabelas_publicacao.py
Roda por último, depois de figuras_publicacao.py. Não estima nada: confere que todas as etapas usaram a mesma
amostra auditada e organiza as saídas.
"""
import csv
import json
from pathlib import Path
import shutil

RAIZ=Path(__file__).resolve().parent.parent
D=RAIZ/'dados/limpos/publicacao'
DOCS=RAIZ/'docs'
TABELAS=['painel_resultados.csv','painel_diagnosticos.json','painel_amostras.csv','decomposicao_resultados.csv',
    'decomposicao_resultados.json','decomposicao_condicionais.csv','decomposicao_participacao.json','temporal_resultados.json']


def main():
    prep=json.loads((D/'preparacao_resumo.json').read_text(encoding='utf-8'))
    dec=json.loads((D/'decomposicao_resultados.json').read_text(encoding='utf-8'))
    tempo=json.loads((D/'temporal_resultados.json').read_text(encoding='utf-8'))
    share=json.loads((D/'decomposicao_participacao.json').read_text(encoding='utf-8'))
    diag=json.loads((D/'painel_diagnosticos.json').read_text(encoding='utf-8'))
    for nome,sha in [('painel',diag['auditoria'].get('sha256_fonte')),('decomposição',dec.get('sha256_fonte')),
        ('perfil anual',tempo.get('sha256_fonte')),('participação',share.get('sha256_fonte'))]:
        if sha!=prep['sha256_arquivo']:
            raise ValueError(f'{nome} não corresponde à versão auditada atual; reexecute a etapa')
    resultados=list(csv.DictReader((D/'painel_resultados.csv').open(encoding='utf-8')))
    familia=[r for r in resultados if r['contraste'] not in ('anos_ativos','log_valor')]
    n_familia=len(familia)
    destino=DOCS/'publicacao/tabelas'; destino.mkdir(exist_ok=True,parents=True)
    with (destino/'painel_multiplicidade.csv').open('w',newline='', encoding='utf-8') as f:
        campos=['modelo','contraste','p_t','p_bonferroni','n_familia']
        w=csv.DictWriter(f,fieldnames=campos);w.writeheader()
        w.writerows(dict(modelo=r['modelo'],contraste=r['contraste'],p_t=r['p_t'],
            p_bonferroni=min(1.,n_familia*float(r['p_t'])),n_familia=n_familia) for r in familia)
    for arquivo in TABELAS:
        shutil.copyfile(D/arquivo,destino/arquivo)
    (DOCS/'publicacao/manifesto-resultados.json').write_text(json.dumps(dict(
        sha256_fonte=prep['sha256_arquivo'],n=prep['total']['n'],modelos=list(diag['modelos']),
        replica_bootstrap=1999,protocolo='docs/protocolo-publicacao.md'),ensure_ascii=False,indent=2)+'\n', encoding='utf-8', newline='\n')
    print('Tabelas:',destino,flush=True)


if __name__=='__main__':
    main()
