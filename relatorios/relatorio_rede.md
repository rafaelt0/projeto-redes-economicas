# Medidas de rede e permanência dos fornecedores depois da troca de partido


## Tamanho da rede por mandato

Nó empresa = raiz do CNPJ (8 dígitos). Partido do município = partido do prefeito eleito no início do mandato; município sem prefeito conhecido não conta partido. Mandato 2008 = anos 2009 a 2012. Ter clientes de 2 ou mais partidos é quase o mesmo que ter 2 ou mais clientes (84% das empresas com 2 clientes e 100% das com 6 ou mais), por isso essa medida não serve de ponte.

| mandato | arestas | empresas | municipios | pct_empresas_2_partidos | mediana_clientes |
|---|---|---|---|---|---|
| 2008 | 729.137 | 253.842 | 644 | 34.1 | 1.0 |
| 2012 | 704.527 | 249.939 | 644 | 32.9 | 1.0 |
| 2016 | 728.338 | 259.432 | 644 | 30.3 | 1.0 |
| 2020 | 838.055 | 284.837 | 644 | 30.0 | 1.0 |


## Destino das arestas por transição e alternância

Só municípios com mandatos inteiros (sem suplementar) e prefeito conhecido nos dois lados. Alternância: muda o partido e o prefeito. `pct_*`: % das arestas da linha. Sem baixa confirmada não significa cadastro ativo: inclui outras situações cadastrais e cadastro ausente. No Parquet, o nome legado desse destino é `saiu_da_rede_ativa`.

| transicao | alternancia | arestas | continua | perdeu_cliente_segue_na_rede | saiu_sem_baixa_confirmada | saiu_da_rede_baixada | pct_continua | pct_perdeu_segue | pct_saiu_sem_baixa_confirmada | pct_saiu_baixada |
|---|---|---|---|---|---|---|---|---|---|---|
| 2012 | não | 250.543 | 97.068 | 87.399 | 41.226 | 24.850 | 38.7 | 34.9 | 16.5 | 9.9 |
| 2012 | sim | 447.309 | 163.320 | 165.029 | 74.149 | 44.811 | 36.5 | 36.9 | 16.6 | 10.0 |
| 2016 | não | 189.507 | 74.100 | 64.904 | 31.493 | 19.010 | 39.1 | 34.2 | 16.6 | 10.0 |
| 2016 | sim | 466.693 | 170.700 | 167.131 | 79.407 | 49.455 | 36.6 | 35.8 | 17.0 | 10.6 |
| 2020 | não | 308.538 | 122.827 | 104.913 | 54.859 | 25.939 | 39.8 | 34.0 | 17.8 | 8.4 |
| 2020 | sim | 368.976 | 137.661 | 135.336 | 63.772 | 32.207 | 37.3 | 36.7 | 17.3 | 8.7 |
| todas | não | 748.588 | 293.995 | 257.216 | 127.578 | 69.799 | 39.3 | 34.4 | 17.0 | 9.3 |
| todas | sim | 1.282.978 | 471.681 | 467.496 | 217.328 | 126.473 | 36.8 | 36.4 | 16.9 | 9.9 |


## Atende o partido novo, por faixa de clientes

População das comparações: mandatos inteiros, alternância e empresa com 2 ou mais clientes. `atende_partido_novo`: a empresa vendeu no mesmo mandato a outro município governado pelo partido que assume. `atende_partido_antigo`: o mesmo com o partido que sai. `pct_continua_com` e `pct_continua_sem`: % das arestas que continuam, com e sem `atende_partido_novo`.

| faixa_clientes | arestas | pct_atende_partido_novo | pct_continua_com | pct_continua_sem | pct_atende_partido_antigo |
|---|---|---|---|---|---|
| 2+ | 992.926 | 55.1 | 41.1 | 34.9 | 60.9 |
| 2 | 132.872 | 12.3 | 32.1 | 32.3 | 14.4 |
| 3 | 86.558 | 21.4 | 33.5 | 33.2 | 25.2 |
| 4-5 | 113.324 | 31.5 | 35.2 | 34.3 | 37.3 |
| 6-10 | 157.260 | 46.7 | 36.5 | 35.5 | 53.7 |
| 11-20 | 143.977 | 64.0 | 37.9 | 37.5 | 72.0 |
| 21-50 | 153.298 | 79.6 | 38.7 | 38.5 | 87.3 |
| 51+ | 205.637 | 91.9 | 48.7 | 45.9 | 97.1 |


## Diferença atende - não atende, estratificada (Mantel-Haenszel)

Estrato = faixa de clientes x divisão CNAE do setor x transição. Nos contrastes de partido, entram empresas com 2 ou mais clientes. Em cada estrato, diferença entre a taxa de continuar das arestas que atendem o partido e das que não atendem; a média usa o peso w = n1*n0/(n1+n0). Estratos sem um dos dois grupos ficam fora, e cada contraste usa os seus. O placebo troca o partido que assume pelo que sai: se a ligação política importa, a diferença do partido novo é maior que a do antigo (linha `diferença (novo - antigo)`). 'Continua entre as que seguem na rede' exclui as arestas de empresas que não aparecem na rede observada no mandato seguinte, e separa isso de perder o cliente. O contraste 'alternância' compara as arestas de municípios com e sem alternância, em todas as arestas comparáveis (inclusive de empresas com 1 cliente) e com os mesmos critérios de estratificação: mede a associação entre alternância e continuidade. O desenho não identifica um efeito causal. Em pontos percentuais.

| resultado | contraste | arestas | arestas_atende | estratos | municipios |
|---|---|---|---|---|---|
| continua | partido novo | 992.926 | 547.160 | 1.499 | 610 |
| continua | partido antigo | 992.926 | 604.779 | 1.499 | 610 |
| continua | alternância | 2.031.566 | 1.282.978 | 1.749 | 642 |
| continua entre as que seguem na rede | partido novo | 827.132 | 485.693 | 1.472 | 610 |
| continua entre as que seguem na rede | partido antigo | 827.132 | 535.598 | 1.472 | 610 |
| continua entre as que seguem na rede | alternância | 1.490.388 | 939.177 | 1.709 | 642 |

| resultado | contraste | dif_atende_menos_nao_pp | estratos_usados |
|---|---|---|---|
| continua | partido novo | 0.71 | 1.465 |
| continua | partido antigo | 0.52 | 1.450 |
| continua | diferença (novo - antigo) | 0.19 |  |
| continua | alternância | -2.68 | 1.724 |
| continua entre as que seguem na rede | partido novo | 0.71 | 1.439 |
| continua entre as que seguem na rede | partido antigo | 0.41 | 1.426 |
| continua entre as que seguem na rede | diferença (novo - antigo) | 0.3 |  |
| continua entre as que seguem na rede | alternância | -2.92 | 1.695 |


## Intervalo de confiança de 95% (bootstrap por município)

Reamostra os municípios com reposição (200 réplicas, semente 2026); cada município leva todas as suas arestas das três transições. Os dois contrastes de partido usam as mesmas réplicas, e a diferença entre eles é calculada réplica a réplica; a alternância sorteia à parte entre os seus municípios. Intervalo pelos percentis 2,5 e 97,5.

| resultado | contraste | dif_atende_menos_nao_pp | ic95_inf_pp | ic95_sup_pp | replicas | estratos_usados |
|---|---|---|---|---|---|---|
| continua | partido novo | 0.71 | 0.03 | 1.35 | 200 | 1.465 |
| continua | partido antigo | 0.52 | -0.14 | 1.14 | 200 | 1.450 |
| continua | diferença (novo - antigo) | 0.19 | -0.62 | 0.98 | 200 |  |
| continua | alternância | -2.68 | -3.27 | -2.17 | 200 | 1.724 |
| continua entre as que seguem na rede | partido novo | 0.71 | -0.09 | 1.41 | 200 | 1.439 |
| continua entre as que seguem na rede | partido antigo | 0.41 | -0.36 | 1.12 | 200 | 1.426 |
| continua entre as que seguem na rede | diferença (novo - antigo) | 0.3 | -0.69 | 1.24 | 200 |  |
| continua entre as que seguem na rede | alternância | -2.92 | -3.53 | -2.4 | 200 | 1.695 |


## Robustez

A mesma diferença da seção de Mantel-Haenszel, com cada real empenhado no mandato anterior contando como uma observação (peso = valor da aresta), e restrita às arestas com venda em 2 ou mais anos do mandato.

| resultado | contraste | dif_atende_menos_nao_pp | ic95_inf_pp | ic95_sup_pp | replicas | estratos_usados |
|---|---|---|---|---|---|---|
| continua | partido novo | 0.71 | 0.03 | 1.35 | 200 | 1.465 |
| continua | partido antigo | 0.52 | -0.14 | 1.14 | 200 | 1.450 |
| continua | diferença (novo - antigo) | 0.19 | -0.62 | 0.98 | 200 |  |
| continua | alternância | -2.68 | -3.27 | -2.17 | 200 | 1.724 |
| continua, ponderado pelo valor | partido novo | 0.58 | -2.18 | 3.11 | 200 | 1.465 |
| continua, ponderado pelo valor | partido antigo | 0.32 | -2.78 | 4.27 | 200 | 1.450 |
| continua, ponderado pelo valor | diferença (novo - antigo) | 0.26 | -4.99 | 4.58 | 200 |  |
| continua, ponderado pelo valor | alternância | -4.36 | -6.9 | -1.78 | 200 | 1.724 |
| continua, anos_ativos >= 2 | partido novo | 0.42 | -0.4 | 1.17 | 200 | 1.381 |
| continua, anos_ativos >= 2 | partido antigo | 0.09 | -0.72 | 0.76 | 200 | 1.369 |
| continua, anos_ativos >= 2 | diferença (novo - antigo) | 0.34 | -0.66 | 1.48 | 200 |  |
| continua, anos_ativos >= 2 | alternância | -3.75 | -4.47 | -3.13 | 200 | 1.673 |


## Por transição e por tamanho

A análise "continua" separada em subgrupos, com os mesmos estratos e as mesmas réplicas do bootstrap. Com 7 subgrupos, um intervalo que exclui o zero por acaso já é esperado de vez em quando.

| resultado | contraste | dif_atende_menos_nao_pp | ic95_inf_pp | ic95_sup_pp | replicas | estratos_usados |
|---|---|---|---|---|---|---|
| continua, transição 2012 | partido novo | 0.3 | -0.76 | 1.18 | 200 | 495 |
| continua, transição 2012 | partido antigo | 0.89 | -0.08 | 1.94 | 200 | 482 |
| continua, transição 2012 | diferença (novo - antigo) | -0.58 | -2.2 | 0.83 | 200 |  |
| continua, transição 2012 | alternância | -2.44 | -3.32 | -1.62 | 200 | 579 |
| continua, transição 2016 | partido novo | 0.87 | -0.45 | 2.04 | 200 | 489 |
| continua, transição 2016 | partido antigo | 0.37 | -0.97 | 1.59 | 200 | 487 |
| continua, transição 2016 | diferença (novo - antigo) | 0.5 | -1.21 | 2.24 | 200 |  |
| continua, transição 2016 | alternância | -2.73 | -3.74 | -1.85 | 200 | 573 |
| continua, transição 2020 | partido novo | 1.04 | -0.22 | 1.94 | 200 | 481 |
| continua, transição 2020 | partido antigo | 0.24 | -0.93 | 1.37 | 200 | 481 |
| continua, transição 2020 | diferença (novo - antigo) | 0.81 | -1.31 | 2.44 | 200 |  |
| continua, transição 2020 | alternância | -2.86 | -3.8 | -2.03 | 200 | 572 |
| continua, 2 a 3 clientes | partido novo | 0.08 | -1.02 | 1.15 | 200 | 436 |
| continua, 2 a 3 clientes | partido antigo | 0.68 | -0.26 | 1.8 | 200 | 428 |
| continua, 2 a 3 clientes | diferença (novo - antigo) | -0.6 | -2.03 | 0.9 | 200 |  |
| continua, 2 a 3 clientes | alternância | -2.92 | -3.74 | -2.14 | 200 | 458 |
| continua, 4 a 10 clientes | partido novo | 0.94 | 0.13 | 1.79 | 200 | 438 |
| continua, 4 a 10 clientes | partido antigo | 0.21 | -0.71 | 0.94 | 200 | 437 |
| continua, 4 a 10 clientes | diferença (novo - antigo) | 0.73 | -0.25 | 1.95 | 200 |  |
| continua, 4 a 10 clientes | alternância | -3.03 | -3.79 | -2.46 | 200 | 440 |
| continua, 11 a 50 clientes | partido novo | 0.38 | -0.54 | 1.11 | 200 | 422 |
| continua, 11 a 50 clientes | partido antigo | 0.33 | -0.59 | 1.17 | 200 | 422 |
| continua, 11 a 50 clientes | diferença (novo - antigo) | 0.05 | -1.21 | 1.21 | 200 |  |
| continua, 11 a 50 clientes | alternância | -2.94 | -3.65 | -2.25 | 200 | 423 |
| continua, 51+ clientes | partido novo | 2.16 | 0.95 | 3.61 | 200 | 169 |
| continua, 51+ clientes | partido antigo | 4.55 | 2.72 | 6.69 | 200 | 163 |
| continua, 51+ clientes | diferença (novo - antigo) | -2.39 | -4.38 | -0.4 | 200 |  |
| continua, 51+ clientes | alternância | -1.59 | -2.42 | -1.06 | 200 | 170 |
