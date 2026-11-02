# Validação e limpeza das despesas do TCESP, 2009


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 22.237.486.
    Registros lidos: 22.237.485.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 859.583 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | nr_empenho | identificador_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 32.337 | 32.337 | 0 | 0 | 32.337 | 32.337 | 32.337 | 32.337 | 32.337 | 32.355 | 32.337 | 32.337 | 32.337 | 32.337 | 3.812.299 |


## Codificação

O arquivo é latin-1. Na leitura, 464.708 trechos em UTF-8 foram decodificados como UTF-8
    (123.986 com segundo byte entre 0x80 e 0x9F, 340.722 entre 0xA0 e 0xBF) e 0 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 27 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| A LTDA. | REFERENTE À CONTRATAǴ~AO DE EMPRESA PARA FORNECIMEN | 6 |
| MO LTDA | REFERENTE Á CONTRATAǴ~AO DE ÔNIBUS PARA TRANSPORTE  | 4 |
|  EVENTOS ME | REFERENTE À LOCAǴ~AO DE SOM, PARA A REALIZAÇÃO  | 3 |
| AO PAGAMENTO DE TAXA DE INSCRIǴ~AO DE 15 ATLETAS DE EQUIPE DE | 3 |
| CIPAL DE SAÚDE E SUA ESTRUTURAǴ~AO PARA SERVIDORES WALKIRIA A | 3 |
| EFERENTE À DESPESAS COM AQUISIǴ~AO DE MATERIAL PARA USO DA DI | 3 |
| TREINAMENTO CURSOS DE CAPACITAǴ~AO DE  PREGOEIRO/LICITAÇÕES E | 3 |
| S LTDA ME | REFERENTE À AQUISIǴ~AO DE 13 (TREZE) MUDAS DE IPÊ | 2 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Liquidado | 7.957.615 | 52.243.534.613,06 |
| Valor Pago | 7.473.464 | 45.351.748.968,10 |
| Empenhado | 6.288.560 | 59.339.403.379,92 |
| Anulação | 490.843 | 6.624.747.823,69 |
| Reforço | 27.003 | 1.168.252.574,56 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    10.940 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.238.144 | 59.016 | 2.270 | 9.902 | 219 | 0 | 1.189 | 5.655 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Jundiaí | 5.054 |
| Itapira | 202 |
| Monte Mor | 168 |
| Ribeirão Grande | 44 |
| Caraguatatuba | 35 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Américo Brasiliense | 8.722 | 34.453.935,30 |
| Itirapuã | 8.348 | 15.642.011,39 |
| Pedregulho | 7.474 | 20.471.400,91 |
| Franca | 6.935 | 24.442.398,26 |
| Tatuí | 6.203 | 130.131.175,23 |
| Tapiratiba | 6.018 | 19.770.910,80 |
| Santa Lúcia | 5.684 | 10.152.990,41 |
| São José da Bela Vista | 3.904 | 8.773.743,87 |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.009 | 9.683 | 531.903.511,16 |
| 2.008 | 213 | 0,00 |
| 2.007 | 5 | 0,00 |
| 2.010 | 1 | 0,00 |


## Municípios

Nomes distintos no TCESP: 644. Casados com o IBGE: 644 de 645 (a capital não é fiscalizada pelo TCESP).

Não casados:

| municipio_tcesp |
|---|


## Municípios do IBGE ausentes no TCESP


| codigo_ibge | nome_ibge |
|---|---|
| 3550308 | São Paulo |


## Órgãos

Órgãos distintos: 1738. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 112 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 64 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 55 | SERVICO DE AGUA E ESGOTO DO MUNICIPIO DE JAU |
| FUNDO | 45 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AUTARQUIA | 8 | AUTARQUIA DE ESPORTE DE ASSIS |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| INST | 8 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| EMPRESA | 6 | EMPRESA DE TRANSPORTES COLETIVOS DE SÃO BERNARDO DO CAMPO |
| SAAE | 6 | SAAE - SERVICO AUTONOMO DE AGUA E ESGOTO |
| CENTRO | 5 | CENTRO MUNICIPAL DE FORMAÇÃO PROFISSIONAL-CMFP |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 3.948.928 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 915.481 |
| PESSOA FÍSICA | 911.584 |
| INSCRIÇÃO GENÉRICA-OUTROS | 442.337 |
| None | 9.902 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 6.731 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 2.175 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 629 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 336 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 41 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 179.986 | 178.764 | 1.222 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 3.948.928 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2009

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%. Linhas da Receita casadas mas malformadas, ignoradas: 0.

| cnpj_basicos | achados_na_receita |
|---|---|
| 169.706 | 169.671 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)

Linhas casadas mas malformadas, ignoradas: 0.

| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 178.764 | 178.620 | 50.225 |











## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 9.902 | 6.932.659,05 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 723.975 | 7.168.120.697,89 | 59.765 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.016.699 | 18.718.494.981,62 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 13.791 | 43.159.102,84 | 961 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 261.600 | 5.822.282.871,03 | 1.930 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 64.776 | 1.763.974.559,84 | 7.390 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 129.762 | 1.668.704.178,71 | 2.099 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 387.336 | 1.334.618.144,31 | 923 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 24.769 | 543.769.368,43 | 221 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 99.380 | -1.185.007,06 | 34.190 |
| 99 | MANTIDO | None | 2.506.154 | 16.516.545.480,87 | 145.159 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 329.150.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 145.159 | 1,00 | 436 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| CONCORRÊNCIA | 26.550 | 3.749.308.049,34 |
| PREGÃO | 266.636 | 3.709.008.731,51 |
| DISPENSA DE LICITAÇÃO | 1.367.033 | 3.197.094.020,24 |
| OUTROS/NÃO APLICÁVEL | 604.204 | 3.101.404.108,75 |
| CONVITE | 112.138 | 1.147.591.717,86 |
| TOMADA DE PREÇOS | 46.610 | 980.086.524,80 |
| INEXIGÍVEL | 69.844 | 411.214.720,35 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 12.713 | 190.552.533,99 |
| CONCURSO | 426 | 30.285.074,03 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 228 | 267.594.761,95 |
| 02558157000162 | TELECOMUNICACOES .DE S.PAULO S.A. TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 496 | 200.725.518,14 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 197 | 137.706.692,09 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 320 | 106.477.734,24 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 29 | 101.618.798,44 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 25 | 100.204.276,67 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 20 | 95.744.220,95 |
| 43642727000185 | TELEC.DE SAO PAULO S/A. TELESP | Serviços de telefonia fixa comutada - STFC | 121 | 29.206.204,02 |
| 61695227000517 | ELETROPAULO ELET. DE S.PAULO | Distribuição de energia elétrica | 3 | 23.686.787,80 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 24 | 18.151.671,54 |
| 03498897000202 | *** NÃO CONSTA NO CADASTRO *** | Serviços de comunicação multimídia - SCM | 233 | 16.327.876,02 |
| 02449992005638 | BANCO BRASIL | Telefonia móvel celular | 453 | 14.347.742,20 |
| 07297359000111 | E.D.E. VALE PARANAPANEMA S/A. | Distribuição de energia elétrica | 23 | 13.922.963,50 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 13.805.247,61 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 19 | 12.502.330,77 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 50751908 | SUPERMERCADOS FURLANETTI LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 289 | 333 | 1.024.558,16 |
| 50745611 | LINDO ANDREOTTI & CIA. LTDA | Comércio varejista de artigos do vestuário e acessórios | 288 | 332 | 819.986,96 |
| 08865660 | CODAX SISTEMAS LTDA | Suporte técnico, manutenção e outros serviços em tecnologia da informação | 126 | 126 | 723.675,66 |
| 03640467 | SUPERMERCADO JAU SERVE LTDA. | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 266 | 365 | 619.436,50 |
| 07178151 | SUPERMERCADO MARAJOARA MAX LTD | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 37 | 37 | 591.040,56 |
| 55204762 | SUPERMERCADO REDI LTDA | Compra e venda de imóveis próprios | 240 | 281 | 548.534,28 |
| 62835632 | JOSE GERALDO VALENTIM JAU | Loteamento de imóveis próprios | 249 | 290 | 506.092,36 |
| 84526177 | AUTO ONIBUS INTEGRACAO LTDA | Transporte rodoviário coletivo de passageiros, com itinerário fixo, municipal | 7 | 12 | 428.509,16 |
| 05810218 | MARIA ELENA SANITA BONFIETTI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 353 | 487 | 315.407,67 |
| 45056793 | BARCAS DE SANTOS-GUARUJA S/C LTDA | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 49 | 54 | 312.092,10 |
| 02882101 | FERRACINI & LENHARO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 227 | 291 | 282.251,76 |
| 43246735 | AUTO VIACAO AMERICANA S/A -AVA | Construção de edifícios | 54 | 56 | 271.916,00 |
| 50747997 | JAC EMPREENDIMENTOS PARTICIP.E NEGOCIOS S/A | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 47 | 50 | 256.990,59 |
| 08578449 | AVALOG - LOGISTICA EM TRANSPORTES LTDA | Construção de edifícios | 59 | 60 | 244.922,40 |
| 05348094 | HSTU SERVICO DE SAUDE LTDA | Serviços de assistência social sem alojamento | 14 | 22 | 175.857,20 |
| 59275289 | TRANSPORTADORA TURISTICA  BENFICA LTDA | Transporte rodoviário de carga, exceto produtos perigosos e mudanças, intermunicipal, interestadual e internacional | 7 | 10 | 162.475,50 |
| 07356901 | ASSOCIACAO DOS CONDUTORES DE TRANSP. ALTE | Atividades de associações de defesa de direitos sociais | 86 | 88 | 124.188,60 |
| 05112616 | LUIZ CARLOS PATRIAN - ME | Comércio varejista de carnes - açougues | 486 | 504 | 123.777,64 |
| 62234984 | SUPERMERCADO AVENIDA DE PEDERN | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 38 | 38 | 114.957,90 |
| 60028362 | SUPERMERCADO SCARLASSARA LTDA | Comércio varejista de artigos do vestuário e acessórios | 42 | 42 | 84.991,80 |
| 50760180 | SUPERMERCADOS OMETTO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 188 | 212 | 79.463,36 |
| 01564249 | DANIEL H. MARINELLI VERA CRUZ | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 12 | 13 | 63.744,14 |
| 62217815 | SUPERMERCADO FURLAMAX LTDA EPP | Padaria e confeitaria com predominância de revenda | 90 | 113 | 57.437,91 |
| 04812807 | EDNA C L  DE MORAES EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 34 | 34 | 54.554,34 |
| 50745934 | VANDIR CHECHETTO & FILHO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 144 | 161 | 53.681,52 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 73188336000101 | LOGIC ENGENHARIA E CONSTRUCAO LTDA | Construção de edifícios | 16 | 171.040.160,23 |
| 61699567000192 | SECRETARIA DE ESTADO DA SAUDE | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 7 | 135.278.100,92 |
| 62436282000121 | GERALDO J  COAN   CIA  LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 36 | 130.887.169,39 |
| 53437315000167 | COMERCIAL JOAO AFONSO  N | Comércio atacadista de produtos alimentícios em geral | 170 | 103.181.103,87 |
| 49957137000128 | TERMAQ   TERRAPLENAGEM  CONSTR  CIVIL E ESCAVACOES LTDA | Construção de edifícios | 9 | 102.911.579,65 |
| 46044368000152 | *** NÃO CONSTA NO CADASTRO *** | Atividades de assistência psicossocial e à saúde a portadores de distúrbios psíquicos, deficiência mental e dependência química e grupos similares não | 2 | 91.774.478,75 |
| 56473317000108 | EMPARSANCO S A | Construção de rodovias e ferrovias | 3 | 83.596.878,93 |
| 61699567001245 | SPDM ASSOC PAULISTA P/O DESENV DA MEDICINA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 83.410.882,77 |
| 47497367000398 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 1 | 81.193.037,38 |
| 55333769000113 | ENCALSO CONSTRUCOES LTDA. | Construção de rodovias e ferrovias | 4 | 78.989.259,79 |
| 08493239000152 | CONSORCIO TECAM - TECNOLOGIA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 78.729.970,52 |
| 02293852000140 | S.P.  ALIMENTAÇÃO E SERVIÇOS LTDA.- | Fornecimento de alimentos preparados preponderantemente para empresas | 11 | 73.509.397,79 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 12 | 71.513.682,07 |
| 57543001000108 | LARA CENTRAL DE TRATAMENTO DE RESIDUOS LTDA | Coleta de resíduos não-perigosos | 7 | 62.736.678,21 |
| 14310577000104 | CONSTRUTORA OAS LTDA | Outras obras de engenharia civil não especificadas anteriormente | 5 | 58.385.249,82 |
| 50944198000130 | HOSPITAL DE CARIDADE S.VICENTE DE PAULA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 2 | 57.653.406,18 |
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 5 | 57.646.389,03 |
| 61836813000100 | QUITAUNA SERVICOS LTDA | Coleta de resíduos não-perigosos | 1 | 56.010.000,00 |
| 55996615000101 | CONSLADEL - CONSTE LD ELETRONICA LTDA | Construção de edifícios | 11 | 55.880.415,22 |
| 62162847000120 | JOFEGE - PAVIMENTACAO E CONSTRUCAO LTDA | Construção de rodovias e ferrovias | 16 | 52.174.717,07 |
| 02671087000154 | M.W.E. - PAVIMENTACAO E CONSTRUCAO LTDA. | Obras de urbanização - ruas, praças e calçadas | 10 | 50.266.916,82 |
| 49723802000119 | SCOPUS CONSTR. E INCORPORADORA LTDA | Construção de edifícios | 7 | 49.827.425,56 |
| 05252462000110 | YTAQUITI CONSTRUTORA LTDA | Obras de urbanização - ruas, praças e calçadas | 3 | 48.611.661,68 |
| 46020301000188 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Educação superior - graduação e pós-graduação | 3 | 47.073.159,52 |
| 61699567000273 | SOCIEDADE PAULISTA P/O DESENV.DA MEDICINA | Atividade médica ambulatorial restrita a consultas | 4 | 46.259.479,93 |
| 08528442000117 | NUTRICIONALE  COM DE ALIMENTOS LTDA | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 270 | 46.180.295,12 |
| 61069050000110 | CONSTRUTORA GOMES LOURENCO LTDA | Construção de redes de abastecimento de água, coleta de esgoto e construções correlatas, exceto obras de irrigação | 6 | 46.111.682,73 |
| 24232886005711 | PRO SAUDE   ASSOCIACAO BENEFICIENTE DE ASSISTENCIA SOCIA | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 1 | 45.975.676,77 |
| 99999999000191 | CONSORCIO SBC AMBIENTAL | None | 1 | 44.898.949,30 |
| 67729178000149 | CIAL CIRURGICA RIOCLARENSE LTDA | Comércio atacadista de medicamentos e drogas de uso humano | 410 | 43.715.692,61 |
