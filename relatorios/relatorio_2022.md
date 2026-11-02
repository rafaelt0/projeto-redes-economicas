# Validação e limpeza das despesas do TCESP, 2022


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 27.496.739.
    Registros lidos: 27.496.738.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 237.705 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7.667 | 0 | 0 | 7.667 | 7.667 | 7.667 | 7.667 | 7.667 | 7.667 | 7.667 | 7.667 | 7.667 | 7.667 | 20 | 0 | 7.667 |


## Codificação

O arquivo é latin-1. Na leitura, 92.189 trechos em UTF-8 foram decodificados como UTF-8
    (6.845 com segundo byte entre 0x80 e 0x9F, 85.344 entre 0xA0 e 0xBF) e 2.876 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 153 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| ORDIA  Item 004: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: ROYA | 30 |
| 02: CORTES DE FRANGO, TIPO FILɠDO PEITO, SEM OSSO, CORTADO EM | 26 |
| 000 SCH EXTRATO DE TOMATE SACHʠCONTENDO 340G | 21 |
| A | CORTES DE FRANGO, TIPO FILɠDO PEITO, SEM OSSO, CORTADO EM | 12 |
| PRIORI SERVIÇOS E SOLUÇՕES, CONTABILIDADE EIRELI | PRE | 11 |
|  EPP | Item 001: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: TRIS | 6 |
| ALMENTE EM AÇO INOXIDÁVEL QUE ɠALTAMENTE DURÁVEL ALEM DE RESI | 6 |
| MARCOS  JOSɠ DOS SANTOS | DILIGÊNCIA DE OF | 6 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Liquidado | 9.630.586 | 171.590.746.789,81 |
| Valor Pago | 9.449.346 | 166.169.714.907,85 |
| Empenhado | 7.664.634 | 201.735.601.397,22 |
| Anulação | 659.408 | 26.907.097.053,97 |
| Reforço | 92.764 | 6.936.609.073,76 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    4.666 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 7.665.330 | 97 | 620 | 1.433 | 3 | 0 | 161 | 74 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Buritama | 24 |
| São José do Rio Preto | 23 |
| Cerqueira César | 6 |
| Ribeirão Grande | 5 |
| Oscar Bressane | 4 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Piracicaba | 28 | 0,17 |
| São José do Rio Preto | 25 | 890.534,74 |
| Cerqueira César | 8 | None |
| Santa Bárbara d Oeste | 7 | None |
| Oscar Bressane | 5 | 4.096,00 |
| Ourinhos | 5 | None |
| São Caetano do Sul | 5 | None |
| Buritama | 3 | None |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.022 | 1.432 | 24.918.414,29 |
| 2.021 | 1 | 0,00 |


## Municípios

Nomes distintos no TCESP: 644. Casados com o IBGE: 644 de 645 (a capital não é fiscalizada pelo TCESP).

Não casados:

| municipio_tcesp |
|---|

O arquivo traz o código IBGE. Nomes cujo código casado pelo nome difere do código do arquivo:

| ds_municipio | codigo_arquivo | codigo_pelo_nome |
|---|---|---|


## Municípios do IBGE ausentes no TCESP


| codigo_ibge | nome_ibge |
|---|---|
| 3550308 | São Paulo |


## Órgãos

Órgãos distintos: 1743. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 128 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 61 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 52 | SERVICO AUTONOMO DE AGUA E ESGOTO DE SALTO - SAAE SALTO |
| FUNDO | 41 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 10 | DEPARTAMENTO AUTONOMO DE AGUA E ESGOTO |
| EMPRESA | 9 | EMPRESA DE DESENVOLVIMENTO URBANO E SOCIAL DE SOROCABA |
| AGENCIA | 8 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| AUTARQUIA | 8 | AUTARQUIA DE PREVIDÊNCIA PRÓPRIA |
| CAIXA | 8 | CAIXA APOSENTADORIA PREV SERV MUNICIPAIS DE ITATINGA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 6 | SAAE - SERVICO AUTONOMO DE AGUA E ESGOTO |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 6.306.071 |
| PESSOA FÍSICA | 907.932 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 335.051 |
| INSCRIÇÃO GENÉRICA-OUTROS | 112.729 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 1.733 |
| None | 1.433 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 163 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 91 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 74 |
| INTERNACIONAL | 42 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 11 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 204.987 | 204.951 | 36 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 6.306.071 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2022

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.

| cnpj_basicos | achados_na_receita |
|---|---|
| 196.228 | 196.218 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)


| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 204.951 | 204.913 | 23.560 |





## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 1.433 | -3.113.949,66 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 631.235 | 23.840.722.935,69 | 55.580 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 1.244.207 | 14.822.451.714,46 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 2.411 | 45.636.840,80 | 23 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 1.525.179 | 53.434.033.490,62 | 2.386 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 71.293 | 18.230.911.231,36 | 8.161 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 352.795 | 8.005.029.464,92 | 2.486 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 307.694 | 3.508.754.391,42 | 1.140 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 41.717 | 2.911.219.943,95 | 247 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 142.511 | -319.819,72 | 37.334 |
| 99 | MANTIDO | None | 3.344.855 | 56.971.385.179,47 | 164.934 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 400.165.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 164.934 | 1,00 | 549 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO PRESENCIAL | 1.163.307 | 19.765.239.531,78 |
| CONCORRÊNCIA | 15.336 | 11.175.898.943,36 |
| PREGÃO ELETRÔNICO | 312.095 | 8.127.488.897,92 |
| DISPENSA DE LICITAÇÃO | 1.602.279 | 7.370.473.384,77 |
| OUTROS/NÃO APLICÁVEL | 165.104 | 4.556.585.054,71 |
| TOMADA DE PREÇOS | 25.116 | 3.600.990.146,23 |
| INEXIGÍVEL | 31.590 | 1.504.963.775,97 |
| CONVITE | 29.559 | 743.380.275,39 |
| RDC | 114 | 105.259.449,74 |
| CONCURSO | 322 | 20.663.757,11 |
| Leilão | 2 | 327.971,52 |
| Diálogo Competitivo | 31 | 113.990,97 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 262 | 1.006.627.826,22 |
| 02328280000197 | BENEFICIO SOCIAL - ELEKTRO | Distribuição de energia elétrica | 217 | 427.190.481,44 |
| 43776517000180 | BENEFICIO SOCIAL -  SABESP | Captação, tratamento e distribuição de água | 363 | 365.256.975,40 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 24 | 300.295.056,60 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 27 | 260.272.907,97 |
| 02302100000106 | BANDEIRANTE ENERGIA  SA | Distribuição de energia elétrica | 30 | 260.270.877,11 |
| 02558157000162 | FRANCINETE DE SOUZA OLIVEIRA | Serviços de telecomunicações sem fio não especificados anteriormente | 609 | 153.364.874,61 |
| 07282377000120 | ENERGISA -CAIUA DISTRIBUIÇÃO DE ENERGIA S/A | Distribuição de energia elétrica | 72 | 146.155.062,57 |
| 53859112000169 | CIA JAGUARI DE ENERGIA | Distribuição de energia elétrica | 37 | 83.420.979,05 |
| 00910456000199 | AMBIENT SERVICOS AMBIENTAIS DE RP S/A | Gestão de redes de esgoto | 1 | 66.800.000,00 |
| 02998611000104 | COMPANHIA DE TRANSMDE ENERGIA ELETRICA PAULISTA | Transmissão de energia elétrica | 3 | 31.318.572,17 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 28.850.452,15 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 238 | 21.751.979,35 |
| 60746948000112 | BANCO BRADESCO | Bancos múltiplos, com carteira comercial | 237 | 21.151.589,27 |
| 01778972000174 | AMERICA NET LTDA | Serviços de telefonia fixa comutada - STFC | 16 | 20.290.883,13 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 11517841 | COMPANHIA SULAMERICANA DE DISTRIBUICAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 180 | 187 | 3.925.693,73 |
| 44498384 | SUPERMERCADO FERNANDES DE IGARACU LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 128 | 135 | 2.333.213,06 |
| 27509356 | RVM DE SOUZA ME | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 139 | 139 | 1.740.457,86 |
| 00965345 | ASSOCIAÇÃO COMERCIAL E EMPRESARIAL DE ECP. | Atividades de associações de defesa de direitos sociais | 24 | 24 | 1.665.230,00 |
| 02581032 | KATIA REGINA MARTINUCCI DE OLIVEIRA EIRELI | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 144 | 274 | 1.653.460,92 |
| 46464962 | ASSOCIACAO COMERCIAL E EMPRESARIAL DE TUPI PAULIST | Atividades de organizações associativas patronais e empresariais | 32 | 40 | 1.475.717,11 |
| 12515796 | REAL CARD SOLUCOES EM PAGAMENTOS EIRELI | Serviços combinados de escritório e apoio administrativo | 74 | 75 | 787.300,03 |
| 02086040 | SUPERMERCADO BURGOS & CIA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 104 | 111 | 577.109,98 |
| 03640467 | SUPERMERCADO JAU SERVE LTDA. ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 103 | 124 | 571.654,40 |
| 04067201 | SUPERMERCADO ANA MARA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 99 | 99 | 561.000,00 |
| 45056793 | BARCA SANTOS GUARUJA LTDA. TRANSP.MARIT.COLET | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 31 | 31 | 481.039,55 |
| 03451241 | ASPUMC-ASSOC.SERV.PUBL.MUNIC.CRUZALIA | Atividades de associações de defesa de direitos sociais | 6 | 6 | 366.447,50 |
| 47716873 | ZANATTA CIA LTDA | Serviços combinados de escritório e apoio administrativo | 127 | 157 | 358.129,75 |
| 03354724 | PAVONI E SALAZAR SUPERMERCADOS LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 37 | 340.304,85 |
| 47619309 | CICERO PONTES DA SILVA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 184 | 232 | 226.997,07 |
| 20524113 | SUPERMERCADO NOVA PROMISSAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 61 | 173.684,70 |
| 21303181 | BUS FACIL TECNOLOGIA E SERVICOS LTDA | Outras atividades auxiliares dos transportes terrestres não especificadas anteriormente | 12 | 15 | 159.090,55 |
| 26125193 | SUPERMERCADO MAJOLI LTDA - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 4 | 6 | 143.091,06 |
| 10629930 | EVERTON APARECIDO LEMES E CIA MINIMERCADO LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 79 | 79 | 136.285,00 |
| 92556539 | KAPPE SOFTWARE CONSULTORIA DE INFORMATICA LTDA | Desenvolvimento de programas de computador sob encomenda | 6 | 6 | 108.100,00 |
| 29055993 | SINDICATO DAS EMP DE TRANP DE PASS DE B MANSA E V RED | Atividades de organizações associativas patronais e empresariais | 13 | 13 | 102.552,93 |
| 06021676 | CASA DE CARNES CAMACHO PSSAO LTDA | Comércio varejista de carnes - açougues | 36 | 36 | 102.055,02 |
| 57742819 | ASSOC.CATR.AUTON.PRAIA STA.CRUZ NAVEGANTES | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 10 | 10 | 66.138,62 |
| 58173139 | MONTE SERRAT CASINO ELEVADOR LTDA | Trens turísticos, teleféricos e similares | 4 | 5 | 56.503,62 |
| 55644025 | LUIS CARLOS FERRO E CIA. LTDA. - ME | Comércio varejista de carnes - açougues | 36 | 36 | 53.667,49 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 9 | 518.287.191,58 |
| 08183516000120 | CASAMAX COM DE PECAS E EQUIPAMENTOS LTDA ME | Comércio varejista de materiais de construção em geral | 25 | 298.749.092,28 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 8 | 235.061.971,93 |
| 62162847000120 | JOFEGE   PAVIMENTACAO E CONSTRUCAO LTDA | Construção de rodovias e ferrovias | 13 | 223.799.881,77 |
| 12039966000111 | LINK CARD ADM  DE BENEFICIOS EIRELI | Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica | 109 | 223.507.948,40 |
| 12538448000142 | COTIA AMBIENTAL S.A | Coleta de resíduos não-perigosos | 1 | 211.135.655,39 |
| 33507785000142 | CONSORCIO SAO BERNARDO AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 199.716.794,60 |
| 53437315000167 | COMERCIAL JOAO AFONSO  N | Comércio atacadista de produtos alimentícios em geral | 200 | 188.274.672,74 |
| 07118264000193 | QUALITY MED COM  E DIS DE MEDIC LTDA EPP | Comércio atacadista de medicamentos e drogas de uso humano | 105 | 176.165.259,26 |
| 60003761000129 | FUND FAC REG DE MEDICINA S J RIO PRETO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 26 | 175.214.559,40 |
| 06291846000104 | CONSTROESTE   CONSTR  E PARTIC  LTDA | Construção de rodovias e ferrovias | 168 | 166.349.500,68 |
| 09445502000109 | SOLUCOES SERVICOS TERCEIRIZADOS   EIRELI | Limpeza em prédios e em domicílios | 20 | 163.251.765,66 |
| 46020301000269 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 3 | 163.218.481,97 |
| 15320722000109 | VIGENT CONSTRUCOES LTDA | Construção de edifícios | 20 | 157.043.141,80 |
| 44782779000110 | SANTA CASA DE MISERICORDIA DE BARRETOS | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 155.327.250,02 |
| 02666114000109 | MICLEAN COMERCIOS E SERVICOS LTDA | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 15 | 155.264.464,57 |
| 09294054000181 | ECOOSASCO AMBIENTAL S A | Coleta de resíduos não-perigosos | 1 | 153.384.252,80 |
| 36573767000157 | CITY TRANSPORTES URBANO GLOBAL LTDA | Transporte rodoviário coletivo de passageiros, com itinerário fixo, municipal | 4 | 153.203.455,13 |
| 50765288000163 | MPD ENGENHARIA LTDA | Construção de edifícios | 1 | 142.467.270,35 |
| 03829424000151 | PLANETA EDUCACAO GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 2 | 137.798.017,50 |
| 05497348000150 | TRAIL INFRAESTRUTURA EIRELI | Construção de rodovias e ferrovias | 4 | 133.682.671,24 |
| 69144434000161 | SANCETUR   SANTA CECILIA TURISMO LTDA | Transporte rodoviário coletivo de passageiros, com itinerário fixo, municipal | 10 | 131.126.718,52 |
| 11164874000109 | RC NUTRY ALIMENTACAO LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 6 | 130.355.569,86 |
| 61980272000190 | S H A COMERCIO DE ALIMENTOS LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 6 | 124.780.437,99 |
| 04597289000129 | NET TELECOM INFORMATICA LTDA | Suporte técnico, manutenção e outros serviços em tecnologia da informação | 25 | 123.803.391,94 |
| 05326068000189 | A 3 TERRAPLANAGEM ENGENHARIA LTDA | Obras de terraplenagem | 32 | 121.099.609,33 |
| 05340639000130 | PRIME CONS E ASS EMPRESARIAL LTDA  EPP | Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica | 46 | 120.238.459,40 |
| 13034156000135 | TETO CONSTRUTORA LTDA | Construção de edifícios | 37 | 113.343.782,34 |
| 28131759000122 | TMK ENGENHARIA S A | Obras de terraplenagem | 10 | 111.601.013,97 |
| 48096044000193 | DEMAX - SERVIÇOS E COMÉRCIO LTDA. | Limpeza em prédios e em domicílios | 13 | 110.124.619,03 |
