# Validação e limpeza das despesas do TCESP, 2017


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 22.304.867.
    Registros lidos: 22.304.866.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 239.655 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 48.825 | 0 | 0 |


## Codificação

O arquivo é latin-1. Na leitura, 19.491 trechos em UTF-8 foram decodificados como UTF-8
    (39 com segundo byte entre 0x80 e 0x9F, 19.452 entre 0xA0 e 0xBF) e 810 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 68 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| 900ML  Item 004: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 005: | 15 |
|  1 LT  Item 003: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 004: | 12 |
|  500G  Item 004: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 005: | 3 |
|  500G  Item 006: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 0 | 3 |
|  EPP | Item 001: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 002: | 3 |
|  GEGE  Item 002: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: ROYA | 3 |
| 900ML  Item 005: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 006: | 3 |
| 900ML  Item 006: FERMENTO EM PӠ- EMBALAGE | 3 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Pago | 7.758.602 | 98.749.341.978,43 |
| Valor Liquidado | 7.491.352 | 104.035.093.162,47 |
| Empenhado | 6.387.301 | 116.092.654.892,48 |
| Anulação | 596.043 | 13.790.187.429,56 |
| Reforço | 71.568 | 5.221.525.272,97 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    5.831 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.386.449 | 29 | 605 | 0 | 0 | 0 | 283 | 36 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| São José do Rio Preto | 11 |
| Pirassununga | 9 |
| Santo Antônio do Aracanguá | 9 |
| Mogi Guaçu | 2 |
| São Sebastião | 2 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| São José do Rio Preto | 11 | 131.964,15 |
| Chavantes | 2 | None |
| Itatiba | 2 | None |
| Ituverava | 2 | None |
| Nova Odessa | 2 | None |
| Pitangueiras | 2 | None |
| São Sebastião | 2 | 1.455,32 |
| Bernardino de Campos | 1 | None |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|


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

Órgãos distintos: 1763. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 125 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 67 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 57 | SERVIÇO ASSIST DOS FUNC E SERV MUNICIP DE BEBEDOURO |
| FUNDO | 44 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AGENCIA | 10 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| AUTARQUIA | 8 | AUTARQUIA DE ESPORTE DE ASSIS |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| EMPRESA | 8 | EMPRESA DE DESENVOLVIMENTO URBANO E SOCIAL DE SOROCABA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 6 | SAAE - AMBIENTE |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 4.108.966 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1.127.651 |
| PESSOA FÍSICA | 813.689 |
| INSCRIÇÃO GENÉRICA-OUTROS | 329.383 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA AL | 5.539 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTER | 623 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 480 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 76 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 42 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 181.795 | 181.661 | 134 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.108.966 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2017

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.

| cnpj_basicos | achados_na_receita |
|---|---|
| 173.042 | 173.034 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)


| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 181.661 | 181.611 | 36.812 |








## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 655.974 | 16.138.945.961,55 | 56.788 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.043.029 | 37.867.227.409,22 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 8.152 | 139.437.599,84 | 104 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 328.531 | 12.035.254.108,73 | 1.269 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 53.612 | 5.196.745.672,17 | 6.807 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 186.067 | 4.120.552.901,02 | 2.102 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 326.019 | 2.192.051.448,95 | 922 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 45.770 | 1.827.398.966,81 | 273 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 122.638 | -119.340,25 | 36.514 |
| 99 | MANTIDO | None | 2.616.657 | 28.006.430.850,99 | 144.453 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 328.934.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 144.453 | 1,00 | 508 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 915.661 | 10.808.827.413,81 |
| CONCORRÊNCIA | 24.068 | 5.359.745.491,95 |
| OUTROS/NÃO APLICÁVEL | 190.963 | 4.264.795.936,34 |
| DISPENSA DE LICITAÇÃO | 1.339.782 | 4.212.686.886,44 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 47.737 | 1.057.228.407,40 |
| INEXIGÍVEL | 21.071 | 995.627.692,21 |
| TOMADA DE PREÇOS | 27.918 | 704.850.499,48 |
| CONVITE | 48.938 | 447.871.672,18 |
| CONCURSO | 377 | 126.946.260,71 |
| RDC | 141 | 27.843.590,47 |
| Leilão | 1 | 7.000,00 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 243 | 539.489.990,10 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 208 | 265.519.190,70 |
| 43776517000180 | CETESB COMPANHIA AMBIENTAL DO ESTADO DE SAO PAULO | Captação, tratamento e distribuição de água | 335 | 207.122.674,36 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 23 | 199.912.684,00 |
| 02558157000162 | TELECOMUNICACOES DE S PAULO S A TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 598 | 190.862.057,78 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 30 | 170.218.000,71 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 25 | 153.195.599,38 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 56 | 48.553.653,62 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 25 | 34.994.131,69 |
| 07297359000111 | E.D.E. VALE PARANAPANEMA S/A. | Distribuição de energia elétrica | 27 | 24.053.391,00 |
| 90400888000142 | BANCO  SANTANDER | Bancos múltiplos, com carteira comercial | 198 | 23.197.323,53 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 20.125.822,29 |
| 61416244000144 | C. N. E. E. | Distribuição de energia elétrica | 15 | 18.482.485,92 |
| 02302100001684 | EDP SAO PAULO DISTRIBUICAO DE ENERGIA S.A. | Distribuição de energia elétrica | 1 | 14.617.686,58 |
| 01778972000174 | AMERICA NET LTDA | Serviços de telefonia fixa comutada - STFC | 11 | 13.168.542,69 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 04875903 | ASSOCIAÇÃO ANJOS DA GUARDA MIRIM DE OSASCO - AA G MIRIM | Atividades de associações de defesa de direitos sociais | 8 | 9 | 1.477.976,43 |
| 07693267 | CASTELLUCCI FIGUEIREDO E ADVOGADOS ASSOCIADOS | Serviços advocatícios | 10 | 19 | 1.346.675,00 |
| 03354724 | PAVONI E SALAZAR SUPERMERCADOS LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 53 | 72 | 741.517,79 |
| 06554998 | DROGARIA SAO RAFAEL DE ALVARO DE CARVALHO - ME | Comércio varejista de produtos farmacêuticos, sem manipulação de fórmulas | 114 | 213 | 648.442,75 |
| 02581032 | KATIA REGINA MARTINUCCI DE OLIVEIRA - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 154 | 157 | 608.081,95 |
| 13385811 | HC DO VALE TRANSPORTES LTDA ME | Transporte rodoviário de carga, exceto produtos perigosos e mudanças, intermunicipal, interestadual e internacional | 8 | 15 | 498.755,89 |
| 07275201 | MENDES ESPINHA E MENDES ESPINHA LTDA-EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 211 | 393 | 381.493,70 |
| 07993190 | ESPINHA E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 232 | 388 | 374.754,49 |
| 07122631 | CARVALHO DA SILVA E RODRIGUES SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 145 | 145 | 353.190,00 |
| 07559337 | SIMCRED CONVENIOS LTDA | Administração de cartões de crédito | 38 | 42 | 329.588,23 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 117 | 118 | 250.857,60 |
| 27509356 | RVM DE SOUZA ME | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 12 | 12 | 242.205,78 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 118 | 159 | 218.833,02 |
| 20524113 | SUPERMERCADO NOVA PROMISSAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 26 | 46 | 193.400,37 |
| 67191700 | EDUARDO CARLOS BONACI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 36 | 57 | 182.252,95 |
| 08655788 | BENEFICIO CERTO LTDA  ME | Atividades de intermediação e agenciamento de serviços e negócios em geral, exceto imobiliários | 13 | 13 | 118.893,38 |
| 45056793 | BARCAS DE SANTOS-GUARUJA S/C LTDA | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 9 | 9 | 113.041,00 |
| 29055993 | SINDICATO DAS EMP DE TRANP DE PASS DE B MANSA E V RED | Atividades de organizações associativas patronais e empresariais | 11 | 11 | 104.664,07 |
| 05938407 | FABIO FERNANDES ACOUGUES-ME | Comércio varejista de carnes - açougues | 73 | 79 | 79.460,71 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 12 | 56.810,00 |
| 16786508 | CARLOS EDUARDO BOTELHO MINIMERCADO ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 11 | 19 | 50.190,93 |
| 00010639 | ANTONIO CARLOS QUINTINO ME | Comércio varejista de carnes - açougues | 73 | 73 | 38.550,00 |
| 17837111 | GILBERTO APARECIDO MACEDO PINTO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 15 | 34.963,40 |
| 60237229 | JOSE ANTONIO AGOSTINHO -ME | Serviços de reservas e outros serviços de turismo não especificados anteriormente | 30 | 40 | 33.755,90 |
| 55644025 | LUIS CARLOS FERRO E CIA. LTDA. - ME | Comércio varejista de carnes - açougues | 18 | 33 | 30.627,44 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 10 | 345.736.560,13 |
| 61699567000192 | SPDM - ASSOC. PAULISTA P/ DESENV. DA MEDICINA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 3 | 215.090.102,69 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 200 | 160.193.872,61 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 9 | 147.420.671,70 |
| 06291846000104 | CONSTROESTE   CONSTR  E PARTIC  LTDA | Construção de rodovias e ferrovias | 150 | 144.987.673,32 |
| 44690238000161 | IRMANDADE DA SANTA CASA DE MISERICORDIA DE BARIRI | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 7 | 134.808.981,67 |
| 10541089000157 | ESTRE SPI AMBIENTAL S A | Coleta de resíduos não-perigosos | 11 | 132.838.852,11 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 12 | 124.955.554,75 |
| 46020301000188 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Educação superior - graduação e pós-graduação | 2 | 122.581.731,03 |
| 14963977000119 | INSTITUTO GERIR | Atividades associativas não especificadas anteriormente | 2 | 106.660.005,30 |
| 19224814000138 | CONSORCIO RENOVA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 105.225.236,75 |
| 55996615000101 | CONSLADEL - CONSTE LD ELETRONICA LTDA | Construção de edifícios | 5 | 96.939.759,04 |
| 09095412000127 | ABBC   ASSOCIACAO BRASILEIRA DE BENEFICENCIA COMUNITARIA   UPA | Atividades associativas não especificadas anteriormente | 9 | 96.138.709,91 |
| 16505708000134 | SBC VALORIZACAO DE RESIDUOS SA | Coleta de resíduos não-perigosos | 1 | 94.537.990,28 |
| 03829424000151 | PLANETA EDUCACAO GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 6 | 93.827.664,21 |
| 67729178000491 | COM. CIR. RIOCLARENSE LTDA | Comércio atacadista de medicamentos e drogas de uso humano | 508 | 85.927.249,28 |
| 15664292000134 | PIRACICABA AMBIENTAL SOCIEDADE ANONIMA | Coleta de resíduos não-perigosos | 1 | 84.079.425,79 |
| 50668722000944 | PROACTIVA MEIO AMBIENTE BRASIL LTDA | Tratamento e disposição de resíduos perigosos | 1 | 84.051.547,61 |
| 48096044000193 | DEMAX SERVICOS E COMERCIO LTDA | Limpeza em prédios e em domicílios | 10 | 83.880.141,58 |
| 09294054000181 | ECOOSASCO AMBIENTAL S/A | Coleta de resíduos não-perigosos | 1 | 83.483.747,55 |
| 08528442000117 | NUTRICIONALE   COMERCIO DE ALIMENTOS LTDA | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 305 | 82.257.363,45 |
| 02666114000109 | MILCLEAN COMERCIO E SERVICOS LTDA | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 11 | 82.063.582,01 |
| 60924040000151 | TB SERV.TRANSP.,LIMP.GERENC. E REC. HUM. LTDA | Locação de automóveis sem condutor | 7 | 79.597.219,50 |
| 61836813000100 | QUITAUNA SERVICOS LTDA | Coleta de resíduos não-perigosos | 1 | 78.912.613,82 |
| 62719083000120 | PIONEIRA SANEAMENTO E LIMP URBANA LTDA | Coleta de resíduos não-perigosos | 10 | 76.065.624,96 |
| 00405527000104 | MONTE AZUL ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 24 | 74.108.902,40 |
| 61980272000190 | S H A COMERCIO DE ALIMENTOS LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 6 | 73.537.564,11 |
| 60003761000129 | FACULDADE REG.MED.DE SAO JOSE R.PRETO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 25 | 73.424.725,70 |
| 60499365000215 | FUNDACAO LEONOR DE BARROS CAMARGO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 72.371.449,78 |
| 62162847000120 | JOFEGE - Pavimentação e Construção Ltda | Construção de rodovias e ferrovias | 9 | 71.589.291,03 |
