# Validação e limpeza das despesas do TCESP, 2023


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 28.100.127.
    Registros lidos: 28.100.126.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 256.388 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 23 | 0 | 0 | 23 | 23 | 23 | 23 | 23 | 23 | 23 | 23 | 23 | 51 | 62 | 0 | 23 |


## Codificação

O arquivo é latin-1. Na leitura, 79.823 trechos em UTF-8 foram decodificados como UTF-8
    (116 com segundo byte entre 0x80 e 0x9F, 79.707 entre 0xA0 e 0xBF) e 2.296 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 61 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| PRIORI SERVIÇOS E SOLUÇՕES, CONTABILIDADE EIRELI | PRE | 14 |
|  DE MADEIRA OU AÇO- SUPORTA ATɠ10KG. ACOMPANHA BUCHAS E PARAF | 9 |
| ALMENTE EM AÇO INOXIDÁVEL QUE ɠALTAMENTE DURÁVEL ALEM DE RESI | 6 |
| camar  Item 003: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: Tris | 6 |
| L ¨CINE IN ARTE - CINEMA ARAPEͨ | 4 |
|  EPP | Item 001: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: ROYA | 3 |
| ADO EIRELI EPP | FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: ROYA | 3 |
| LIDER  Item 002: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: ROYA | 3 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Liquidado | 9.910.138 | 198.723.360.540,10 |
| Valor Pago | 9.633.896 | 190.896.297.945,54 |
| Empenhado | 7.791.320 | 228.255.147.217,88 |
| Anulação | 669.973 | 28.046.433.935,87 |
| Reforço | 94.799 | 8.731.661.426,28 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    6.327 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 7.790.718 | 75 | 531 | 10 | 10 | 0 | 192 | 141 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Taubaté | 85 |
| São José do Rio Preto | 14 |
| Cubatão | 11 |
| Tambaú | 10 |
| Buritama | 8 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| São José do Rio Preto | 20 | 1.188.023,08 |
| Tambaú | 10 | None |
| Buritama | 9 | None |
| Santa Bárbara d Oeste | 5 | None |
| Mirante do Paranapanema | 3 | None |
| Osasco | 3 | None |
| Cubatão | 2 | 1.000,00 |
| Ourinhos | 2 | None |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.023 | 6 | 217.798,78 |
| 2.022 | 3 | 0,00 |
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

Órgãos distintos: 1742. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 126 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 65 | FUNDACAO CAIXA BENEF SERV DA UNIVERSIDADE TAUBATE |
| SERVICO | 51 | SERVICO AUTONOMO DE AGUA E ESGOTO DE SALTO - SAAE SALTO |
| FUNDO | 41 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 10 | DEPARTAMENTO AUTONOMO DE AGUA E ESGOTO |
| AGENCIA | 9 | AGENCIA MUNICIPAL DE AGUA E ESGOTO DE MARILIA-AMAE |
| AUTARQUIA | 8 | AUTARQUIA DE PREVIDÊNCIA PRÓPRIA |
| CAIXA | 8 | CAIXA APOSENTADORIA PREV SERV MUNICIPAIS DE ITATINGA |
| EMPRESA | 8 | EMPRESA DE DESENVOLVIMENTO URBANO E SOCIAL DE SOROCABA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 6 | SAAE - SERVICO AUTONOMO DE AGUA E ESGOTO |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 6.776.994 |
| PESSOA FÍSICA | 1.013.617 |
| INTERNACIONAL | 96 |
| None | 10 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 209.831 | 209.831 | 0 | None |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 6.776.994 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2023

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.

| cnpj_basicos | achados_na_receita |
|---|---|
| 201.248 | 201.240 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)


| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 209.831 | 209.803 | 19.965 |




## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 10 | 0,00 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 641.351 | 27.647.239.420,54 | 57.807 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 932.994 | 2.392.667.641,82 | 0 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 1.922.874 | 73.860.742.598,01 | 2.320 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 74.337 | 22.236.882.505,36 | 8.960 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 400.992 | 10.051.248.601,18 | 2.508 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 295.080 | 3.508.902.369,61 | 1.122 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 40.197 | 3.486.593.499,44 | 249 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 139.389 | -991.692,93 | 37.293 |
| 99 | MANTIDO | None | 3.343.494 | 65.758.507.361,30 | 167.851 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 410.128.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 167.851 | 1,00 | 570 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO PRESENCIAL | 1.190.339 | 21.124.511.215,25 |
| CONCORRÊNCIA | 16.827 | 15.587.739.368,85 |
| PREGÃO ELETRÔNICO | 387.294 | 10.345.600.535,03 |
| DISPENSA DE LICITAÇÃO | 1.490.914 | 7.848.237.166,64 |
| OUTROS/NÃO APLICÁVEL | 169.055 | 4.639.297.512,80 |
| TOMADA DE PREÇOS | 24.626 | 3.586.276.689,38 |
| INEXIGÍVEL | 37.784 | 1.766.126.444,83 |
| CONVITE | 26.073 | 651.089.561,28 |
| RDC | 82 | 189.999.160,41 |
| CONCURSO | 483 | 19.474.835,68 |
| Diálogo Competitivo | 11 | 142.540,92 |
| Leilão | 6 | 12.330,23 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 262 | 987.539.385,10 |
| 43776517000180 | BENEFICIO SOCIAL -  SABESP | Captação, tratamento e distribuição de água | 365 | 443.830.911,29 |
| 02328280000197 | BENEFICIO SOCIAL - ELEKTRO | Distribuição de energia elétrica | 217 | 421.305.260,16 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 23 | 271.777.323,75 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 27 | 263.410.837,45 |
| 02302100000106 | BANDEIRANTE ENERGIA  SA | Distribuição de energia elétrica | 30 | 213.445.687,49 |
| 07282377000120 | ENERGISA -CAIUA DISTRIBUIÇÃO DE ENERGIA S/A | Distribuição de energia elétrica | 71 | 142.855.181,96 |
| 02558157000162 | FRANCINETE DE SOUZA OLIVEIRA | Serviços de telecomunicações sem fio não especificados anteriormente | 604 | 124.689.229,09 |
| 53859112000169 | CIA JAGUARI DE ENERGIA | Distribuição de energia elétrica | 37 | 77.142.526,04 |
| 00910456000199 | AMBIENT SERVICOS AMBIENTAIS DE RP S/A | Gestão de redes de esgoto | 1 | 65.500.000,00 |
| 02998611000104 | COMPANHIA DE TRANSMDE ENERGIA ELETRICA PAULISTA | Transmissão de energia elétrica | 2 | 34.200.587,11 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 25.695.417,90 |
| 60746948000112 | BANCO BRADESCO | Bancos múltiplos, com carteira comercial | 243 | 24.303.990,94 |
| 90400888000142 | BANCO  SANTANDER | Bancos múltiplos, com carteira comercial | 252 | 23.735.292,28 |
| 01778972000174 | AMERICA NET LTDA | Serviços de telefonia fixa comutada - STFC | 17 | 22.156.546,37 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 11517841 | COMPANHIA SULAMERICANA DE DISTRIBUICAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 180 | 193 | 4.348.569,37 |
| 67228536 | REDE DE DISTR.ZEFERINO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 344 | 344 | 4.307.226,94 |
| 07732866 | ANTONELLI SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 131 | 179 | 2.904.784,24 |
| 00965345 | ASSOCIAÇÃO COMERCIAL E EMPRESARIAL DE ECP. | Atividades de associações de defesa de direitos sociais | 29 | 32 | 2.185.930,00 |
| 46464962 | ASSOCIACAO COMERCIAL E EMPRESARIAL DE TUPI PAULIST | Atividades de organizações associativas patronais e empresariais | 31 | 39 | 1.679.990,67 |
| 57412660 | SUPERMERCADO DALALANA DE ITAPIRA LTDA - EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 1.408.634,53 |
| 53913075 | SUPERMERCADO RASTELAO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 84 | 132 | 1.034.912,17 |
| 05364327 | SUPERMERCADO SANTO ANTONIO M. GUACU LTDA | Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica | 178 | 185 | 989.607,36 |
| 56440027 | SUPERMERCADO PENHA CENTER LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 72 | 73 | 771.410,18 |
| 27509356 | RVM DE SOUZA ME | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 54 | 67 | 674.490,00 |
| 05727945 | SUPERMERCADO GELAIN DE ITAPIRA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 39 | 658.997,76 |
| 03451241 | ASPUMC-ASSOC.SERV.PUBL.MUNIC.CRUZALIA | Atividades de associações de defesa de direitos sociais | 8 | 9 | 586.596,50 |
| 08468552 | DAVID BARBOZA SUPERMERCADO EIRELI | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 108 | 109 | 523.702,65 |
| 27147045 | CRISTIELE SOUSA DUARTE - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 91 | 91 | 419.368,90 |
| 20161546 | SUPERMERCADO MIX CENTER LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 416.304,25 |
| 12515796 | REAL CARD SOLUCOES EM PAGAMENTOS EIRELI ME. | Serviços combinados de escritório e apoio administrativo | 44 | 44 | 408.562,26 |
| 03354724 | PAVONI E SALAZAR SUPERMERCADOS LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 21 | 36 | 357.693,19 |
| 47619309 | CICERO PONTES DA SILVA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 125 | 143 | 291.537,28 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 34 | 46 | 240.391,06 |
| 11382312 | SUPERMERCADO JURITIS DE ITAPIRA LTDA. - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 72 | 72 | 209.857,04 |
| 58747932 | IRMAOS TROYANO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 66 | 107 | 183.125,73 |
| 65803264 | MERCADINHO VILA IZAURA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 177.804,68 |
| 01984761 | SUPERMERCADO AURELIO DE ITAPIRA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 166.406,97 |
| 06021676 | CASA DE CARNES CAMACHO DE PROMISSAO LTDA | Comércio varejista de carnes - açougues | 39 | 40 | 152.536,69 |
| 92556539 | KAPPE SOFTWARE CONSULTORIA DE INFORMATICA LTDA | Desenvolvimento de programas de computador sob encomenda | 23 | 23 | 147.375,68 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 10 | 756.784.020,01 |
| 08183516000120 | CASAMAX COM DE PECAS E EQUIPAMENTOS LTDA ME | Comércio varejista de materiais de construção em geral | 23 | 448.690.122,77 |
| 06291846000104 | CONSTROESTE   CONSTR  E PARTIC  LTDA | Construção de rodovias e ferrovias | 167 | 273.716.172,27 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 7 | 272.784.819,42 |
| 12039966000111 | LINK CARD ADM  DE BENEFICIOS EIRELI | Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica | 126 | 253.547.361,22 |
| 62162847000120 | JOFEGE   PAVIMENTACAO E CONSTRUCAO LTDA | Construção de rodovias e ferrovias | 13 | 229.942.395,93 |
| 15320722000109 | VIGENT CONSTRU  ES LTDA | Construção de edifícios | 21 | 225.118.429,02 |
| 33507785000142 | CONSORCIO SAO BERNARDO AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 224.382.456,23 |
| 69144434000161 | SANCETUR   SANTA CECILIA TURISMO LTDA | Transporte rodoviário coletivo de passageiros, com itinerário fixo, municipal | 12 | 221.261.899,47 |
| 12538448000142 | COTIA AMBIENTAL S.A | Coleta de resíduos não-perigosos | 1 | 209.468.390,66 |
| 09445502000109 | SOLUCOES SERVICOS TERCEIRIZADOS   EIRELI | Limpeza em prédios e em domicílios | 22 | 205.361.516,61 |
| 53437315000167 | COMERCIAL JOAO AFONSO  N | Comércio atacadista de produtos alimentícios em geral | 215 | 200.397.193,65 |
| 02666114000109 | MICLEAN COMERCIOS E SERVICOS LTDA | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 18 | 196.593.670,14 |
| 09033330000158 | COMPEC GALASSO ENG E CONST LTDA | Outras obras de engenharia civil não especificadas anteriormente | 9 | 187.141.669,49 |
| 36573767000157 | CITY TRANSPORTES URBANO GLOBAL LTDA | Transporte rodoviário coletivo de passageiros, com itinerário fixo, municipal | 4 | 177.480.834,79 |
| 05326068000189 | A 3 TERRAPLENAGEM E ENGENHARIA LTDA | Obras de terraplenagem | 31 | 175.475.804,08 |
| 46020301000269 | SOCIEDADE CAMPINEIRA DE EDUCAÇÃO E INSTRUÇÃO - SCEI, ASSOCIAÇÃO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 168.422.873,22 |
| 61980272000190 | S H A COM DE ALIMENTOS LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 6 | 167.471.829,51 |
| 28131759000122 | TMK ENGENHARIA S A | Obras de terraplenagem | 11 | 163.241.551,58 |
| 09294054000181 | ECOOSASCO AMBIENTAL S A | Coleta de resíduos não-perigosos | 1 | 163.213.226,34 |
| 05497348000150 | TRAIL INFRAESTRUTURA EIRELI | Construção de rodovias e ferrovias | 4 | 159.740.766,53 |
| 48211585000115 | SOCIEDADE BENEFICENTE CAMINHO DE DAMASCO | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 3 | 155.796.800,87 |
| 61608477000149 | DGB ENG.E CONSTRUCOES LTDA | Construção de rodovias e ferrovias | 41 | 150.177.602,51 |
| 48096044000193 | DEMAX - SERVIÇOS E COMÉRCIO LTDA. | Limpeza em prédios e em domicílios | 15 | 147.937.149,78 |
| 03829424000151 | PLANETA EDUCACAO GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 2 | 147.656.673,38 |
| 05340639000130 | PRIME CONS E ASS EMPRESARIAL LTDA  EPP | Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica | 57 | 145.364.278,75 |
| 02841119000112 | EGEO ENGENHARIA E SOLUCOES AMBIENTAIS LTDA | Construção de edifícios | 2 | 145.154.803,76 |
| 13461965000123 | EPPO ITU SOLUCOES AMBIENTAIS S/A | Coleta de resíduos não-perigosos | 1 | 142.076.241,19 |
| 65035222000195 | ERA TECNICA ENG  SER  LTDA | Atividades paisagísticas | 14 | 137.055.766,61 |
| 10362443000186 | CRISTIAN A DA COSTA | Comércio atacadista de frutas, verduras, raízes, tubérculos, hortaliças e legumes frescos | 63 | 137.053.322,04 |
