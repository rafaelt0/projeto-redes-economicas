"""Figuras científicas exportáveis a partir das saídas auditadas."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RAIZ=Path(__file__).resolve().parent.parent
DADOS=RAIZ/'dados/limpos/publicacao'
FIGURAS=RAIZ/'docs/publicacao/figuras'
NOMES={'mantem_ambos':'Mantém prefeito e partido','muda_prefeito':'Muda prefeito, mantém partido',
    'muda_partido':'Mantém prefeito, muda partido','muda_ambos':'Muda prefeito e partido'}

def fmt(x):
    return f'{x:+.2f}'.replace('.',',')


def salvar(fig,nome):
    fig.savefig(FIGURAS/f'{nome}.png',dpi=230,bbox_inches='tight',facecolor='white')
    fig.savefig(FIGURAS/f'{nome}.svg',bbox_inches='tight',facecolor='white',metadata={'Date':None})
    plt.close(fig)


def main():
    FIGURAS.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
        'font.family':'DejaVu Sans','axes.labelcolor':'#253342','text.color':'#253342','svg.hashsalt':'redes'})
    temporal=json.loads((DADOS/'temporal_resultados.json').read_text(encoding='utf-8'))
    fig,ax=plt.subplots(figsize=(8.2,4.5))
    cores=['#315974','#7995a6','#b78a3c','#a53935']
    for categoria,cor,marcador in zip(NOMES,cores,['o','s','^','D']):
        rows=[r for r in temporal['perfis'] if r['categoria']==categoria]
        x=np.array([r['tempo'] for r in rows]); y=np.array([r['taxa_pct'] for r in rows])
        ax.plot(x,y,label=NOMES[categoria],color=cor,marker=marcador,lw=1.8,markersize=4)
        ax.fill_between(x,[r['ic95_inf_pct'] for r in rows],[r['ic95_sup_pct'] for r in rows],color=cor,alpha=.09)
    ax.axvline(0,color='#555',ls=':',lw=1)
    ax.set(xlabel='Ano-base relativo à eleição (retorno no ano seguinte)',ylabel='Continuidade anual (%)',
        xticks=list(range(-3,4)),ylim=(48,61))
    ax.grid(axis='y',alpha=.15)
    ax.legend(frameon=False,loc='lower left',fontsize=8.5,ncol=2)
    fig.tight_layout();salvar(fig,'perfil-anual')
    dec=json.loads((DADOS/'decomposicao_resultados.json').read_text(encoding='utf-8'))
    r=[r for r in dec['resultados'] if r['analise']=='alternancia_destinos']
    vals=[row['estimativa_pp'] for row in r]
    labels=['Continua na mesma prefeitura','Perde a prefeitura, segue na rede',
        'Sai da rede, baixa confirmada em 2026','Sai da rede, sem baixa confirmada']
    fig,ax=plt.subplots(figsize=(8.2,3.8))
    for i,row in enumerate(r):
        ax.errorbar(vals[i],i,xerr=[[vals[i]-row['ic95_inf_pp']],[row['ic95_sup_pp']-vals[i]]],
            fmt='o',color='#a53935' if i==0 else '#315974',capsize=3,ms=6)
        ax.annotate(f"{fmt(vals[i])} pp",(vals[i],i),xytext=(0,9),textcoords='offset points',
            ha='center',fontsize=9)
    ax.axvline(0,color='#888',lw=1);ax.invert_yaxis()
    ax.set(yticks=range(4),yticklabels=labels,xlabel='Diferença ajustada: alternância menos ausência de alternância (pp)',
        xlim=(-3.7,3.3),ylim=(3.6,-.6))
    ax.grid(axis='x',alpha=.15);fig.tight_layout();salvar(fig,'destinos')
    boot=np.load(DADOS/'decomposicao_boot_alternancia_destinos.npz')['replicas']
    razao=boot[:,1]/(-boot[:,0]);lo,hi=np.quantile(razao,[.025,.975])
    share=dict(proporcao_pct=float(100*vals[1]/(-vals[0])),ic95_inf_pct=float(100*lo),ic95_sup_pct=float(100*hi),
        sha256_fonte=dec['sha256_fonte'])
    (DADOS/'decomposicao_participacao.json').write_text(json.dumps(share,ensure_ascii=False,indent=2)+'\n', encoding='utf-8', newline='\n')
    # Todos os modelos ficam em tabela; a figura apresenta as quatro categorias
    # da especificação com fornecedor×transição, sem selecionar por significância.
    rows=list(csv.DictReader((DADOS/'painel_resultados.csv').open(encoding='utf-8')))
    forest=[r for r in rows if r['modelo']=='M4_fornecedor_transicao' and r['contraste'] in
        ['so_prefeito','so_partido','prefeito_e_partido']]
    if len(forest)!=3:
        raise ValueError('Resultados M4 incompletos')
    fig,ax=plt.subplots(figsize=(8.2,3.4))
    labels=['Muda só o prefeito','Muda só o partido','Mudam prefeito e partido']
    for i,(r,label) in enumerate(zip(forest,labels)):
        est=100*float(r['estimativa']);low=100*float(r['ic95_inferior']);high=100*float(r['ic95_superior'])
        ax.errorbar(est,i,xerr=[[est-low],[high-est]],fmt='o',color='#a53935' if i==2 else '#315974',capsize=4)
        ax.annotate(f'{fmt(est)} [{fmt(low)}; {fmt(high)}]',(est,i),xytext=(0,10),textcoords='offset points',ha='center',fontsize=9)
    ax.axvline(0,color='#888',lw=1);ax.set(yticks=range(3),yticklabels=labels,ylim=(2.5,-.6),
        xlabel='Diferença de continuidade versus mantém ambos (pp)',xlim=(-3.5,2.0))
    ax.grid(axis='x',alpha=.15);fig.tight_layout();salvar(fig,'quatro-transicoes')
    print(json.dumps(share,ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
