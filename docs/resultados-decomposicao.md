# Decomposição e janela temporal — resultados retrospectivos

Gerado por `codigo/decompor_publicacao.py`; protocolo em `docs/protocolo-publicacao.md`. Diferenças em pontos percentuais. IC percentil de 95%, 1.999 reamostragens municipais. Os destinos são mutuamente exclusivos, sem condicionamento em sobreviver na rede. O bootstrap municipal não resolve toda dependência por fornecedor compartilhado. O modelo de painel complementa esta inferência com agrupamento por município e fornecedor.

## Contrastes ajustados

| Análise | Resultado | Diferença pp | IC95 | N | Suporte | Municípios |
|---|---|---:|---|---:|---:|---:|
| alternancia_destinos | continua | -2.791 | -3.323; -2.278 | 1951293 | 1951241 | 635 |
| alternancia_destinos | perdeu_cliente_segue_na_rede | 1.993 | 1.628; 2.393 | 1951293 | 1951241 | 635 |
| alternancia_destinos | saiu_da_rede_baixada | 0.471 | 0.294; 0.657 | 1951293 | 1951241 | 635 |
| alternancia_destinos | saiu_da_rede_ativa | 0.326 | 0.026; 0.630 | 1951293 | 1951241 | 635 |
| alternancia_ultimo_ano | qualquer_ano_seguinte | -6.058 | -6.707; -5.443 | 862038 | 861905 | 635 |
| alternancia_ultimo_ano | primeiro_ano_seguinte | -6.124 | -6.810; -5.479 | 862038 | 861905 | 635 |
| alternancia_ultimo_ano | anos2a4_seguinte | -5.339 | -6.033; -4.665 | 862038 | 861905 | 635 |
| sucessao_partido | continua | -3.421 | -4.453; -2.473 | 1377437 | 1376807 | 624 |
| sucessao_partido | perdeu_cliente_segue_na_rede | 2.536 | 1.841; 3.265 | 1377437 | 1376807 | 624 |
| sucessao_partido | saiu_da_rede_baixada | 0.371 | -0.039; 0.751 | 1377437 | 1376807 | 624 |
| sucessao_partido | saiu_da_rede_ativa | 0.514 | -0.147; 1.187 | 1377437 | 1376807 | 624 |
| prefeito_mesmo_partido | continua | 0.835 | -0.118; 1.891 | 607157 | 606932 | 395 |
| prefeito_mesmo_partido | perdeu_cliente_segue_na_rede | -0.658 | -1.349; 0.031 | 607157 | 606932 | 395 |
| prefeito_mesmo_partido | saiu_da_rede_baixada | 0.121 | -0.257; 0.505 | 607157 | 606932 | 395 |
| prefeito_mesmo_partido | saiu_da_rede_ativa | -0.298 | -0.992; 0.382 | 607157 | 606932 | 395 |
| partido_mesmo_prefeito | continua | -0.022 | -1.155; 1.088 | 573856 | 573198 | 415 |
| partido_mesmo_prefeito | perdeu_cliente_segue_na_rede | 0.312 | -0.474; 1.105 | 573856 | 573198 | 415 |
| partido_mesmo_prefeito | saiu_da_rede_baixada | 0.154 | -0.300; 0.624 | 573856 | 573198 | 415 |
| partido_mesmo_prefeito | saiu_da_rede_ativa | -0.444 | -1.156; 0.260 | 573856 | 573198 | 415 |
| apenas_novo_menos_apenas_antigo | continua | 0.077 | -0.647; 0.893 | 333583 | 333406 | 598 |
| apenas_novo_menos_apenas_antigo | perdeu_cliente_segue_na_rede | -0.163 | -0.912; 0.535 | 333583 | 333406 | 598 |
| apenas_novo_menos_apenas_antigo | saiu_da_rede_baixada | 0.093 | -0.110; 0.284 | 333583 | 333406 | 598 |
| apenas_novo_menos_apenas_antigo | saiu_da_rede_ativa | -0.007 | -0.290; 0.257 | 333583 | 333406 | 598 |

## Destinos condicionais entre quem não continua

Para cada contraste, a parcela de cada destino é calculada apenas entre as arestas que não continuam na mesma prefeitura, com os mesmos estratos e pesos. As parcelas dos três destinos não contínuos somam 100% em cada grupo. A coluna de diferença é grupo 1 menos grupo 0. A decomposição da diferença na taxa de `perdeu_cliente_segue_na_rede` separa o componente de nível (mais quebras no grupo 1) do componente de composição (destinos diferentes entre quem quebra); a soma reproduz exatamente a diferença padronizada do destino no mesmo suporte MH. As parcelas condicionais são razões de taxas padronizadas, não médias de contagens ou de razões por estrato.

| Análise | Destino | Parcela grupo 0 | Parcela grupo 1 | Diferença pp | IC95 | Nível pp | Composição pp |
|---|---|---:|---:|---:|---|---:|---:|
| alternancia_destinos | perdeu_cliente_segue_na_rede | 56.86% | 57.50% | 0.64 | 0.33; 0.95 | 1.60 [1.30; 1.90] | 0.40 [0.20; 0.59] |
| alternancia_destinos | saiu_da_rede_baixada | 15.44% | 15.51% | 0.06 | -0.24; 0.37 | 0.43 [0.35; 0.52] | 0.04 [-0.15; 0.23] |
| alternancia_destinos | saiu_da_rede_ativa | 27.69% | 26.99% | -0.70 | -1.12; -0.28 | 0.76 [0.62; 0.91] | -0.44 [-0.69; -0.18] |
| sucessao_partido | perdeu_cliente_segue_na_rede | 56.23% | 57.20% | 0.96 | 0.30; 1.60 | 1.94 [1.40; 2.53] | 0.60 [0.18; 0.99] |
| sucessao_partido | saiu_da_rede_baixada | 15.95% | 15.67% | -0.27 | -0.99; 0.36 | 0.54 [0.39; 0.70] | -0.17 [-0.61; 0.23] |
| sucessao_partido | saiu_da_rede_ativa | 27.82% | 27.13% | -0.69 | -1.65; 0.34 | 0.94 [0.68; 1.20] | -0.43 [-1.02; 0.21] |

Parcelas brutas, sem padronização, para conferência direta com a tabela de destinos:

| Análise | Grupo | Não continuam | Seguem na rede | Parcela condicional |
|---|---|---:|---:|---:|
| alternancia_destinos | Demais | 438230 | 247970 | 56.58% |
| alternancia_destinos | Alternância | 777168 | 448304 | 57.68% |
| sucessao_partido | Demais | 89545 | 50282 | 56.15% |
| sucessao_partido | Alternância | 777168 | 448304 | 57.68% |

Parcelas condicionais por tamanho da carteira anterior:

| Carteira | Grupo | Não continuam | Seguem na rede | Parcela condicional |
|---|---|---:|---:|---:|
| 1 cliente(s) | Demais | 111932 | 11454 | 10.23% |
| 1 cliente(s) | Alternância | 190184 | 20227 | 10.64% |
| 2+ cliente(s) | Demais | 326298 | 236516 | 72.48% |
| 2+ cliente(s) | Alternância | 586984 | 428077 | 72.93% |

## Definições e limites

Estratos: faixa de clientes × divisão CNAE × transição, pesos n1*n0/(n1+n0). Comparações políticas são de categorias observadas, não tratamentos aleatórios. Sucessão_partido compara partidos diferentes vs iguais apenas quando muda o prefeito; prefeito_mesmo_partido compara sucessão vs permanência do prefeito quando o partido se mantém; partido_mesmo_prefeito compara mudança de legenda vs manutenção quando o prefeito permanece. Os destinos de cada contraste usam o mesmo suporte e somam zero. Último_ano restringe o risco a fornecedores com despesa no ano da eleição; primeiro_ano significa presença no ano seguinte. Novo versus antigo compara diretamente vínculos exclusivos, com suporte próprio. Não identifica equivalência nem efeito causal. Correção auditada: São João da Boa Vista/2016 é continuidade do prefeito e partido, apesar de título ocultado no TSE. Suplementares detectadas em todas as candidaturas (incluindo eventos sem vencedor registrado) excluem ambas as transições adjacentes. Vínculos partidários usam somente clientes externos sem suplementar registrada no mandato anterior. A amostra única está em permanencia_auditada.parquet. Nenhum arquivo legado foi sobrescrito.

