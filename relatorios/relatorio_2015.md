# Validação e limpeza das despesas do TCESP, 2015


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 22.102.492.
    Registros lidos: 22.102.491.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 259.603 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2.230.465 | 0 | 0 |


## Codificação

O arquivo é latin-1. Na leitura, 17.891 trechos em UTF-8 foram decodificados como UTF-8
    (0 com segundo byte entre 0x80 e 0x9F, 17.891 entre 0xA0 e 0xBF) e 21 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 36 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| L 30 UI,BIOTINA 30 MCG,ÁCIDO FӴLICO 1 MG,ÁCIDO PANTOTÊNICO 10 | 12 |
| - ME | Item 001: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 002: | 6 |
|  002: EXTRATO ETANÓLICO DAS RAʹZES DE PELARGONIUM SIDOIDES D. | 3 |
|  007: EXTRATO ETANÓLICO DAS RAʹZES DE PELARGONIUM SIDOIDES D. | 3 |
| 900ML  Item 006: FERMENTO EM PӠ- EMBALAGE | 3 |
| TAL,VÁLVULA DE ESCAPE,ESTETOSCӴPIO SIMPLES | 3 |
| UPA,MANGUEIRA DE INNMETRO E SAʹDA DÁGUA,MANUAL EM PORTUGUÊS,1 | 3 |
| WS 8.1 PROFESSIONAL ORIGINAL MʹDIA PORTUGUÊS.  Item 002: NOBR | 3 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Pago | 7.681.587 | 89.879.266.770,23 |
| Valor Liquidado | 7.452.624 | 95.556.971.034,93 |
| Empenhado | 6.331.871 | 110.826.294.676,13 |
| Anulação | 589.700 | 14.112.404.161,40 |
| Reforço | 46.709 | 3.055.857.193,58 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    14.199 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.329.901 | 214 | 1.551 | 0 | 3 | 0 | 1.059 | 130 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Matão | 18 |
| Cubatão | 17 |
| São Caetano do Sul | 15 |
| Pompéia | 13 |
| Espírito Santo do Pinhal | 10 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Espírito Santo do Pinhal | 155 | 351.760,94 |
| Araçatuba | 11 | None |
| Brotas | 5 | None |
| Ribeira | 5 | 10.219,00 |
| Santos | 4 | 29.861,41 |
| Buri | 3 | 8.995,15 |
| Cosmópolis | 3 | None |
| São José do Rio Preto | 3 | 425.954,00 |


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

Órgãos distintos: 1765. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 124 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 68 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 59 | SERVICO DE AGUA E ESGOTO DO MUNICIPIO DE JAU |
| FUNDO | 44 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AGENCIA | 10 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| AUTARQUIA | 8 | AUTARQUIA DE ESPORTE DE ASSIS |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| EMPRESA | 7 | EMPRESA DE DESENVOLVIMENTO URBANO E SOCIAL DE SOROCABA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 6 | SAAE - AMBIENTE |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 4.041.545 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1.059.622 |
| PESSOA FÍSICA | 830.399 |
| INSCRIÇÃO GENÉRICA-OUTROS | 387.878 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 4.095 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 3.914 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 2.139 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 247 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 62 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 179.199 | 179.010 | 189 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.041.545 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2015

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%. Linhas da Receita casadas mas malformadas, ignoradas: 0.

| cnpj_basicos | achados_na_receita |
|---|---|
| 170.089 | 170.078 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)

Linhas casadas mas malformadas, ignoradas: 0.

| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 179.010 | 178.953 | 42.169 |










## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 661.605 | 13.558.884.011,93 | 55.952 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.052.424 | 33.983.759.609,06 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 7.174 | 126.431.990,28 | 145 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 314.746 | 10.801.732.935,31 | 1.297 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 57.844 | 4.399.471.442,01 | 7.405 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 169.159 | 3.833.424.346,76 | 2.110 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 342.184 | 2.117.245.830,60 | 903 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 42.152 | 1.514.361.330,43 | 254 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 133.514 | -2.419,00 | 37.415 |
| 99 | MANTIDO | None | 2.549.099 | 29.433.676.067,43 | 142.125 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 323.883.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 142.125 | 1,00 | 524 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 812.601 | 10.809.112.126,34 |
| CONCORRÊNCIA | 29.466 | 6.656.080.484,12 |
| OUTROS/NÃO APLICÁVEL | 227.742 | 4.114.095.235,50 |
| DISPENSA DE LICITAÇÃO | 1.310.339 | 4.095.303.089,18 |
| TOMADA DE PREÇOS | 34.055 | 1.217.769.370,09 |
| CONVITE | 80.476 | 914.520.634,75 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 35.018 | 758.866.900,59 |
| INEXIGÍVEL | 18.377 | 750.350.806,97 |
| CONCURSO | 897 | 105.354.852,68 |
| RDC | 128 | 12.222.567,21 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 245 | 483.944.808,49 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 209 | 285.400.740,08 |
| 02558157000162 | TELECOMUNICACOES DE S PAULO S A TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 586 | 225.866.155,48 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 23 | 200.413.328,21 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 31 | 171.300.143,11 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 25 | 154.971.039,40 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 333 | 154.343.658,56 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 25 | 32.744.914,16 |
| 07297359000111 | E.D.E. VALE PARANAPANEMA S/A. | Distribuição de energia elétrica | 27 | 31.777.901,99 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 22 | 29.995.065,85 |
| 61416244000144 | C. N. E. E. | Distribuição de energia elétrica | 15 | 22.510.890,76 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 20.534.787,27 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 169 | 17.077.819,14 |
| 01778972000174 | AMERICA NET LTDA | Serviços de telefonia fixa comutada - STFC | 9 | 15.303.812,38 |
| 02302100001684 | EDP SAO PAULO DISTRIBUICAO DE ENERGIA S.A. | Distribuição de energia elétrica | 1 | 15.251.929,89 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 47361100 | JUCO -  JUVENTUDE CÍVICA DE OSASCO | Atividades de associações de defesa de direitos sociais | 10 | 15 | 3.919.248,11 |
| 02581032 | KATIA REGINA MARTINUCI DE OLIVEIRA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 119 | 160 | 363.410,27 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 88 | 109 | 275.034,09 |
| 01564249 | DANIEL H. MARINELLI VERA CRUZ | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 13 | 17 | 274.731,58 |
| 49041353 | SUPERMERCADO BELOTO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 207 | 401 | 265.668,11 |
| 00010639 | ANTONIO CARLOS QUINTINO - ME | Comércio varejista de carnes - açougues | 103 | 127 | 223.948,50 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 88 | 144 | 218.626,96 |
| 07122631 | CARVALHO DA SILVA E RODRIGUES SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 100 | 114 | 213.900,00 |
| 67191700 | EDUARDO CARLOS BONACI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 36 | 43 | 123.563,35 |
| 09274132 | NOGUEIRA E LEONEL LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 101 | 111 | 104.501,22 |
| 59464537 | A FONTANEZI CABRALIA PAULISTA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 131 | 139 | 104.050,85 |
| 06129146 | CRISTOVAO ALBARRACIM FILHO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 21 | 21 | 96.520,00 |
| 60780889 | MARIA ODETE CHECHETTO BERTINOTTI ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 64 | 87 | 93.707,43 |
| 19370743 | ASSOC. DAS EMPRESAS TRANSP. COLET. DE LIMEIRA | Atividades de organizações associativas patronais e empresariais | 31 | 36 | 85.915,70 |
| 11641519 | GERSON PFISTER BARUQUE | Comércio varejista de carnes - açougues | 171 | 294 | 72.376,39 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 10 | 11 | 59.660,00 |
| 19895581 | R. L. PARRILHA SUPERMERCADO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 55 | 97 | 57.456,75 |
| 17139426 | J.W.T. DONAIRE - ME | Comércio varejista de carnes - açougues | 17 | 25 | 50.700,91 |
| 17001663 | JULIO CESAR DA SILVA E LOPES LTDA ME | Comércio varejista de carnes - açougues | 13 | 13 | 38.700,00 |
| 09625409 | EDGAR DA SILVA EMPORIO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 13 | 13 | 36.420,00 |
| 56160203 | ANDREY APARECIDO GARBULIO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 62 | 62 | 33.980,00 |
| 01894316 | ELIZEU GERVASIO ACOUGUE ME | Comércio varejista de carnes - açougues | 57 | 57 | 32.440,00 |
| 60237229 | JOSE ANTONIO AGOSTINHO -ME | Serviços de reservas e outros serviços de turismo não especificados anteriormente | 17 | 24 | 23.497,80 |
| 50743913 | ALCENY GARBULLIO E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 21 | 29 | 18.198,00 |
| 08594304 | ANTONIO RENALDO SPEDO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 5 | 6 | 15.639,60 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 9 | 326.467.314,48 |
| 61699567000192 | SECRETARIA DE ESTADO DA SAUDE | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 5 | 278.083.143,86 |
| 60924040000151 | TB SERVICOS TRANSP LIMP GER E REC.HUMANOS S.A | Locação de automóveis sem condutor | 7 | 187.457.574,47 |
| 06291846000104 | CONSTROESTE CONST  E PARTICIPACOES LTDA | Construção de rodovias e ferrovias | 103 | 184.247.248,73 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 9 | 149.238.905,41 |
| 16505708000134 | SBC VALORIZACAO DE RESIDUOS SA | Coleta de resíduos não-perigosos | 1 | 142.128.000,00 |
| 00912784000205 | INSTITUTO HYGIA SAUDE E DESENVOLVIMENTO SOCIAL | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 1 | 140.045.416,54 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 176 | 133.296.626,75 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 14 | 128.198.595,28 |
| 10541089000157 | AZALEIA EMPREENDIMENTOS E PARTICIPACOES S A | Coleta de resíduos não-perigosos | 16 | 121.144.500,52 |
| 44164606000138 | ERJ ADM E RESTAURANTES DE EMPRESAS LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 9 | 118.591.071,83 |
| 61836813000100 | QUITAUNA SERVICOS LTDA | Coleta de resíduos não-perigosos | 1 | 114.343.725,29 |
| 46020301000188 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Educação superior - graduação e pós-graduação | 2 | 110.775.098,71 |
| 55996615000101 | CONSLADEL - CONSTE LD ELETRONICA LTDA | Construção de edifícios | 6 | 103.605.448,40 |
| 08528442000117 | NUTRICIONALE   COMERCIO DE ALIMENTOS LTDA | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 335 | 96.545.965,59 |
| 19224814000138 | CONSORCIO RENOVA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 89.522.771,26 |
| 07229374000122 | INST. CORPORE PARA O DESENV. DA QUALIDADE DE VIDA | Atividades de profissionais da área de saúde não especificadas anteriormente | 9 | 88.863.273,92 |
| 56419492000109 | WORKS CONSTRUCAO & SERVICOS LTDA. | Treinamento em desenvolvimento profissional e gerencial | 4 | 84.120.551,16 |
| 67729178000491 | COM. CIR. RIOCLARENSE LTDA | Comércio atacadista de medicamentos e drogas de uso humano | 500 | 83.222.783,20 |
| 03829424000151 | PLANETA EDUCACAO  GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 11 | 78.194.831,45 |
| 24232886000167 | PRO SAUDE  ASSOCIACAO BENEFICENTE DE ASSISTENCIA S | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 3 | 77.610.302,32 |
| 12162177000173 | COLEPAV AMBIENTAL LTDA | Coleta de resíduos não-perigosos | 3 | 75.002.562,07 |
| 15664292000134 | PIRACICABA AMBIENTAL SOCIEDADE ANONIMA | Coleta de resíduos não-perigosos | 1 | 69.307.402,29 |
| 31733363000755 | CORPUS SANEAMENTO E OBRAS LTDA | Coleta de resíduos não-perigosos | 1 | 69.231.906,38 |
| 09095412000127 | ABBC   ASSOCIACAO BRASILEIRA DE BENEFICENCIA COMUNITARIA   UPA | Atividades associativas não especificadas anteriormente | 5 | 68.314.828,92 |
| 43677822000114 | SOEBE CONSTRUCAO E PAVIMENTACAO LTDA | Construção de rodovias e ferrovias | 7 | 67.559.468,76 |
| 00029160000163 | AGRO COMERCIAL DA VARGEM LTDA | Comércio atacadista de mercadorias em geral, com predominância de produtos alimentícios | 23 | 67.077.620,67 |
| 09294054000181 | ECOOSASCO AMBIENTAL S/A | Coleta de resíduos não-perigosos | 1 | 66.128.250,66 |
| 62719083000120 | PIONEIRA SANEAMENTO E LIMP URBANA LTDA | Coleta de resíduos não-perigosos | 13 | 65.478.911,35 |
| 66806555000133 | FBS - CONSTRUCAO CIVIL E PAVIMENTACAO LTDA | Construção de rodovias e ferrovias | 6 | 64.274.544,90 |
