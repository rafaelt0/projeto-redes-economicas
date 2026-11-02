# Validação e limpeza das despesas do TCESP, 2024


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 28.000.383.
    Registros lidos: 28.000.382.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 275.379 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 34 | 21 | 0 | 5 |


## Codificação

O arquivo é latin-1. Na leitura, 89.773 trechos em UTF-8 foram decodificados como UTF-8
    (333 com segundo byte entre 0x80 e 0x9F, 89.440 entre 0xA0 e 0xBF) e 1.694 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 46 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| PRIORI SERVIÇOS E SOLUÇՕES, CONTABILIDADE EIRELI | PRE | 10 |
| CAMAR  Item 003: FERMENTO EM PӠ- EMBALAGEM C/ 250GMARCA: TRIS | 9 |
| RECTH  Item 004: FERMENTO EM PӠ- EMBALAGEM C/ 250GMARCA: TRIS | 9 |
|  DE MADEIRA OU AÇO- SUPORTA ATɠ10KG. ACOMPANHA BUCHAS E PARAF | 9 |
| ALMENTE EM AÇO INOXIDÁVEL QUE ɠALTAMENTE DURÁVEL ALEM DE RESI | 3 |
| ERÂMICA, VAPOR CONSTANTE DE ATɠ35 G/MIN, VAPOR EXTRA DE 100 G | 3 |
| camar  Item 003: FERMENTO EM PӠ- EMBALAGEM C/ 250GMarca: Tris | 3 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Liquidado | 9.849.931 | 221.147.896.166,40 |
| Valor Pago | 9.736.913 | 213.137.938.369,67 |
| Empenhado | 7.626.744 | 253.460.554.546,52 |
| Anulação | 684.042 | 33.224.825.251,67 |
| Reforço | 102.752 | 9.480.071.025,30 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    6.267 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 7.625.917 | 212 | 682 | 3 | 3 | 0 | 203 | 176 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| São José do Rio Preto | 61 |
| Taubaté | 54 |
| Serrana | 30 |
| Buritama | 4 |
| Cristais Paulista | 4 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| São José do Rio Preto | 74 | 12.275.140,01 |
| Serrana | 43 | None |
| Bom Jesus dos Perdões | 40 | None |
| Cristais Paulista | 8 | 30.527,50 |
| Angatuba | 5 | None |
| Buritama | 4 | None |
| Piracicaba | 4 | 0,02 |
| São Sebastião | 4 | 3.020,00 |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.023 | 3 | 0,00 |


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

Órgãos distintos: 1738. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 127 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 63 | FUNDACAO CAIXA BENEF SERV DA UNIVERSIDADE TAUBATE |
| SERVICO | 50 | SERVICO AUTONOMO DE AGUA E ESGOTO DE SALTO - SAAE SALTO |
| FUNDO | 40 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 9 | DEPARTAMENTO AUTONOMO DE AGUA E ESGOTO |
| AGENCIA | 8 | AGENCIA MUNICIPAL DE AGUA E ESGOTO DE MARILIA-AMAE |
| AUTARQUIA | 8 | AUTARQUIA DE PREVIDÊNCIA PRÓPRIA |
| CAIXA | 8 | CAIXA APOSENTADORIA PREV SERV MUNICIPAIS DE ITATINGA |
| EMPRESA | 8 | EMPRESA DE DESENVOLVIMENTO URBANO E SOCIAL DE SOROCABA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 6 | SAAE - SERVICO AUTONOMO DE AGUA E ESGOTO |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 6.559.746 |
| PESSOA FÍSICA | 1.066.098 |
| INTERNACIONAL | 65 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 5 |
| None | 3 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 186.212 | 186.212 | 0 | None |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 6.559.746 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2024

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.

| cnpj_basicos | achados_na_receita |
|---|---|
| 178.474 | 178.465 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)


| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 186.212 | 186.185 | 13.086 |



## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 3 | 0,00 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 589.839 | 30.774.718.500,39 | 50.036 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 988.283 | 2.601.131.436,93 | 0 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 2.012.777 | 79.977.183.425,08 | 2.401 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 81.012 | 26.551.337.946,68 | 9.911 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 399.226 | 11.288.602.333,02 | 2.519 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 305.817 | 3.775.382.315,62 | 1.087 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 41.145 | 4.062.022.855,63 | 243 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 134.586 | -7.415.779,45 | 33.229 |
| 99 | MANTIDO | None | 3.073.229 | 70.680.677.854,47 | 146.111 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 366.910.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 146.111 | 1,00 | 566 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO PRESENCIAL | 1.094.273 | 21.203.676.842,82 |
| CONCORRÊNCIA | 23.347 | 19.470.803.620,80 |
| PREGÃO ELETRÔNICO | 498.788 | 12.755.242.810,81 |
| DISPENSA DE LICITAÇÃO | 1.199.365 | 7.392.106.121,41 |
| OUTROS/NÃO APLICÁVEL | 168.039 | 5.201.273.020,54 |
| INEXIGÍVEL | 57.820 | 2.345.756.597,18 |
| TOMADA DE PREÇOS | 13.012 | 1.809.814.231,39 |
| CONVITE | 17.867 | 318.423.275,88 |
| RDC | 120 | 154.181.358,03 |
| CONCURSO | 588 | 29.071.449,00 |
| Diálogo Competitivo | 7 | 324.389,27 |
| Leilão | 3 | 4.137,34 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 263 | 1.112.022.225,80 |
| 43776517000180 | BENEFICIO SOCIAL -  SABESP | Captação, tratamento e distribuição de água | 364 | 543.665.594,13 |
| 02328280000197 | BENEFICIO SOCIAL - ELEKTRO | Distribuição de energia elétrica | 217 | 463.360.343,04 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 27 | 276.713.452,32 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 23 | 251.703.507,75 |
| 02302100000106 | BANDEIRANTE ENERGIA  SA | Distribuição de energia elétrica | 30 | 213.826.286,97 |
| 07282377000120 | ENERGISA SUL - SUDESTE - DISTRIBUIDORA DE ENERGIA | Distribuição de energia elétrica | 71 | 151.129.114,64 |
| 02558157000162 | N-TELEFONICA BRASIL S.A. | Serviços de telecomunicações sem fio não especificados anteriormente | 598 | 119.488.835,69 |
| 53859112000169 | CIA JAGUARI DE ENERGIA | Distribuição de energia elétrica | 39 | 106.624.476,91 |
| 00910456000199 | AMBIENT SERVICOS AMBIENTAIS DE RP S/A | Gestão de redes de esgoto | 1 | 48.805.722,59 |
| 90400888000142 | BANCO  SANTANDER | Bancos múltiplos, com carteira comercial | 260 | 28.008.484,71 |
| 01778972000174 | AMERICA NET LTDA | Serviços de telefonia fixa comutada - STFC | 15 | 27.921.461,33 |
| 60746948000112 | BANCO BRADESCO | Bancos múltiplos, com carteira comercial | 253 | 25.451.022,79 |
| 60701190000104 | BANCO ITAU | Bancos comerciais | 130 | 18.051.346,16 |
| 02421421000111 | TIM S A | Serviços de telefonia fixa comutada - STFC | 60 | 17.171.659,42 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 67228536 | REDE DE DISTR.ZEFERINO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 375 | 375 | 6.527.829,50 |
| 11517841 | COMPANHIA SULAMERICANA DE DISTRIBUICAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 180 | 190 | 5.003.019,24 |
| 07732866 | ANTONELLI SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 124 | 147 | 4.412.514,95 |
| 56784531 | VIAÇÃO LIMA  LIMA LTDA | Transporte rodoviário de produtos perigosos | 6 | 12 | 2.531.226,98 |
| 46464962 | ASSOCIACAO COMERCIAL E EMPRESARIAL DE TUPI PAULIST | Atividades de organizações associativas patronais e empresariais | 30 | 38 | 1.852.708,12 |
| 57412660 | SUPERMERCADO DALALANA DE ITAPIRA LTDA - EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 1.745.180,21 |
| 05364327 | REDE ROFATTO DE SUPERMERCADOS LTDA | Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica | 213 | 221 | 1.425.096,99 |
| 56440027 | SUPERMERCADO PENHA CENTER LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 72 | 72 | 1.025.842,54 |
| 53913075 | SUPERMERCADO RASTELAO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 66 | 112 | 993.427,45 |
| 05727945 | SUPERMERCADO GELAIN DE ITAPIRA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 54 | 54 | 991.967,89 |
| 00965345 | ASSOCIAÇÃO COMERCIAL E EMPRESARIAL DE ECP. | Atividades de associações de defesa de direitos sociais | 8 | 8 | 833.600,00 |
| 10377432 | ALEXANDRE ARAUJO FELIX E CIA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 197 | 249 | 755.001,02 |
| 08468552 | DAVID BARBOZA SUPERMERCADO EIRELI | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 108 | 108 | 732.424,74 |
| 67693945 | TAPS DISTRIBUIDORA DE ALIMENTOS LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 157 | 204 | 607.161,58 |
| 20161546 | SUPERMERCADO MIX CENTER LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 547.199,00 |
| 67191700 | EDUARDO CARLOS BONACI | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 52 | 104 | 538.950,91 |
| 45056793 | BARCA SANTOS GUARUJA LTDA. TRANSP.MARIT.COLET | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 59 | 110 | 468.774,00 |
| 03354724 | PAVONI E SALAZAR SUPERMERCADOS LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 434.127,99 |
| 07627686 | NAIARA NOGUEIRA FERRACIOLLI EIRELI EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 75 | 80 | 346.270,60 |
| 27147045 | CRISTIELE SOUSA DUARTE - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 37 | 71 | 322.015,79 |
| 47619309 | CICERO PONTES DA SILVA E CIA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 56 | 67 | 253.295,06 |
| 20524113 | IDELFA ZONETTI LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 39 | 48 | 253.093,63 |
| 01984761 | SUPERMERCADO AURELIO DE ITAPIRA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 242.954,41 |
| 65803264 | MERCADINHO VILA IZAURA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 37 | 37 | 242.495,57 |
| 11382312 | SUPERMERCADO JURITIS DE ITAPIRA LTDA. - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 72 | 72 | 224.984,30 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 9 | 842.783.742,50 |
| 08183516000120 | CASAMAX COMERCIAL E SERVICOS LTDA | Comércio varejista de materiais de construção em geral | 22 | 511.432.467,96 |
| 62162847000120 | JOFEGE   PAVIMENTACAO E CONSTRUCAO LTDA | Construção de rodovias e ferrovias | 10 | 361.305.988,59 |
| 15320722000109 | VIGENT CONSTRUCOES LTDA | Construção de edifícios | 19 | 324.711.694,52 |
| 12039966000111 | LINK CARD ADM  DE BENEFICIOS EIRELI | Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica | 140 | 324.226.382,90 |
| 06291846000104 | CONSTROESTE   CONSTR  E PARTIC  LTDA | Construção de rodovias e ferrovias | 168 | 320.623.173,30 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 7 | 292.297.455,22 |
| 02666114000109 | MICLEAN COMERCIOS E SERVICOS LTDA | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 21 | 284.327.821,45 |
| 69144434000161 | SANCETUR   SANTA CECILIA TURISMO LTDA | Transporte rodoviário coletivo de passageiros, com itinerário fixo, municipal | 18 | 283.726.158,97 |
| 61980272000190 | S H A COM DE ALIMENTOS LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 6 | 233.292.650,82 |
| 12538448000142 | COTIA AMBIENTAL S.A | Coleta de resíduos não-perigosos | 1 | 230.870.947,57 |
| 09445502000109 | SOLUCOES SERVICOS TERCEIRIZADOS   EIRELI | Limpeza em prédios e em domicílios | 19 | 223.191.395,77 |
| 05326068000189 | A 3 TERRAPLENAGEM E ENGENHARIA LTDA | Obras de terraplenagem | 31 | 210.145.970,09 |
| 36573767000157 | CITY TRANSPORTES URBANO GLOBAL LTDA | Transporte rodoviário coletivo de passageiros, com itinerário fixo, municipal | 4 | 209.018.553,18 |
| 09033330000158 | COMPEC GALASSO ENGENHARIA CONSTRUCOES LTDA | Outras obras de engenharia civil não especificadas anteriormente | 6 | 203.752.542,26 |
| 46020301000269 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 2 | 202.529.371,13 |
| 48096044000193 | DEMAX - SERVIÇOS E COMÉRCIO LTDA. | Limpeza em prédios e em domicílios | 14 | 202.285.057,34 |
| 65035222000195 | ERA TECNICA ENG  SER  LTDA | Atividades paisagísticas | 18 | 201.045.493,99 |
| 53437315000167 | COMERCIAL J. AFONSO LTDA | Comércio atacadista de produtos alimentícios em geral | 215 | 198.807.346,50 |
| 05340639000130 | PRIME CONS E ASS EMPRESARIAL LTDA  EPP | Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica | 67 | 197.188.062,58 |
| 33507785000142 | CONSORCIO SAO BERNARDO AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 193.875.728,42 |
| 09294054000181 | ECOOSASCO AMBIENTAL S A | Coleta de resíduos não-perigosos | 1 | 182.518.391,52 |
| 58198524000119 | IRMANDADE DA SANTA CASA DE MISERIC DE SANTOS | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 2 | 182.049.541,08 |
| 48211585000115 | SOCIEDADE BENEFICENTE CAMINHO DE DAMASCO | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 3 | 180.230.651,93 |
| 07118264000193 | QUALITY COM. E DISTR.DE MEDICAMENTOS LTDA. | Comércio atacadista de medicamentos e drogas de uso humano | 48 | 170.311.023,34 |
| 25224614000188 | BRT SOROCABA CONCESS.DE SERV.PUBL.SPE S.A. | Transporte rodoviário coletivo de passageiros, com itinerário fixo, municipal | 1 | 164.799.478,19 |
| 61149829000145 | TECIPAR ENGENHARIA E MEIO AMBIENTE LTDA | Coleta de resíduos não-perigosos | 5 | 162.971.472,82 |
| 01958324000108 | PONTO FORTE  CONSTRUCOES E EMPREENDIMENTOS LTDA. | Construção de edifícios | 4 | 161.921.617,27 |
| 51473692000126 | IRMAND SANTA CASA DE MISERICORDIA DE LIMEIRA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 5 | 161.573.975,55 |
| 50351626000110 | BENEFICENCIA HOSPITALAR DE C. LANGE | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 9 | 158.811.709,68 |
