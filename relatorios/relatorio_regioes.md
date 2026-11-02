# Permanência dos fornecedores por região intermediária do IBGE

## Cobertura e método

Mapa único por código IBGE: 644/644 municípios esperados de SP, excluída a capital, conferidos em toda a permanência antes de filtrar; 642 municípios têm arestas comparáveis. Chaves de aresta também conferidas sem duplicatas. Região = município focal da aresta; a partição do IBGE disponível hoje (quadro de 2017) é aplicada retrospectivamente às transições de 2012, 2016 e 2020.

São reutilizados n_clientes, vínculos com partidos, setor e faixa_clientes calculados na rede estadual; a rede não é recalculada dentro de cada região. Comparáveis: mandatos inteiros e alternância conhecida. Partidos novo/antigo: mesma população com alternância, 2+ clientes e ambos os vínculos conhecidos. Alternância: todas as arestas comparáveis, inclusive empresas com 1 cliente; muda partido e prefeito.

Resultado principal: destino = continua. Em cada região, Mantel-Haenszel por faixa de clientes × divisão CNAE (ausente = ??) × transição: média das diferenças de taxas com peso n1*n0/(n1+n0). n1/n0 = arestas com/sem o vínculo de partido, ou com/sem alternância. Só estratos com n1>0 e n0>0 contribuem; n_suporte é o total de arestas nesses estratos. Cada contraste usa seu suporte, que pode diferir mesmo para a mesma população. A diferença novo − antigo compara essas duas estimativas; não tem exposição ou suporte próprios (NA nessas colunas); n e municípios são da população comum.

Bootstrap: 200 réplicas, semente 2026, reiniciada por região e população. Sorteiam-se municípios com reposição dentro de cada região e população, levando todas as suas transições. Novo e antigo compartilham os sorteios; sua diferença é calculada réplica a réplica somente quando ambos são estimáveis. Alternância tem seu sorteio na própria população. IC95 pelos percentis 2,5 e 97,5 das réplicas válidas; conta de válidas explícita, inclusive zero. Estimativa/IC sem suporte = NA. Diferenças e IC em pontos percentuais.

| regiao_id | regiao | municipios_mapa | municipios_permanencia | municipios_comparaveis |
|---|---|---|---|---|
| 3.501 | São Paulo | 49 | 49 | 49 |
| 3.502 | Sorocaba | 78 | 78 | 78 |
| 3.503 | Bauru | 48 | 48 | 48 |
| 3.504 | Marília | 54 | 54 | 54 |
| 3.505 | Presidente Prudente | 55 | 55 | 55 |
| 3.506 | Araçatuba | 44 | 44 | 43 |
| 3.507 | São José do Rio Preto | 100 | 100 | 100 |
| 3.508 | Ribeirão Preto | 64 | 64 | 64 |
| 3.509 | Araraquara | 26 | 26 | 26 |
| 3.510 | Campinas | 87 | 87 | 86 |
| 3.511 | São José dos Campos | 39 | 39 | 39 |


## 3501 — São Paulo

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 58.427 | 31.505 | 26.922 | 45 | 1.056 | 57.259 | 2.1 | 0.42 | 3.75 | 200 |
| partido antigo | 58.427 | 35.117 | 23.310 | 45 | 1.000 | 55.595 | 0.93 | -0.65 | 2.68 | 200 |
| diferença (novo - antigo) | 58.427 | NA | NA | 45 | NA | NA | 1.17 | -0.81 | 3.58 | 200 |
| alternância | 162.303 | 85.299 | 77.004 | 49 | 1.488 | 161.962 | -3.78 | -5.82 | -1.97 | 200 |


## 3502 — Sorocaba

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 116.529 | 62.331 | 54.198 | 74 | 1.193 | 115.263 | -0.49 | -1.76 | 0.88 | 200 |
| partido antigo | 116.529 | 71.347 | 45.182 | 74 | 1.155 | 113.872 | 1.48 | 0.13 | 3.02 | 200 |
| diferença (novo - antigo) | 116.529 | NA | NA | 74 | NA | NA | -1.97 | -3.58 | -0.52 | 200 |
| alternância | 235.983 | 154.892 | 81.091 | 78 | 1.545 | 235.684 | -2.65 | -4.01 | -1.49 | 200 |


## 3503 — Bauru

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 66.002 | 34.527 | 31.475 | 44 | 1.098 | 64.962 | 0.65 | -1.52 | 3.3 | 200 |
| partido antigo | 66.002 | 39.584 | 26.418 | 44 | 1.034 | 63.095 | 2.4 | -0.3 | 4.57 | 200 |
| diferença (novo - antigo) | 66.002 | NA | NA | 44 | NA | NA | -1.76 | -4.66 | 2.65 | 200 |
| alternância | 135.325 | 82.848 | 52.477 | 48 | 1.469 | 135.007 | -3.87 | -5.26 | -2.4 | 200 |


## 3504 — Marília

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 85.928 | 49.693 | 36.235 | 52 | 1.089 | 84.722 | 1.0 | -0.65 | 3.09 | 200 |
| partido antigo | 85.928 | 52.802 | 33.126 | 52 | 1.037 | 83.467 | 0.62 | -2.0 | 3.23 | 200 |
| diferença (novo - antigo) | 85.928 | NA | NA | 52 | NA | NA | 0.38 | -2.58 | 3.37 | 200 |
| alternância | 168.615 | 105.775 | 62.840 | 54 | 1.430 | 168.251 | -1.36 | -2.6 | 0.06 | 200 |


## 3505 — Presidente Prudente

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 79.037 | 40.716 | 38.321 | 52 | 1.062 | 78.033 | 1.67 | -0.27 | 3.53 | 200 |
| partido antigo | 79.037 | 49.875 | 29.162 | 52 | 1.018 | 76.745 | -1.03 | -3.33 | 1.21 | 200 |
| diferença (novo - antigo) | 79.037 | NA | NA | 52 | NA | NA | 2.71 | 0.06 | 5.4 | 200 |
| alternância | 146.659 | 96.139 | 50.520 | 55 | 1.394 | 146.289 | -3.48 | -4.88 | -1.87 | 200 |


## 3506 — Araçatuba

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 64.168 | 37.272 | 26.896 | 39 | 1.055 | 63.026 | 0.81 | -0.75 | 2.75 | 200 |
| partido antigo | 64.168 | 40.586 | 23.582 | 39 | 993 | 61.129 | 0.1 | -2.37 | 2.78 | 200 |
| diferença (novo - antigo) | 64.168 | NA | NA | 39 | NA | NA | 0.71 | -2.66 | 3.8 | 200 |
| alternância | 125.647 | 76.590 | 49.057 | 43 | 1.408 | 125.327 | -1.9 | -2.86 | -0.86 | 200 |


## 3507 — São José do Rio Preto

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 161.645 | 92.593 | 69.052 | 98 | 1.236 | 160.971 | 0.27 | -1.2 | 1.73 | 200 |
| partido antigo | 161.645 | 99.130 | 62.515 | 98 | 1.185 | 158.979 | -0.7 | -1.89 | 0.57 | 200 |
| diferença (novo - antigo) | 161.645 | NA | NA | 98 | NA | NA | 0.97 | -0.83 | 3.06 | 200 |
| alternância | 284.150 | 192.425 | 91.725 | 100 | 1.542 | 283.817 | -2.72 | -3.79 | -1.59 | 200 |


## 3508 — Ribeirão Preto

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 98.927 | 54.331 | 44.596 | 61 | 1.121 | 96.108 | 1.44 | -0.78 | 3.35 | 200 |
| partido antigo | 98.927 | 57.758 | 41.169 | 61 | 1.112 | 96.209 | 0.31 | -1.71 | 1.93 | 200 |
| diferença (novo - antigo) | 98.927 | NA | NA | 61 | NA | NA | 1.13 | -1.58 | 3.92 | 200 |
| alternância | 210.204 | 130.471 | 79.733 | 64 | 1.518 | 209.862 | -2.94 | -4.49 | -0.99 | 200 |


## 3509 — Araraquara

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 40.601 | 23.359 | 17.242 | 23 | 940 | 38.693 | 0.08 | -2.07 | 2.1 | 200 |
| partido antigo | 40.601 | 25.159 | 15.442 | 23 | 898 | 36.020 | -1.01 | -3.41 | 1.35 | 200 |
| diferença (novo - antigo) | 40.601 | NA | NA | 23 | NA | NA | 1.1 | -1.97 | 3.62 | 200 |
| alternância | 83.314 | 53.519 | 29.795 | 26 | 1.313 | 82.514 | -4.69 | -6.8 | -2.73 | 200 |


## 3510 — Campinas

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 163.721 | 87.077 | 76.644 | 83 | 1.288 | 162.974 | 0.6 | -1.23 | 2.06 | 200 |
| partido antigo | 163.721 | 99.207 | 64.514 | 83 | 1.269 | 162.184 | 0.6 | -1.03 | 2.82 | 200 |
| diferença (novo - antigo) | 163.721 | NA | NA | 83 | NA | NA | 0.0 | -2.61 | 2.48 | 200 |
| alternância | 349.884 | 223.603 | 126.281 | 86 | 1.615 | 349.747 | -2.71 | -4.06 | -1.47 | 200 |


## 3511 — São José dos Campos

| contraste | n | n1 | n0 | municipios | estratos_usados | n_suporte | diferenca_pp | ic95_inf_pp | ic95_sup_pp | replicas_validas |
|---|---|---|---|---|---|---|---|---|---|---|
| partido novo | 57.941 | 33.756 | 24.185 | 39 | 958 | 55.044 | -0.35 | -2.88 | 1.38 | 200 |
| partido antigo | 57.941 | 34.214 | 23.727 | 39 | 958 | 54.655 | 1.21 | -1.5 | 3.74 | 200 |
| diferença (novo - antigo) | 57.941 | NA | NA | 39 | NA | NA | -1.56 | -4.35 | 1.24 | 200 |
| alternância | 129.482 | 81.417 | 48.065 | 39 | 1.422 | 128.906 | -4.5 | -6.32 | -2.88 | 200 |


## Limites de interpretação

Associações observacionais: os controles não identificam efeito causal ou favorecimento. As comparações regionais são exploratórias e múltiplas, sem ajuste dos intervalos por multiplicidade. Fornecedores compartilhados geram dependência entre municípios e regiões, não resolvida pelo bootstrap por município. Suportes e composições diferem; não se testa diferença entre regiões comparando seus ICs separados (nem porque um inclui zero e outro não). A partição atual pode não representar a organização regional dos períodos antigos. Permanecem os limites da rede estadual: capital excluída, cadastro/CNAE posteriores e seleção dos fornecedores já presentes no mandato anterior.
