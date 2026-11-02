# Validação e limpeza das despesas do TCESP, 2021


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 23.711.257.
    Registros lidos: 23.711.256.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 183.506 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 56 | 0 | 1 |


## Codificação

O arquivo é latin-1. Na leitura, 68.766 trechos em UTF-8 foram decodificados como UTF-8
    (31 com segundo byte entre 0x80 e 0x9F, 68.735 entre 0xA0 e 0xBF) e 1.156 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 110 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
|  DE MADEIRA OU AÇO- SUPORTA ATɠ10KG. ACOMPANHA BUCHAS E PARAF | 15 |
|  MOLHO DE TOMATE REFOGADO SACHʠCONTENDO 340G. | 12 |
| 000 SCH EXTRATO DE TOMATE SACHʠCONTENDO 340G | 11 |
| A | CORTES DE FRANGO, TIPO FILɠDO PEITO, SEM OSSO, CORTADO EM | 8 |
| PRIORI SERVIÇOS E SOLUÇՕES, CONTABILIDADE EIRELI | PRE | 8 |
| 02: CORTES DE FRANGO, TIPO FILɠDO PEITO, SEM OSSO, CORTADO EM | 6 |
| ARANA  Item 003: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: TRIS | 6 |
| LINCE  Item 013: JOGO DE DOMINӴ  Item 014: JOGO DE MONTA PALA | 6 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Pago | 8.368.079 | 136.603.576.203,76 |
| Valor Liquidado | 7.917.671 | 141.340.212.796,66 |
| Empenhado | 6.747.774 | 160.913.865.934,89 |
| Anulação | 579.870 | 19.734.314.887,84 |
| Reforço | 97.862 | 7.422.107.156,30 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    5.553 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.747.294 | 92 | 393 | 1 | 1 | 0 | 116 | 42 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| São José do Rio Preto | 21 |
| Mogi Guaçu | 12 |
| Pirassununga | 4 |
| Avaré | 2 |
| Osvaldo Cruz | 1 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Piracicaba | 39 | 0,20 |
| São José do Rio Preto | 23 | 171.499,36 |
| Bauru | 7 | None |
| Itápolis | 6 | None |
| Santa Bárbara d Oeste | 5 | None |
| Pitangueiras | 4 | None |
| Cravinhos | 1 | None |
| Nova Odessa | 1 | None |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.020 | 1 | 0,00 |


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

Órgãos distintos: 1748. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 128 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 63 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 54 | SERVICO AUTONOMO DE AGUA E ESGOTO DE SALTO - SAAE SALTO |
| FUNDO | 41 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| EMPRESA | 9 | EMPRESA DE DESENVOLVIMENTO URBANO E SOCIAL DE SOROCABA |
| AGENCIA | 8 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| CAIXA | 8 | CAIXA APOSENTADORIA PREV SERV MUNICIPAIS DE ITATINGA |
| AUTARQUIA | 7 | AUTARQUIA DE PREVIDÊNCIA PRÓPRIA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 6 | SAAE - SERVICO AUTONOMO DE AGUA E ESGOTO |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 4.351.706 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1.294.249 |
| PESSOA FÍSICA | 735.181 |
| INSCRIÇÃO GENÉRICA-OUTROS | 359.530 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 5.692 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 566 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 178 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 115 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 76 |
| None | 1 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 183.998 | 183.937 | 61 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.351.706 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2021

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.

| cnpj_basicos | achados_na_receita |
|---|---|
| 175.674 | 175.665 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)


| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 183.937 | 183.907 | 23.689 |





## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 1 | 0,00 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 607.591 | 21.190.633.839,06 | 53.258 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.180.385 | 42.654.380.880,40 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 6.839 | 133.168.113,20 | 42 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 422.853 | 17.912.734.901,24 | 1.387 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 64.204 | 11.707.856.486,14 | 7.891 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 195.322 | 6.393.446.514,88 | 2.013 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 296.182 | 2.879.171.864,27 | 1.051 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 39.935 | 2.577.204.859,30 | 239 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 134.788 | -23.013,10 | 35.145 |
| 99 | MANTIDO | None | 2.799.194 | 43.154.543.205,41 | 146.427 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 346.640.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 146.427 | 1,00 | 527 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 951.993 | 14.363.414.198,70 |
| CONCORRÊNCIA | 12.817 | 8.038.431.167,36 |
| DISPENSA DE LICITAÇÃO | 1.427.089 | 7.037.409.169,88 |
| OUTROS/NÃO APLICÁVEL | 141.883 | 5.300.964.247,54 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 195.299 | 4.755.835.181,86 |
| TOMADA DE PREÇOS | 20.088 | 1.748.580.259,79 |
| INEXIGÍVEL | 21.871 | 1.278.285.589,03 |
| CONVITE | 27.821 | 515.092.452,13 |
| RDC | 138 | 106.759.894,81 |
| CONCURSO | 193 | 9.571.719,76 |
| Leilão | 2 | 199.324,55 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 254 | 831.647.547,98 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 214 | 384.592.499,39 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 24 | 248.174.138,46 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 347 | 241.023.514,99 |
| 02302100000106 | BANDEIRANTE ENERGIA  SA | Distribuição de energia elétrica | 30 | 238.031.473,92 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 26 | 231.313.770,58 |
| 02558157000162 | TELECOMUNICACOES .DE S.PAULO S.A. TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 606 | 157.398.000,38 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 69 | 133.497.589,23 |
| 53859112000169 | CIA JAGUARI DE ENERGIA | Distribuição de energia elétrica | 35 | 75.548.418,37 |
| 02998611000104 | COMPANHIA DE TRANSMDE ENERGIA ELETRICA PAULISTA | Transmissão de energia elétrica | 1 | 26.371.709,26 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 26.102.209,60 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 208 | 22.119.138,38 |
| 60746948000112 | BANCO BRADESCO | Bancos múltiplos, com carteira comercial | 192 | 15.004.086,59 |
| 01778972000174 | AMERICA NET LTDA | Serviços de telefonia fixa comutada - STFC | 12 | 12.654.506,56 |
| 02328280001835 | ELEKTRO ELETRICIDADE E SERVICOS S/A | Distribuição de energia elétrica | 1 | 12.640.733,90 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 11517841 | COMPANHIA SULAMERICANA DE DISTRIBUICAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 180 | 194 | 3.577.799,78 |
| 27509356 | RVM DE SOUZA ME | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 138 | 138 | 1.878.796,17 |
| 02581032 | KATIA REGINA MARTINUCCI DE OLIVEIRA EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 143 | 239 | 1.441.851,16 |
| 03477342 | ASSOC. COMERCIAL INDUSTR. E AGROPEC. DE JUQUIA | Atividades de associações de defesa de direitos sociais | 9 | 18 | 1.383.890,00 |
| 46464962 | ASSOCIACAO COMERCIAL E EMPRESARIAL DE TUPI PAULIST | Atividades de organizações associativas patronais e empresariais | 25 | 32 | 1.322.597,78 |
| 00965345 | ASSOCIAÇÃO COMERCIAL E EMPRESARIAL DE ECP. | Atividades de associações de defesa de direitos sociais | 20 | 20 | 1.150.920,00 |
| 53913075 | SUPERMERCADO RASTELAO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 72 | 117 | 700.511,67 |
| 26125193 | SUPERMERCADO MAJOLI LTDA - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 13 | 397.450,88 |
| 07629859 | AGENCIA DE VIAGENS E TRANSPORTES VICAMPE LTDA - ME | Agências de viagens | 23 | 42 | 344.004,78 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 125 | 143 | 318.683,27 |
| 03451241 | ASPUMC-ASSOC.SERV.PUBL.MUNIC.CRUZALIA | Atividades de associações de defesa de direitos sociais | 7 | 7 | 306.732,00 |
| 03354724 | PAVONI E SALAZAR SUPERMERCADOS LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 286.687,43 |
| 45056793 | BARCA SANTOS GUARUJA LTDA. TRANSP.MARIT.COLET | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 24 | 24 | 176.925,70 |
| 47619309 | CICERO PONTES DA SILVA E CIA. LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 111 | 122 | 167.398,99 |
| 20524113 | SUPERMERCADO NOVA PROMISSAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 40 | 133.701,69 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 13 | 14 | 131.980,00 |
| 31132797 | JOSEFA JOVINO FERREIRA *** | Comércio varejista de carnes - açougues | 9 | 11 | 91.062,50 |
| 24129437 | CONGONHAS COMERCIO DE COMBUSTIVEIS LTDA. | Comércio varejista de combustíveis para veículos automotores | 15 | 18 | 90.513,50 |
| 06021676 | CASA DE CARNES CAMACHO PSSAO LTDA | Comércio varejista de carnes - açougues | 36 | 36 | 89.175,75 |
| 28415046 | MINIMERCADO REAL BUENO E VALETIN LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 12 | 12 | 88.072,79 |
| 08623864 | PABELLA PANETERIA E DOCARIA LTDA ME | Fabricação de produtos de padaria e confeitaria com predominância de produção própria | 33 | 62 | 86.247,40 |
| 29055993 | SINDICATO DAS EMP DE TRANP DE PASS DE B MANSA E V RED | Atividades de organizações associativas patronais e empresariais | 12 | 14 | 80.648,90 |
| 08025537 | ADILSON LIMA DOS SANTOS TRANSPORTES ME | Comércio atacadista de sementes, flores, plantas e gramas | 3 | 5 | 77.682,00 |
| 24185821 | MARISA PESSOA BATISTA - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 33 | 33 | 66.450,00 |
| 17139426 | J.W.T. DONAIRE - ME | Comércio varejista de carnes - açougues | 12 | 15 | 52.047,00 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 10 | 600.950.553,72 |
| 61699567000192 | ASSOCIAÇÃO PAULISTA PARA O DESENVOLVIMENTO DA MEDICINA-SPDM | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 4 | 299.888.470,51 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 185 | 218.135.392,34 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 10 | 211.910.195,78 |
| 22315713000187 | INSTITUTO SOCIAL HOSPITAL ALEMÃO OSWALDO CRUZ | Serviços de assistência social sem alojamento | 1 | 206.551.411,04 |
| 12538448000142 | COTIA AMBIENTAL S.A | Coleta de resíduos não-perigosos | 1 | 189.784.136,68 |
| 60003761000129 | FUND. FACULDADE REG. DE MED. SAO JOSE DO RIO PRETO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 22 | 177.472.935,23 |
| 33507785000142 | CONSORCIO SAO BERNARDO AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 171.098.330,07 |
| 62162847000120 | JOFEGE   PAVIMENTACAO E CONSTRUCAO LTDA | Construção de rodovias e ferrovias | 15 | 157.295.461,90 |
| 05497348000150 | TRAIL INFRAESTRUTURA EIRELI | Construção de rodovias e ferrovias | 5 | 151.435.653,47 |
| 07118264000193 | QUALITY MED COM  E DIS DE MEDIC LTDA EPP | Comércio atacadista de medicamentos e drogas de uso humano | 120 | 148.166.051,85 |
| 08004710000100 | GOLDEN FOOD   COMERCIO DE ALIMENTOS   EIRELI | Comércio atacadista de produtos alimentícios em geral | 21 | 147.140.166,04 |
| 06291846000104 | CONSTROESTE   CONSTR  E PARTIC  LTDA | Construção de rodovias e ferrovias | 166 | 140.484.172,30 |
| 09294054000181 | ECOOSASCO AMBIENTAL S A | Coleta de resíduos não-perigosos | 1 | 133.357.590,46 |
| 67642496000178 | INSTITUTO DE DESENVOLVIMENTO DE GESTAO TECNOLOGIA E PESQUISA EM SAUDE ASSISTENCIA SOCIAL IDGT | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 2 | 130.606.413,81 |
| 50765288000163 | MPD ENGENHARIA LTDA | Construção de edifícios | 1 | 128.021.166,06 |
| 02666114000109 | MICLEAN COMERCIOS E SERVICOS LTDA | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 11 | 127.806.083,94 |
| 08183516000120 | CASAMAX COM DE PECAS E EQUIPAMENTOS LTDA ME | Comércio varejista de materiais de construção em geral | 25 | 124.712.364,88 |
| 48211585000115 | SOCIEDADE BENEFICENTE CAMINHO DE DAMASCO | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 7 | 118.204.711,70 |
| 15320722000109 | VIGENT CONSTRUCOES LTDA | Construção de edifícios | 16 | 115.999.867,29 |
| 60499365000215 | FUNDACAO LEONOR DE BARROS CAMARGO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 2 | 113.486.584,40 |
| 47078019000114 | HOSPITAL MAHATMA GANDHI | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 13 | 113.374.462,93 |
| 03829424000151 | PLANETA EDUCACAO GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 2 | 109.341.144,84 |
| 12505853000164 | EMBU ECOLOGICA E AMBIENTAL S/A | Coleta de resíduos não-perigosos | 1 | 107.235.598,24 |
| 19224814000138 | CONSORCIO RENOVA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 107.043.841,93 |
| 66806555000133 | FBS CONSTRUCAO CIVIL E PAVIMENTACAO LTDA | Construção de rodovias e ferrovias | 3 | 104.789.847,31 |
| 08528442000117 | NUTRICIONALE   COMERCIO DE ALIMENTOS LTDA | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 324 | 104.712.852,16 |
| 48697338000170 | ASSOC. SANTAMARENSE DE BENEFICENCIA DO GJA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 103.033.265,10 |
| 10541089000157 | ESTRE SPI AMBIENTAL S.A. | Coleta de resíduos não-perigosos | 11 | 102.880.841,76 |
| 15664292000134 | PIRACICABA AMBIENTAL SOCIEDADE ANONIMA | Coleta de resíduos não-perigosos | 1 | 100.456.500,00 |
