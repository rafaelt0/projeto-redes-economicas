# Validação e limpeza das despesas do TCESP, 2018


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 24.136.359.
    Registros lidos: 24.136.358.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 878.750 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 18 | 0 | 0 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 2.144.948 | 0 | 16 |


## Codificação

O arquivo é latin-1. Na leitura, 75.024 trechos em UTF-8 foram decodificados como UTF-8
    (0 com segundo byte entre 0x80 e 0x9F, 75.024 entre 0xA0 e 0xBF) e 1.057 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 108 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
|  DE MADEIRA OU AÇO- SUPORTA ATɠ10KG. ACOMPANHA BUCHAS E PARAF | 30 |
| : VAL  Item 003: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: TRIS | 12 |
|  PVC EMBORRACHADA COR LARANJA ؽ"REGISTRO DE PREÇOS PARA AQUIS | 8 |
| NÇAS DE 01 À 10 ANOS, ENSURE PӮ   SABORES: CHOCOLATE, BAUNILH | 7 |
| ALMENTE EM AÇO INOXIDÁVEL QUE ɠALTAMENTE DURÁVEL ALEM DE RESI | 6 |
| ARANA  Item 004: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: TRIS | 6 |
| OMERCIO LTDA. | CHOCOLATE EM PӠSOLÚVEL COM 50% DE CACAU E AÇÚ | 6 |
| DUBOM  Item 003: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: ROYA | 4 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Pago | 8.803.300 | 102.858.605.608,44 |
| Valor Liquidado | 7.904.802 | 113.845.612.010,84 |
| Empenhado | 6.734.842 | 128.354.698.823,17 |
| Anulação | 613.682 | 15.247.135.547,49 |
| Reforço | 79.732 | 5.342.511.434,75 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    5.157 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.733.892 | 58 | 721 | 13 | 13 | 0 | 268 | 205 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Bragança Paulista | 72 |
| Bauru | 59 |
| Diadema | 16 |
| Botucatu | 11 |
| Ipaussu | 9 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| São José do Rio Preto | 29 | 159.173,18 |
| Ipaussu | 10 | 7.957,84 |
| Ituverava | 4 | None |
| Piracicaba | 3 | None |
| Matão | 2 | None |
| Pitangueiras | 2 | None |
| São Sebastião | 2 | 2.269,33 |
| Barrinha | 1 | 3.000,00 |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.017 | 10 | -3.858,05 |
| 2.013 | 2 | -450,00 |
| 2.016 | 1 | 0,00 |


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

Órgãos distintos: 1754. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 126 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 64 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 56 | SERVIÇO ASSIST DOS FUNC E SERV MUNICIP DE BEBEDOURO |
| FUNDO | 43 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AGENCIA | 9 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| EMPRESA | 9 | EMPRESA DE DESENVOLVIMENTO URBANO E SOCIAL DE SOROCABA |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| AUTARQUIA | 7 | AUTARQUIA DE PREVIDÊNCIA PRÓPRIA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 6 | SAAE - AMBIENTE |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 4.359.150 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1.192.095 |
| PESSOA FÍSICA | 842.927 |
| INSCRIÇÃO GENÉRICA-OUTROS | 333.987 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 4.752 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 643 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 252 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 49 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 24 |
| None | 13 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 185.929 | 185.819 | 110 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.359.150 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2018

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.

| cnpj_basicos | achados_na_receita |
|---|---|
| 177.110 | 177.103 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)


| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 185.819 | 185.783 | 34.242 |








## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 13 | 0,00 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 652.779 | 18.016.635.830,36 | 56.693 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.143.031 | 39.538.653.761,85 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 11.662 | 266.595.999,44 | 72 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 349.616 | 12.934.019.677,40 | 1.500 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 60.335 | 5.918.388.371,84 | 6.689 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 192.228 | 4.733.446.232,78 | 2.056 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 329.897 | 2.409.844.830,59 | 960 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 48.319 | 1.954.092.949,39 | 268 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 134.462 | -14.247,20 | 36.664 |
| 99 | MANTIDO | None | 2.811.550 | 32.678.323.810,24 | 148.270 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 347.538.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 148.270 | 1,00 | 495 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 1.099.876 | 12.596.827.918,98 |
| CONCORRÊNCIA | 22.116 | 5.912.250.904,83 |
| OUTROS/NÃO APLICÁVEL | 178.612 | 5.111.968.101,65 |
| DISPENSA DE LICITAÇÃO | 1.362.118 | 4.597.932.092,25 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 53.936 | 1.457.061.025,46 |
| TOMADA DE PREÇOS | 26.625 | 1.167.024.624,10 |
| INEXIGÍVEL | 24.292 | 1.110.509.498,48 |
| CONVITE | 43.239 | 476.839.569,29 |
| RDC | 201 | 200.588.509,88 |
| CONCURSO | 534 | 47.319.736,32 |
| Leilão | 1 | 1.829,00 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 246 | 622.744.726,52 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 212 | 309.355.898,96 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 340 | 225.821.839,50 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 23 | 214.211.165,20 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 30 | 194.830.909,98 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 25 | 175.409.949,80 |
| 02558157000162 | N-TELEFONICA BRASIL S.A. | Serviços de telecomunicações sem fio não especificados anteriormente | 600 | 172.912.383,74 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 62 | 93.404.757,70 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 24 | 25.858.152,06 |
| 53859112000169 | CIA JAGUARI DE ENERGIA | Distribuição de energia elétrica | 24 | 25.167.379,76 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 22.722.816,60 |
| 02302100001684 | EDP SAO PAULO DISTRIBUICAO DE ENERGIA S.A. | Distribuição de energia elétrica | 1 | 16.766.830,00 |
| 46682761000171 | COMPANHIA DE DESENVOLVIMENTO DE GUARATINGUETA - CODESG | Gestão de redes de esgoto | 1 | 15.430.607,93 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 201 | 14.207.205,70 |
| 61416244000144 | CIA NACIONAL DE ENERGIA ELETR. | Distribuição de energia elétrica | 8 | 13.786.000,05 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 11517841 | COMPANHIA SULAMERICANA DE DISTRIBUICAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 150 | 202 | 3.374.002,56 |
| 00965345 | ASSOCIAÇÃO COMERCIAL E EMPRESARIAL DE ECP. | Atividades de associações de defesa de direitos sociais | 16 | 16 | 1.144.320,00 |
| 27509356 | RVM DE SOUZA ME | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 79 | 88 | 979.793,57 |
| 07629859 | AGENCIA DE VIAGENS E TRANSPORTES VICAMPE LTDA - ME | Agências de viagens | 28 | 41 | 734.825,71 |
| 03354724 | PAVONI E SALAZAR SUPERMERCADOS LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 66 | 67 | 649.311,09 |
| 02581032 | KATIA REGINA MARTINUCCI DE OLIVEIRA EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 114 | 150 | 532.013,31 |
| 07275201 | MENDES ESPINHA E MENDES ESPINHA LTDA-EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 218 | 380 | 432.033,55 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 113 | 142 | 431.951,50 |
| 07122631 | CARV DA SILVA E ROD SUPERM LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 107 | 129 | 409.995,42 |
| 07993190 | ESPINHA E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 239 | 336 | 352.929,51 |
| 03451241 | ASPUMC-ASSOC.SERV.PUBL.MUNIC.CRUZALIA | Atividades de associações de defesa de direitos sociais | 6 | 6 | 276.733,75 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 92 | 135 | 183.491,50 |
| 20524113 | SUPERMERCADO NOVA PROMISSAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 33 | 42 | 176.534,56 |
| 29055993 | SINDICATO DAS EMP DE TRANP DE PASS DE B MANSA E V RED | Atividades de organizações associativas patronais e empresariais | 30 | 41 | 108.254,72 |
| 05938407 | FABIO FERNANDES ACOUGUES | Comércio varejista de carnes - açougues | 71 | 84 | 94.034,53 |
| 06021676 | CASA DE CARNES CAMACHO PSSAO LTDA | Comércio varejista de carnes - açougues | 33 | 34 | 71.257,14 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 11 | 13 | 68.480,00 |
| 17139426 | J.W.T. DONAIRE - ME | Comércio varejista de carnes - açougues | 13 | 26 | 55.042,00 |
| 48804561 | MIGUEL CASTILHO FERRES | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 10 | 13 | 40.900,00 |
| 55644025 | LUIS CARLOS FERRO E CIA. LTDA. - ME | Comércio varejista de carnes - açougues | 36 | 36 | 27.914,17 |
| 01066358 | ALCINDO FRANCA -ME | Comércio varejista de carnes - açougues | 11 | 14 | 26.818,20 |
| 00010639 | ANTONIO CARLOS QUINTINO ME | Comércio varejista de carnes - açougues | 48 | 59 | 23.325,00 |
| 28342220 | ABINADABE OLIVEIRA LUCIANO *** | Agências de viagens | 7 | 7 | 23.272,59 |
| 26300119 | PAULO HONORATO DA SILVA MINIMERCADO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 11 | 12 | 19.150,00 |
| 50743913 | ALCENY GARBULLIO E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 27 | 34 | 17.925,00 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 10 | 300.526.183,98 |
| 61699567000192 | SPDM - ASSOC. PAULISTA P/ DESENV. DA MEDICINA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 4 | 298.649.333,40 |
| 06291846000104 | CONSTROESTE CONST  E PARTICIPACOES LTDA | Construção de rodovias e ferrovias | 157 | 154.742.609,23 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 8 | 150.917.881,56 |
| 46020301000188 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Educação superior - graduação e pós-graduação | 2 | 137.405.449,60 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 202 | 136.004.268,99 |
| 10541089000157 | ESTRE SPI AMBIENTAL S A | Coleta de resíduos não-perigosos | 20 | 122.095.286,39 |
| 14963977000119 | INSTITUTO GERIR | Atividades associativas não especificadas anteriormente | 2 | 117.827.493,69 |
| 09033330000158 | COMPEC GALASSO ENG E CONST LTDA | Outras obras de engenharia civil não especificadas anteriormente | 9 | 114.902.125,98 |
| 60003761000129 | FACULDADE REG.MED.DE SAO JOSE R.PRETO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 30 | 113.602.511,05 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 11 | 113.404.578,70 |
| 55996615000101 | CONSLADEL - CONSTE LD ELETRONICA LTDA | Construção de edifícios | 5 | 107.581.389,79 |
| 10558895000138 | NOROMIX CONCRETO  S/A | Obras de urbanização - ruas, praças e calçadas | 161 | 102.273.056,85 |
| 19224814000138 | CONSORCIO RENOVA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 100.951.542,48 |
| 05497348000150 | TRAIL INFRAESTRUTURA LTDA | Construção de rodovias e ferrovias | 5 | 99.412.098,78 |
| 50765288000163 | MPD ENGENHARIA E CONSTRUCOES LTDA | Construção de edifícios | 2 | 99.189.933,18 |
| 48096044000193 | DEMAX SERVICOS E COMERCIO LTDA | Limpeza em prédios e em domicílios | 10 | 96.676.301,01 |
| 19478960000190 | CONSORCIO CENTRO SECO | Serviços especializados para construção não especificados anteriormente | 1 | 96.594.914,73 |
| 09294054000181 | ECOOSASCO AMBIENTAL S A | Coleta de resíduos não-perigosos | 1 | 95.383.606,99 |
| 61600839000155 | C.I.E.E. CENTRO DE INTEG. EMPRESA ESCOLA | Serviços de assistência social sem alojamento | 366 | 94.710.034,79 |
| 09445502000109 | SOLUCOES SERVICOS TERCEIRIZADOS   EIRELI | Limpeza em prédios e em domicílios | 17 | 94.337.632,22 |
| 03829424000151 | PLANETA EDUCACAO GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 5 | 94.332.532,04 |
| 71485056000121 | IRMANDADE DA SANTA CASA DE MISER. SOROCABA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 93.419.408,47 |
| 02666114000109 | MICLEAN COMERCIOS E SERVICOS LTDA | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 10 | 91.766.262,53 |
| 15664292000134 | PIRACICABA AMBIENTAL SOCIEDADE ANONIMA | Coleta de resíduos não-perigosos | 1 | 81.570.881,34 |
| 62719083000120 | PIONEIRA SANEAMENTO E LIMP URBANA LTDA | Coleta de resíduos não-perigosos | 8 | 79.826.937,55 |
| 44690238000404 | ORGANIZAÇÃO SOCIAL VITALE SAÚDE | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 79.239.721,69 |
| 60499365000215 | FUNDACAO LEONOR DE BARROS CAMARGO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 2 | 77.997.697,10 |
| 67729178000491 | COM. CIRÚRGICA RIOCLARENSE LTDA. | Comércio atacadista de medicamentos e drogas de uso humano | 495 | 76.922.112,43 |
| 08528442000117 | NUTRICIONALE   COMERCIO DE ALIMENTOS LTDA | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 300 | 76.823.905,92 |
