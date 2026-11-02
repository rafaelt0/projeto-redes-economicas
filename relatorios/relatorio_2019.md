# Validação e limpeza das despesas do TCESP, 2019


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 24.317.549.
    Registros lidos: 24.317.548.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 229.530 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 2.009.548 | 0 | 10 |


## Codificação

O arquivo é latin-1. Na leitura, 77.130 trechos em UTF-8 foram decodificados como UTF-8
    (0 com segundo byte entre 0x80 e 0x9F, 77.130 entre 0xA0 e 0xBF) e 1.184 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 157 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| MORANGO E CHOCOLATE, FORTINI PӮ - SUPLEMENTO NUTRICIONAL SEM  | 15 |
| NÇAS DE 01 À 10 ANOS, ENSURE PӮ   SABORES: CHOCOLATE, BAUNILH | 14 |
| A | CORTES DE FRANGO, TIPO FILɠDO PEITO, SEM OSSO, CORTADO EM | 12 |
| M PROTEÍNAS LÁCTEAS, FORTINI PӮ - SUPLEMENTO NUTRICIONAL SEM  | 12 |
| ODDY  Item 002: CHOCOLATE EM PӠSOLÚVEL COM 50% DE CACAU E AÇÚ | 9 |
| OMERCIO LTDA. | CHOCOLATE EM PӠSOLÚVEL COM 50% DE CACAU E AÇÚ | 9 |
|  PVC EMBORRACHADA COR LARANJA ؽ"REGISTRO DE PREÇOS PARA AQUIS | 8 |
| COAMO  Item 004: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: ROYA | 6 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Pago | 8.510.056 | 118.783.059.637,49 |
| Valor Liquidado | 8.188.248 | 124.939.796.255,55 |
| Empenhado | 6.919.497 | 140.001.412.018,07 |
| Anulação | 618.673 | 14.716.470.040,66 |
| Reforço | 81.074 | 4.831.813.578,87 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    5.109 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.918.756 | 46 | 550 | 6 | 6 | 0 | 240 | 162 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Americana | 61 |
| Osasco | 31 |
| Botucatu | 22 |
| Clementina | 12 |
| São José do Rio Preto | 9 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Bauru | 21 | None |
| São José do Rio Preto | 10 | 59.931,86 |
| Mogi das Cruzes | 5 | None |
| Pitangueiras | 3 | None |
| Sagres | 2 | 6.101,50 |
| Cravinhos | 1 | None |
| Divinolândia | 1 | 500,00 |
| Jaboticabal | 1 | None |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.017 | 3 | 0,00 |
| 2.018 | 2 | 2.307,20 |
| 2.019 | 1 | 247,16 |


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

Órgãos distintos: 1750. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 127 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 62 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 55 | SERVIÇO ASSIST DOS FUNC E SERV MUNICIP DE BEBEDOURO |
| FUNDO | 41 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AGENCIA | 9 | AGENCIA INVESTE SOROCABA |
| EMPRESA | 9 | EMPRESA DE DESENVOLVIMENTO URBANO E SOCIAL DE SOROCABA |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| AUTARQUIA | 7 | AUTARQUIA DE PREVIDÊNCIA PRÓPRIA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 6 | SAAE - AMBIENTE |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 4.432.082 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1.253.264 |
| PESSOA FÍSICA | 864.602 |
| INSCRIÇÃO GENÉRICA-OUTROS | 362.557 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 5.244 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 673 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 200 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 101 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 27 |
| None | 6 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 187.314 | 187.225 | 89 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.432.082 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2019

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.

| cnpj_basicos | achados_na_receita |
|---|---|
| 178.692 | 178.687 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)


| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 187.225 | 187.185 | 30.944 |







## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 6 | 0,00 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 664.692 | 19.606.776.855,27 | 56.634 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.247.155 | 41.587.020.414,65 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 8.661 | 170.748.989,38 | 59 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 365.244 | 14.728.120.371,38 | 1.621 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 59.768 | 6.900.371.918,74 | 6.785 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 200.864 | 5.068.819.778,23 | 2.081 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 311.988 | 2.673.243.017,69 | 986 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 46.266 | 2.200.501.612,69 | 268 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 127.408 | -15.014,44 | 35.607 |
| 99 | MANTIDO | None | 2.886.704 | 37.181.415.373,23 | 149.210 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 350.908.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 149.210 | 1,00 | 500 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 1.133.251 | 13.426.996.930,88 |
| CONCORRÊNCIA | 20.944 | 7.252.288.307,16 |
| OUTROS/NÃO APLICÁVEL | 164.537 | 5.678.625.619,69 |
| DISPENSA DE LICITAÇÃO | 1.403.372 | 5.149.857.839,64 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 73.697 | 2.042.842.245,65 |
| TOMADA DE PREÇOS | 25.408 | 1.557.496.020,47 |
| INEXIGÍVEL | 25.495 | 1.181.824.947,72 |
| CONVITE | 39.287 | 575.611.119,97 |
| RDC | 182 | 310.132.488,68 |
| CONCURSO | 530 | 5.739.285,67 |
| Leilão | 1 | 567,70 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 253 | 698.516.152,83 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 210 | 351.817.523,72 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 343 | 255.963.520,98 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 24 | 239.116.357,85 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 30 | 227.175.321,13 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 25 | 202.856.500,37 |
| 02558157000162 | N-TELEFONICA BRASIL S.A. | Serviços de telecomunicações sem fio não especificados anteriormente | 604 | 160.677.875,22 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 68 | 109.260.706,87 |
| 53859112000169 | CIA JAGUARI DE ENERGIA | Distribuição de energia elétrica | 31 | 49.233.563,31 |
| 46682761000171 | COMPANHIA DE DESENVOLVIMENTO DE GUARATINGUETA - CODESG | Gestão de redes de esgoto | 1 | 23.883.489,62 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 23.586.940,01 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 12 | 18.637.720,07 |
| 02302100001684 | EDP SAO PAULO DISTRIBUICAO DE ENERGIA S.A. | Distribuição de energia elétrica | 1 | 18.478.756,00 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 207 | 14.524.682,13 |
| 43776517031905 | COMPANHIA DE SANEAMENTO BÁSICO DO ESTADO DE SAO PAULO SABESP | Captação, tratamento e distribuição de água | 1 | 12.874.499,75 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 00965345 | ASSOCIAÇÃO COMERCIAL E EMPRESARIAL DE ECP. | Atividades de associações de defesa de direitos sociais | 13 | 13 | 1.187.150,00 |
| 27509356 | RVM DE SOUZA ME | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 76 | 76 | 1.176.286,67 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 111 | 144 | 578.814,76 |
| 07275201 | MENDES ESPINHA E MENDES ESPINHA LTDA-EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 202 | 263 | 490.945,21 |
| 53913075 | SUPERMERCADO RASTELAO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 48 | 58 | 460.073,89 |
| 02581032 | KATIA REGINA MARTINUCI DE OLIVEIRA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 87 | 133 | 435.355,33 |
| 07993190 | ESPINHA E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 214 | 305 | 364.027,25 |
| 03354724 | PAVONI E SALAZAR SUPERMERCADOS LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 47 | 50 | 352.012,07 |
| 04439875 | VIAZUL TOUR LTDA | Atividades de intermediação e agenciamento de serviços e negócios em geral, exceto imobiliários | 127 | 225 | 350.109,52 |
| 07122631 | CARV DA SILVA E ROD SUPERM LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 81 | 116 | 335.701,88 |
| 03451241 | ASPUMC-ASSOC.SERV.PUBL.MUNIC.CRUZALIA | Atividades de associações de defesa de direitos sociais | 6 | 9 | 288.973,75 |
| 47716873 | ZANATTA CIA LTDA | Serviços combinados de escritório e apoio administrativo | 79 | 136 | 189.236,64 |
| 20524113 | SUPERMERCADO NOVA PROMISSAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 33 | 48 | 152.999,73 |
| 29055993 | SINDICATO DAS EMP DE TRANP DE PASS DE B MANSA E V RED | Atividades de organizações associativas patronais e empresariais | 12 | 14 | 96.229,06 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 10 | 12 | 77.740,00 |
| 55644025 | LUIS CARLOS FERRO E CIA. LTDA. - ME | Comércio varejista de carnes - açougues | 36 | 40 | 46.167,53 |
| 31132797 | JOSEFA JOVINO FERREIRA *** | Comércio varejista de carnes - açougues | 8 | 10 | 35.730,00 |
| 05938407 | FABIO FERNANDES ACOUGUES | Comércio varejista de carnes - açougues | 71 | 78 | 22.855,46 |
| 00010639 | ANTONIO CARLOS QUINTINO ME | Comércio varejista de carnes - açougues | 35 | 50 | 21.375,00 |
| 24208095 | MARCELO CARLOS DE SOUZA *** | Comércio varejista de gás liqüefeito de petróleo (GLP) | 54 | 107 | 18.828,01 |
| 50743913 | ALCENY GARBULLIO E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 18 | 25 | 15.825,00 |
| 22976841 | J. L. FERRAREZI ME | Comércio varejista de hortifrutigranjeiros | 41 | 58 | 14.625,00 |
| 04740792 | COOPERLOTAÇÃO - COOPERATIVA DE TRABALHO E SERV. DO TRANSPORTE RODOVIARIO ALTERNATIVO DE PASSAGEIROS | Outras atividades associativas profissionais | 4 | 5 | 14.250,00 |
| 02253775 | CASA DE CARNE SANTA EDWIGES DE ALVARO DE CAR LTDA | Comércio varejista de carnes - açougues | 61 | 61 | 10.416,36 |
| 21303181 | BUS FACIL TECNOLOGIA E SERVICOS LTDA | Outras atividades auxiliares dos transportes terrestres não especificadas anteriormente | 13 | 15 | 8.843,80 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 61699567000192 | ASSOCIACAO PAUL. PARA DESENV. MEDICINA - SPDM | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 6 | 469.963.293,76 |
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 10 | 463.263.294,87 |
| 06291846000104 | CONSTROESTE   CONSTR  E PARTIC  LTDA | Construção de rodovias e ferrovias | 165 | 183.482.778,17 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 10 | 170.032.782,78 |
| 62162847000120 | JOFEGE   PAVIMENTACAO E CONSTRUCAO LTDA | Construção de rodovias e ferrovias | 17 | 146.211.851,68 |
| 46020301000188 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Educação superior - graduação e pós-graduação | 3 | 143.728.261,96 |
| 10946361000189 | INSTITUTO DIRETRIZES | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 2 | 142.193.335,16 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 197 | 137.527.493,10 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 11 | 128.200.701,73 |
| 60003761000129 | FUND. FAC. REG. MED. S.J.RIO PRETO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 25 | 127.867.599,64 |
| 10558895000138 | NOROMIX CONCRETO  S/A | Obras de urbanização - ruas, praças e calçadas | 143 | 121.096.217,31 |
| 10541089000157 | ESTRE SPI AMBIENTAL S A | Coleta de resíduos não-perigosos | 23 | 115.550.145,60 |
| 05497348000150 | TRAIL INFRAESTRUTURA LTDA | Construção de rodovias e ferrovias | 4 | 114.737.267,67 |
| 09445502000109 | SOLUCOES SERVICOS TERCEIRIZADOS   EIRELI | Limpeza em prédios e em domicílios | 18 | 114.399.214,74 |
| 09294054000181 | ECOOSASCO AMBIENTAL S A | Coleta de resíduos não-perigosos | 1 | 113.387.968,48 |
| 33412792000160 | CONSTRUTORA QUEIROZ GALVAO S A | Outras obras de engenharia civil não especificadas anteriormente | 2 | 112.448.283,42 |
| 55996615000101 | CLD CONSTRUTORA, LACOS DETETORES E ELETRONICA LTDA | Construção de edifícios | 6 | 111.685.487,28 |
| 09033330000158 | COMPEC GALASSO ENG E CONST LTDA | Outras obras de engenharia civil não especificadas anteriormente | 9 | 110.707.947,54 |
| 19224814000138 | CONSORCIO RENOVA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 103.482.343,09 |
| 33507785000142 | CONSORCIO SAO BERNARDO AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 102.627.163,75 |
| 61600839000155 | C.I.E.E. CENTRO DE INTEG. EMPRESA ESCOLA | Serviços de assistência social sem alojamento | 381 | 101.449.144,78 |
| 02666114000109 | MICLEAN COMERCIOS E SERVICOS LTDA | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 10 | 98.936.015,32 |
| 61584223000138 | CONSTRUCAP - CCPS ENGENHARIA E COMÉRCIO S/A | Construção de edifícios | 1 | 97.347.556,93 |
| 03829424000151 | PLANETA EDUCACAO GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 3 | 94.160.711,14 |
| 17851447000177 | SUSTENTARE SANEAMENTO S.A. | Coleta de resíduos não-perigosos | 4 | 91.954.200,42 |
| 45383106000150 | IRMANDADE DA SANTA CASA DE MISERICORDIA DE BIRIGUI | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 10 | 91.814.097,13 |
| 71485056000121 | IRMANDADE DA SANTA CASA DE MISER. SOROCABA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 91.810.237,44 |
| 22315713000187 | INSTITUTO SOCIAL HOSPITAL ALEMÃO OSWALDO CRUZ | Serviços de assistência social sem alojamento | 1 | 90.017.639,83 |
| 08528442000117 | NUTRICIONALE   COMERCIO DE ALIMENTOS LTDA | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 308 | 87.429.584,45 |
| 15664292000134 | PIRACICABA AMBIENTAL SOCIEDADE ANONIMA | Coleta de resíduos não-perigosos | 1 | 87.396.016,88 |
