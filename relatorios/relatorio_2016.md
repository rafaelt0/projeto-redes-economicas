# Validação e limpeza das despesas do TCESP, 2016


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 22.068.928.
    Registros lidos: 22.068.927.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 242.032 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 236.211 | 0 | 0 |


## Codificação

O arquivo é latin-1. Na leitura, 22.998 trechos em UTF-8 foram decodificados como UTF-8
    (48 com segundo byte entre 0x80 e 0x9F, 22.950 entre 0xA0 e 0xBF) e 506 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 44 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| - ME | Item 001: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 002: | 11 |
|  1 KG.  Item 008: SAPÓLIO EM PӠ- 300 G  Item 009: TOALHA DE P | 3 |
|  1 KG.  Item 008: SAPÓLIO EM PӠ- 300 G - ME  Item 009: TOALHA | 3 |
|  1 KG.  Item 009: SAPÓLIO EM PӠ- 300 G  Item 010: TOALHA DE P | 3 |
|  50 CM  Item 004: SAPÓLIO EM PӠ- 300 G  Item 005: TOALHA DE P | 3 |
|  PVC EMBORRACHADA COR LARANJA ؽ"  RPMAQUSIÇÃO DE MATERIAIS PA | 3 |
|  PVC EMBORRACHADA COR LARANJA ؽ"AQUISIÇÃO DE MANGUEIRA PARA J | 3 |
| CIPAIS  Item 009: SAPÓLIO EM PӠ- 300 G  Item 010: VASSOURA RE | 3 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Pago | 7.692.332 | 97.082.185.589,63 |
| Valor Liquidado | 7.448.364 | 103.122.635.404,94 |
| Empenhado | 6.273.519 | 119.009.887.531,53 |
| Anulação | 597.495 | 15.932.568.158,08 |
| Reforço | 57.217 | 3.566.504.940,63 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    6.046 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.264.856 | 7.887 | 681 | 0 | 0 | 0 | 350 | 7.795 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Cosmópolis | 7.741 |
| São Carlos | 20 |
| São José do Rio Preto | 8 |
| Campo Limpo Paulista | 5 |
| Getulina | 4 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Cosmópolis | 7.832 | 183.864.848,64 |
| Ituverava | 14 | None |
| Pitangueiras | 13 | None |
| São José do Rio Preto | 10 | 126.659,39 |
| Bom Sucesso de Itararé | 2 | None |
| Cravinhos | 2 | None |
| Matão | 2 | None |
| Nova Odessa | 2 | None |


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

Órgãos distintos: 1766. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 125 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 69 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 59 | SERVIÇO ASSIST DOS FUNC E SERV MUNICIP DE BEBEDOURO |
| FUNDO | 43 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
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
| CNPJ - PESSOA JURÍDICA | 3.966.115 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1.107.643 |
| PESSOA FÍSICA | 825.346 |
| INSCRIÇÃO GENÉRICA-OUTROS | 359.943 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA AL | 4.159 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTER | 659 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 630 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 305 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 56 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 175.453 | 175.283 | 170 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 3.966.115 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2016

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%. Linhas da Receita casadas mas malformadas, ignoradas: 0.

| cnpj_basicos | achados_na_receita |
|---|---|
| 166.705 | 166.695 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)

Linhas casadas mas malformadas, ignoradas: 0.

| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 175.283 | 175.227 | 38.683 |









## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 653.737 | 14.966.127.418,86 | 54.709 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.062.950 | 36.444.747.787,59 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 7.616 | 142.250.007,13 | 135 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 320.239 | 11.447.421.510,64 | 1.339 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 58.139 | 4.915.518.606,62 | 7.298 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 172.922 | 3.956.926.861,43 | 2.036 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 333.908 | 2.217.550.988,97 | 945 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 43.701 | 1.675.082.058,03 | 259 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 126.754 | -17.774.097,69 | 35.559 |
| 99 | MANTIDO | None | 2.484.890 | 30.711.279.800,25 | 137.976 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 306.759.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 137.976 | 1,00 | 508 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 824.757 | 11.396.942.384,45 |
| CONCORRÊNCIA | 26.859 | 7.013.403.711,31 |
| OUTROS/NÃO APLICÁVEL | 214.009 | 4.367.035.309,44 |
| DISPENSA DE LICITAÇÃO | 1.256.996 | 4.038.109.900,83 |
| TOMADA DE PREÇOS | 34.682 | 1.205.480.452,96 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 42.011 | 979.646.482,65 |
| INEXIGÍVEL | 19.030 | 881.512.765,90 |
| CONVITE | 65.777 | 670.616.190,62 |
| CONCURSO | 659 | 118.273.081,29 |
| RDC | 110 | 40.259.520,80 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 243 | 497.591.268,46 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 207 | 276.963.691,77 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 23 | 207.968.380,25 |
| 02558157000162 | TELECOMUNICACOES DE S PAULO S A TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 586 | 206.350.012,85 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 333 | 188.527.162,29 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 25 | 187.248.361,10 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 30 | 179.977.765,91 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 25 | 35.782.643,94 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 22 | 33.627.340,72 |
| 07297359000111 | E.D.E. VALE PARANAPANEMA S/A. | Distribuição de energia elétrica | 27 | 31.845.663,49 |
| 61416244000144 | C. N. E. E. | Distribuição de energia elétrica | 15 | 21.073.429,13 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 19.394.806,31 |
| 90400888000142 | BANCO  SANTANDER | Bancos múltiplos, com carteira comercial | 175 | 17.863.052,80 |
| 02302100001684 | EDP SAO PAULO DISTRIBUICAO DE ENERGIA S.A. | Distribuição de energia elétrica | 1 | 16.208.383,86 |
| 01778972000174 | AMERICA NET LTDA | Serviços de telefonia fixa comutada - STFC | 10 | 16.004.152,03 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 47361100 | JUCO -  JUVENTUDE CÍVICA DE OSASCO | Atividades de associações de defesa de direitos sociais | 9 | 11 | 3.417.108,74 |
| 04875903 | ASSOCIAÇÃO ANJOS DA GUARDA MIRIM DE OSASCO - AA G MIRIM | Atividades de associações de defesa de direitos sociais | 6 | 7 | 954.032,46 |
| 13385811 | HC DO VALE TRANSPORTES LTDA ME | Transporte rodoviário de carga, exceto produtos perigosos e mudanças, intermunicipal, interestadual e internacional | 8 | 15 | 772.212,28 |
| 02581032 | KATIA REGINA MARTINUCCI DE OLIVEIRA-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 152 | 167 | 698.583,42 |
| 07275201 | MENDES ESPINHA E MENDES ESPINHA LTDA-EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 211 | 383 | 414.819,15 |
| 07993190 | ESPINHA E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 220 | 400 | 388.625,55 |
| 06554998 | DROGARIA SAO RAFAEL DE ALVARO DE CARVALHO - ME | Comércio varejista de produtos farmacêuticos, sem manipulação de fórmulas | 129 | 199 | 377.302,08 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 119 | 156 | 274.062,33 |
| 07559337 | SIMCRED CONVENIOS LTDA | Administração de cartões de crédito | 27 | 29 | 259.131,15 |
| 01564249 | DANIEL H. MARINELLI VERA CRUZ | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 13 | 15 | 256.952,08 |
| 07122631 | CARVALHO DA SILVA E RODRIGUES SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 106 | 110 | 195.915,00 |
| 45056793 | BARCAS DE SANTOS-GUARUJA S/C LTDA | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 32 | 32 | 167.476,10 |
| 67191700 | EDUARDO CARLOS BONACI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 36 | 38 | 163.486,90 |
| 08025537 | ADILSON LIMA DOS SANTOS TRANSPORTES ME | Comércio atacadista de sementes, flores, plantas e gramas | 5 | 7 | 146.296,00 |
| 00010639 | ANTONIO CARLOS QUINTINO - ME | Comércio varejista de carnes - açougues | 106 | 110 | 119.940,00 |
| 08655788 | BENEFICIO CERTO LTDA  ME | Atividades de intermediação e agenciamento de serviços e negócios em geral, exceto imobiliários | 13 | 14 | 102.527,97 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 11 | 12 | 90.620,00 |
| 29055993 | SINDICATO DAS EMP DE TRANP DE PASS DE B MANSA E V RED | Atividades de organizações associativas patronais e empresariais | 10 | 10 | 82.162,25 |
| 24185821 | MARISA PESSOA BATISTA - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 13 | 51.466,64 |
| 15547455 | COMPUSOFT SOLUCOES EM INFORMACOES LTDA M | Desenvolvimento de programas de computador sob encomenda | 7 | 10 | 50.000,00 |
| 17001663 | JULIO CESAR DA SILVA E LOPES LTDA ME | Comércio varejista de carnes - açougues | 14 | 14 | 33.240,00 |
| 09625409 | EDGAR DA SILVA EMPORIO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 13 | 14 | 30.213,00 |
| 17139426 | J.W.T. DONAIRE - ME | Comércio varejista de carnes - açougues | 10 | 11 | 29.440,00 |
| 05938407 | FABIO FERNANDES ACOUGUES-ME | Comércio varejista de carnes - açougues | 99 | 108 | 26.401,80 |
| 50743913 | ALCENY GARBULLIO E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 39 | 39 | 20.160,00 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 8 | 344.857.443,29 |
| 61699567000192 | SPDM - ASSOC. PAULISTA P/ DESENV. DA MEDICINA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 4 | 203.256.155,81 |
| 60924040000151 | TB SERV.TRANSP.,LIMP.GERENC. E REC. HUM. LTDA | Locação de automóveis sem condutor | 8 | 192.265.634,92 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 9 | 163.638.183,55 |
| 00912784000205 | INSTITUTO HYGIA SAUDE E DESENVOLVIMENTO SOCIAL | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 1 | 154.295.540,17 |
| 06291846000104 | CONSTROESTE CONST  E PARTICIPACOES LTDA | Construção de rodovias e ferrovias | 107 | 151.900.921,90 |
| 16505708000134 | SBC VALORIZACAO DE RESIDUOS SA | Coleta de resíduos não-perigosos | 1 | 147.863.071,72 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 175 | 146.479.728,95 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 13 | 130.984.632,39 |
| 46020301000188 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Educação superior - graduação e pós-graduação | 3 | 124.613.888,03 |
| 10541089000157 | ESTRE SPI AMBIENTAL S.A. | Coleta de resíduos não-perigosos | 9 | 111.646.320,42 |
| 56419492000109 | WORKS CONSTRUCAO & SERVICOS LTDA. | Treinamento em desenvolvimento profissional e gerencial | 4 | 100.276.853,82 |
| 55996615000101 | CLD CONSTRUTORA LACOS DETENTORES ELETRONICA LTDA | Construção de edifícios | 6 | 99.162.406,34 |
| 48096044000193 | DEMAX SERVICOS E COMERCIO LTDA | Limpeza em prédios e em domicílios | 9 | 95.564.935,26 |
| 08528442000117 | NUTRICIONALE   COMERCIO DE ALIMENTOS LTDA | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 327 | 90.239.223,21 |
| 19224814000138 | CONSORCIO RENOVA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 88.930.135,06 |
| 19478960000190 | CONSORCIO CENTRO SECO | Serviços especializados para construção não especificados anteriormente | 1 | 88.654.487,47 |
| 60166832000104 | APETECE SISTEMAS DE ALIMENTACAO S.A. | Fornecimento de alimentos preparados preponderantemente para empresas | 4 | 88.636.657,22 |
| 09294054000181 | ECOOSASCO AMBIENTAL S/A | Coleta de resíduos não-perigosos | 1 | 87.180.595,03 |
| 03829424000151 | PLANETA EDUCACAO GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 7 | 86.412.482,66 |
| 09095412000127 | ABBC   ASSOCIACAO BRASILEIRA DE BENEFICENCIA COMUNITARIA   UPA | Atividades associativas não especificadas anteriormente | 8 | 85.539.659,85 |
| 24232886000167 | PRO SAUDE  ASSOCIACAO BENEFICENTE DE ASSISTENCIA S | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 4 | 84.750.487,44 |
| 44690238000161 | IRMANDADE DA SANTA CASA DE MISERICORDIA DE BARIRI | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 6 | 84.398.410,28 |
| 31733363000755 | CORPUS SANEAMENTO E OBRAS LTDA | Coleta de resíduos não-perigosos | 1 | 84.268.598,65 |
| 61836813000100 | QUITAUNA SERVICOS LTDA | Coleta de resíduos não-perigosos | 1 | 83.939.638,36 |
| 61704052000133 | BETA CLEAN  SERVICE LTDA | Limpeza em prédios e em domicílios | 6 | 80.297.419,20 |
| 22217580000106 | CONSORCIO VIARIO MOGI | Construção de rodovias e ferrovias | 1 | 77.660.500,99 |
| 61980272000190 | S H A  COMÉRCIO DE ALIMENTOS LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 9 | 74.246.027,80 |
| 02666114000109 | MILCLEAN COM. E SERVIÇOS LTDA. | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 11 | 73.935.990,88 |
| 12162177000173 | COLEPAV AMBIENTAL LTDA | Coleta de resíduos não-perigosos | 3 | 72.208.259,94 |
