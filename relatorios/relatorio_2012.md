# Validação e limpeza das despesas do TCESP, 2012


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 22.825.733.
    Registros lidos: 22.825.732.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 292.544 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | nr_empenho | identificador_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 505 | 505 | 0 | 0 | 505 | 505 | 505 | 505 | 505 | 505 | 505 | 505 | 505 | 505 | 3.035.951 |


## Codificação

O arquivo é latin-1. Na leitura, 87.373 trechos em UTF-8 foram decodificados como UTF-8
    (220 com segundo byte entre 0x80 e 0x9F, 87.153 entre 0xA0 e 0xBF) e 335 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 3 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| S ESCRAVOS E SENHORES DO MUNICʹPIO DE JACAREÍ" DO EMPREENDEDO | 3 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Liquidado | 8.167.640 | 78.595.556.137,53 |
| Valor Pago | 7.614.294 | 72.321.654.997,16 |
| Empenhado | 6.448.247 | 88.287.558.891,90 |
| Anulação | 564.401 | 11.596.984.402,44 |
| Reforço | 31.150 | 2.211.946.052,90 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    18.378 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.435.535 | 9.274 | 3.104 | 458 | 184 | 0 | 972 | 9.585 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Monte Mor | 7.188 |
| Rincão | 1.796 |
| Pompéia | 259 |
| Fernão | 102 |
| Diadema | 67 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Monte Mor | 7.187 | 139.647.550,61 |
| Rincão | 1.878 | 3.532.968,62 |
| Diadema | 72 | 20.482.322,97 |
| São José dos Campos | 33 | 4.340.585,73 |
| Jundiaí | 25 | 57.203,74 |
| Capivari | 11 | 35.905,30 |
| São Carlos | 10 | 98.892,60 |
| São José do Rio Preto | 9 | 21.752,68 |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.012 | 274 | 810,00 |
| 2.011 | 175 | 6.078.019,57 |
| 2.010 | 9 | 0,00 |


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

Órgãos distintos: 1756. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 121 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 70 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 55 | SERVICO DE AGUA E ESGOTO DO MUNICIPIO DE JAU |
| FUNDO | 45 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AGENCIA | 8 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| AUTARQUIA | 8 | AUTARQUIA DE ESPORTE DE ASSIS |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 6 | SAAE - AMBIENTE |
| CENTRO | 5 | CENTRO MUNICIPAL DE FORMAÇÃO PROFISSIONAL-CMFP |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 4.155.028 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 973.587 |
| PESSOA FÍSICA | 891.676 |
| INSCRIÇÃO GENÉRICA-OUTROS | 397.594 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 11.065 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 4.289 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 1.665 |
| None | 458 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 158 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 15 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 179.297 | 178.960 | 337 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.155.028 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2012

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.

| cnpj_basicos | achados_na_receita |
|---|---|
| 169.762 | 169.752 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)


| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 178.960 | 178.876 | 46.298 |



## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 458 | -55.356,69 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 693.322 | 9.941.747.623,02 | 56.528 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.038.740 | 26.070.751.405,71 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 5.081 | 22.217.361,90 | 285 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 291.178 | 8.306.137.384,49 | 1.505 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 63.850 | 2.647.184.875,88 | 7.777 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 152.893 | 2.926.446.025,09 | 2.035 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 388.840 | 1.620.822.443,98 | 912 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 34.916 | 927.908.011,67 | 245 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 128.210 | -9.761.156,52 | 38.994 |
| 99 | MANTIDO | None | 2.638.047 | 26.279.574.664,59 | 143.302 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 334.361.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 143.302 | 1,00 | 481 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 515.654 | 8.068.592.876,17 |
| CONCORRÊNCIA | 30.954 | 6.717.909.970,07 |
| DISPENSA DE LICITAÇÃO | 1.454.641 | 3.809.648.360,93 |
| OUTROS/NÃO APLICÁVEL | 417.854 | 3.656.942.654,21 |
| TOMADA DE PREÇOS | 44.616 | 1.723.075.054,73 |
| CONVITE | 109.411 | 1.332.470.037,09 |
| INEXIGÍVEL | 45.940 | 659.503.279,90 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 18.330 | 231.224.418,72 |
| CONCURSO | 647 | 80.208.012,77 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 231 | 308.910.683,86 |
| 02558157000162 | TELECOMUNICACOES .DE S.PAULO S.A. TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 590 | 248.982.875,12 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 206 | 178.824.656,42 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 318 | 142.383.154,89 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 23 | 135.819.955,24 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 30 | 133.234.051,71 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 26 | 107.700.701,15 |
| 02449992005638 | BANCO BRASIL | Telefonia móvel celular | 472 | 26.640.791,38 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 24 | 24.041.165,65 |
| 07297359000111 | E.D.E. VALE PARANAPANEMA S/A. | Distribuição de energia elétrica | 23 | 20.108.189,66 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 20 | 19.426.430,23 |
| 02592658001641 | SUSTENTARE SERVICOS AMBIENTAIS S/A | Atividades relacionadas a esgoto, exceto a gestão de redes | 1 | 13.908.059,20 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 13.335.752,90 |
| 61416244000144 | C. N. E. E. | Distribuição de energia elétrica | 15 | 13.124.212,35 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 161 | 12.755.499,74 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 47361100 | JUCO -  JUVENTUDE CÍVICA DE OSASCO | Atividades de associações de defesa de direitos sociais | 11 | 12 | 3.232.956,77 |
| 50807155 | ASSOC.SERV.FUNC.PUBLICOS MUNICIPAIS DA PREF. DE SM | Atividades de associações de defesa de direitos sociais | 240 | 262 | 2.717.950,41 |
| 07420925 | AUDAX - SERV. ADM. E  FINANCEIROS LTDA. ME | Serviços combinados de escritório e apoio administrativo | 25 | 25 | 588.224,58 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 106 | 179 | 344.302,02 |
| 07178151 | SUPERMERCADO MARAJOARA MAX LTD | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 8 | 14 | 314.937,69 |
| 07122631 | CARVALHO DA SILVA E RODRIGUES SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 113 | 113 | 305.770,00 |
| 45056793 | BARCAS DE SANTOS-GUARUJA S/C LTDA | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 22 | 29 | 276.003,20 |
| 02911243 | ASSOCIACAO DOS MORADORES DO BAIRRO DO JD ELDORADO | Atividades de associações de defesa de direitos sociais | 9 | 12 | 256.293,54 |
| 52368644 | ASSOC DOS MOR DOS B VL N S ISABEL E CRUZEIRO | Atividades de associações de defesa de direitos sociais | 9 | 10 | 244.577,10 |
| 54791470 | ASSOC DOS AMIGOS  B V GUILHERME E V GUMERCINDO | Atividades de associações de defesa de direitos sociais | 9 | 11 | 203.333,07 |
| 00010639 | ANTONIO CARLOS QUINTINO ME | Comércio varejista de carnes - açougues | 93 | 93 | 174.456,00 |
| 02581032 | KATIA REGINA MARTINUCI DE OLIVEIRA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 111 | 111 | 164.250,00 |
| 06259395 | ASSOC DOS AMIGOS DO BAIRRO OURO FINO | Atividades de associações de defesa de direitos sociais | 9 | 10 | 153.565,44 |
| 01564249 | DANIEL H. MARINELLI VERA CRUZ | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 13 | 17 | 147.689,79 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 83 | 83 | 124.124,00 |
| 06186144 | ASSOC DOS MOR DOS B CACHOEIRA E CHAC ITAPETI | Atividades de organizações religiosas ou filosóficas | 10 | 11 | 123.660,87 |
| 67191700 | EDUARDO CARLOS BONACI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 46 | 54 | 117.509,11 |
| 43068030 | JOSE CARLOS BETIO-ME | Comércio varejista de carnes - açougues | 13 | 24 | 111.645,95 |
| 55859425 | ASSOCIACAO COMERCIAL INDUSTRIAL E AGRO DE REGISTRO | Atividades de associações de defesa de direitos sociais | 43 | 44 | 87.275,00 |
| 29055993 | SINDICATO DAS EMP DE TRANP DE PASS DE B MANSA E V RED | Atividades de organizações associativas patronais e empresariais | 26 | 44 | 76.797,86 |
| 62234984 | SUPERMERCADO AVENIDA DE PEDERN | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 7 | 7 | 33.320,00 |
| 48804561 | MIGUEL CASTILHO FERRES | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 12 | 12 | 30.650,00 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 14 | 29.653,50 |
| 49865439 | BALESTRI   NESPECH LTDA   ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 10 | 10 | 27.440,00 |
| 05211992 | NAIR CORREA M. PINTO V. CRUZ - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 13 | 16 | 27.105,52 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 61699567000192 | SOCIEDADE PTA P/A  O DESENV DA MEDICINA  SPDM | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 4 | 249.373.571,61 |
| 60924040000151 | T B  SERVICOS  TRANSP   LIMPEZA  GERENC  E RECURSOS HUMANOS LTDA | Locação de automóveis sem condutor | 5 | 189.881.267,17 |
| 49957137000128 | TERMAQ   TERRAPLENAGEM  CONSTR  CIVIL E ESCAVACOES LTDA | Construção de edifícios | 11 | 182.015.086,02 |
| 62162847000120 | JOFEGE - PAVIMENTACAO E CONSTRUCAO LTDA. | Construção de rodovias e ferrovias | 12 | 170.677.581,30 |
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 6 | 161.603.848,86 |
| 56473317000108 | EMPARSANCO S A | Construção de rodovias e ferrovias | 3 | 161.357.069,71 |
| 73188336000101 | LOGIC ENGENHARIA E CONSTRUÇÃO LTDA | Construção de edifícios | 14 | 159.716.229,02 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 158 | 146.943.860,21 |
| 14310577000104 | CONSORCIO NOVO CANUDOS | Outras obras de engenharia civil não especificadas anteriormente | 4 | 140.979.049,59 |
| 43677822000114 | SOEBE CONSTRUCAO  E PAVIMENTACAO LTDA | Construção de rodovias e ferrovias | 11 | 110.060.102,99 |
| 03189580000103 | DEMOP - PARTICIPACOES LTDA | Outras obras de engenharia civil não especificadas anteriormente | 65 | 110.047.143,47 |
| 44164606000138 | ERJ ADM E RESTAURANTES DE EMPRESAS LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 15 | 108.803.659,62 |
| 61699567001245 | SPDM ASSOC PAULISTA P/O DESENV DA MEDICINA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 106.426.318,63 |
| 10541089000157 | AZALEIA EMPREENDIMENTOS E PARTICIPACOES S A | Coleta de resíduos não-perigosos | 17 | 100.888.774,92 |
| 06098460000180 | TRATENGE ENGENHARIA LTDA | Construção de rodovias e ferrovias | 2 | 98.177.466,77 |
| 46044368000152 | SERVIÇO DE SAÚDE DR. CÂNDIDO FERREIRA | Atividades de assistência psicossocial e à saúde a portadores de distúrbios psíquicos, deficiência mental e dependência química e grupos similares não | 1 | 95.819.476,52 |
| 47497367000398 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 1 | 95.803.710,85 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 8 | 95.520.805,00 |
| 46020301000269 | SOC CAMPINEIRA DE EDUCACAO E INSTRUCAO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 5 | 84.104.889,40 |
| 55996615000101 | CONSLADEL - CONST. E LACOS DETET. E ELETRONIC | Construção de edifícios | 11 | 83.716.223,67 |
| 62436282000121 | GERALDO J  COAN   CIA  LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 17 | 80.977.403,53 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 11 | 80.462.415,34 |
| 06291846000104 | CONSTROESTE CONST  E PARTICIPACOES LTDA | Construção de rodovias e ferrovias | 41 | 77.950.886,73 |
| 61836813000100 | QUITAUNA SERVICOS LTDA | Coleta de resíduos não-perigosos | 1 | 75.116.101,62 |
| 08493239000152 | CONSORCIO TECAM - TECNOLOGIA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 72.714.641,44 |
| 08528442000117 | COMERCIO DE ALIMENTOS LTDA- NUTRICIONALE | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 361 | 70.469.473,69 |
| 02293852000140 | S.P.  ALIMENTAÇÃO E SERVIÇOS LTDA.- | Fornecimento de alimentos preparados preponderantemente para empresas | 7 | 67.619.958,16 |
| 31733363000160 | CORPUS SANEAMENTO E OBRAS LTDA | Coleta de resíduos não-perigosos | 4 | 61.980.424,13 |
| 04810550000127 | LEAO ENGENHARIA LTDA | Outras obras de engenharia civil não especificadas anteriormente | 11 | 61.538.506,91 |
| 61699567000273 | SOCIEDADE PAULISTA P/O DESENV.DA MEDICINA | Atividade médica ambulatorial restrita a consultas | 4 | 57.438.266,65 |
