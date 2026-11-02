# Validação e limpeza das despesas do TCESP, 2011


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 23.040.691.
    Registros lidos: 23.040.690.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 362.371 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | nr_empenho | identificador_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 40.542 | 40.542 | 0 | 0 | 40.542 | 40.542 | 40.542 | 40.542 | 40.542 | 40.542 | 40.542 | 40.542 | 40.542 | 40.542 | 2.463.270 |


## Codificação

O arquivo é latin-1. Na leitura, 389.669 trechos em UTF-8 foram decodificados como UTF-8
    (19.773 com segundo byte entre 0x80 e 0x9F, 369.896 entre 0xA0 e 0xBF) e 709 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 3 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| DOR PUBLICO | 1% DA RECEITA PRӴPRIA ARRECADADA NO MÊS DE FEVE | 3 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Liquidado | 8.228.535 | 70.112.814.010,34 |
| Valor Pago | 7.687.887 | 64.118.930.031,10 |
| Empenhado | 6.537.876 | 78.215.862.211,70 |
| Anulação | 553.672 | 9.025.756.830,70 |
| Reforço | 32.720 | 1.259.452.642,64 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    15.698 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.528.716 | 22.954 | 2.996 | 17.304 | 1 | 0 | 1.166 | 1.562 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Jundiaí | 984 |
| Itapira | 258 |
| Diadema | 77 |
| Campinas | 40 |
| Fernandópolis | 27 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Restinga | 6.508 | 17.924.080,68 |
| Caconde | 4.927 | 13.051.598,52 |
| Santa Lúcia | 4.670 | 9.779.378,12 |
| Franca | 4.527 | 66.642.977,29 |
| Itirapuã | 1.714 | 4.329.237,40 |
| Rincão | 340 | 732.106,89 |
| Diadema | 95 | 16.548.247,81 |
| São José da Bela Vista | 45 | 88.443,89 |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.011 | 17.303 | 61.974.091,90 |
| 2.010 | 1 | 0,00 |


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

Órgãos distintos: 1748. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 116 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 66 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 55 | SERVICO DE AGUA E ESGOTO DO MUNICIPIO DE JAU |
| FUNDO | 46 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AUTARQUIA | 8 | AUTARQUIA DE ESPORTE DE ASSIS |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| AGENCIA | 7 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 7 | SAAE - AMBIENTE |
| CENTRO | 5 | CENTRO MUNICIPAL DE FORMAÇÃO PROFISSIONAL-CMFP |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 4.200.070 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 978.510 |
| PESSOA FÍSICA | 890.498 |
| INSCRIÇÃO GENÉRICA-OUTROS | 425.837 |
| None | 17.304 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 9.976 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 4.439 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 1.857 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 197 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 28 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 182.577 | 182.159 | 418 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.200.070 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2011

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%. Linhas da Receita casadas mas malformadas, ignoradas: 0.

| cnpj_basicos | achados_na_receita |
|---|---|
| 172.701 | 172.680 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)

Linhas casadas mas malformadas, ignoradas: 0.

| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 182.159 | 182.055 | 48.494 |










## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 17.304 | -14.319.021,57 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 714.707 | 8.763.345.509,58 | 58.216 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.056.741 | 23.079.023.026,68 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 6.624 | 23.343.588,78 | 371 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 283.542 | 7.480.960.588,61 | 1.619 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 66.329 | 2.232.757.022,48 | 7.713 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 148.079 | 2.602.576.216,59 | 2.023 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 389.979 | 1.543.045.779,73 | 926 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 33.937 | 819.097.928,72 | 244 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 121.104 | -764.869,25 | 38.815 |
| 99 | MANTIDO | None | 2.690.370 | 23.791.156.575,57 | 146.514 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 346.004.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 146.514 | 1,00 | 467 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 482.496 | 6.786.137.671,90 |
| CONCORRÊNCIA | 30.281 | 5.993.944.113,80 |
| DISPENSA DE LICITAÇÃO | 1.440.577 | 3.753.012.338,62 |
| OUTROS/NÃO APLICÁVEL | 512.386 | 3.506.406.324,34 |
| TOMADA DE PREÇOS | 51.143 | 1.485.180.540,82 |
| CONVITE | 116.067 | 1.380.982.845,23 |
| INEXIGÍVEL | 38.740 | 535.486.744,75 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 17.877 | 238.370.660,32 |
| CONCURSO | 803 | 111.635.335,79 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 230 | 294.307.408,71 |
| 02558157000162 | TELECOMUNICACOES .DE S.PAULO S.A. TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 561 | 243.043.221,42 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 201 | 167.970.581,59 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 22 | 126.645.448,24 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 30 | 126.348.279,38 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 320 | 120.454.345,18 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 25 | 113.234.716,40 |
| 43642727000185 | TELEC.DE SAO PAULO S/A. TELESP | Serviços de telefonia fixa comutada - STFC | 109 | 25.095.833,03 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 23 | 23.503.196,63 |
| 02449992005638 | BANCO BRASIL | Telefonia móvel celular | 440 | 18.126.788,55 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 20 | 16.966.725,12 |
| 07297359000111 | E.D.E. VALE PARANAPANEMA S/A. | Distribuição de energia elétrica | 24 | 16.741.873,89 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 152 | 13.189.404,39 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 11.841.707,48 |
| 02592658001641 | SUSTENTARE SERVICOS AMBIENTAIS S/A | Atividades relacionadas a esgoto, exceto a gestão de redes | 1 | 11.579.423,28 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 07178151 | SUPERMERCADO MARAJOARA MAX LTD | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 43 | 44 | 1.288.452,35 |
| 50807155 | ASSOC.SERV.FUNC.PUBLICOS MUNICIPAIS DA PREF. DE SM | Atividades de associações de defesa de direitos sociais | 150 | 150 | 1.045.024,93 |
| 11419663 | ONIX - PARTICIPACOES E EMPREENDIMENTOS LTDA | Gestão e administração da propriedade imobiliária | 160 | 199 | 747.376,50 |
| 03283379 | CLAUDIO ALBERTO MARTINS ABDALA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 200 | 290 | 486.942,00 |
| 03640467 | SUPERMERCADO JAU SERV. LTDA. | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 49 | 83 | 360.022,58 |
| 68623479 | CAIXA ECONOMICA FEDERAL | Fundos de investimento, exceto previdenciários e imobiliários | 122 | 151 | 259.904,00 |
| 06210792 | GEOVAZ DE FREITAS SOLANA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 45 | 45 | 244.810,00 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 101 | 177 | 217.321,14 |
| 07122631 | CARVALHO DA SILVA E RODRIGUES SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 116 | 116 | 203.850,00 |
| 62234984 | SUPERMERCADO AVENIDA DE PEDERN | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 37 | 37 | 148.860,00 |
| 67191700 | EDUARDO CARLOS BONACI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 44 | 48 | 118.451,24 |
| 49865439 | BALESTRI   NESPECH LTDA   ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 27 | 27 | 87.490,00 |
| 01564249 | DANIEL H. MARINELLI VERA CRUZ | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 12 | 20 | 85.234,84 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 75 | 75 | 82.650,00 |
| 29055993 | SINDICATO DAS EMP DE TRANP DE PASS DE B MANSA E V RED | Atividades de organizações associativas patronais e empresariais | 44 | 58 | 81.550,34 |
| 00010639 | ANTONIO CARLOS QUINTINO ME | Comércio varejista de carnes - açougues | 84 | 84 | 80.500,00 |
| 02581032 | KATIA REGINA MARTINUCI DE OLIVEIRA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 92 | 93 | 77.250,00 |
| 09618829 | SUPERMERCADO BRANDAO INDIANA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 173 | 177 | 72.250,31 |
| 04812807 | EDNA C L  DE MORAES EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 63.210,00 |
| 08600562 | ADRIANA RIBEIRO MACIEL   ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 37 | 37 | 62.940,00 |
| 12838196 | LOPES   SARANHOLI SUPERMERCADO LTDA   ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 39 | 39 | 59.910,00 |
| 02183038 | SILVANA G B  MANSANO   ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 29 | 29 | 58.150,00 |
| 53813606 | ALFEU PLACIDELLI   CIA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 35 | 35 | 47.610,00 |
| 02911243 | ASSOCIACAO DOS MORADORES DO BAIRRO DO JD ELDORADO | Atividades de associações de defesa de direitos sociais | 13 | 15 | 47.353,59 |
| 01854105 | MERCEARIA FERREIRA   FERREIRA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 78 | 78 | 44.460,00 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 61699567000192 | SOCIEDADE PTA P/A  O DESENV DA MEDICINA  SPDM | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 7 | 230.804.913,63 |
| 14310577000104 | CONSORCIO NOVO CANUDOS | Outras obras de engenharia civil não especificadas anteriormente | 4 | 221.586.195,08 |
| 49957137000128 | TERMAQ   TERRAPLENAGEM  CONSTR  CIVIL E ESCAVACOES LTDA | Construção de edifícios | 11 | 179.223.485,23 |
| 56473317000108 | EMPARSANCO S A | Construção de rodovias e ferrovias | 3 | 166.962.117,79 |
| 73188336000101 | LOGIC ENGENHARIA E CONSTRUÇÃO LTDA | Construção de edifícios | 12 | 163.441.880,16 |
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 10 | 130.961.205,62 |
| 62436282000121 | GERALDO J  COAN   CIA  LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 27 | 116.543.005,74 |
| 53437315000167 | COMERCIAL JOAO AFONSO  N | Comércio atacadista de produtos alimentícios em geral | 161 | 116.458.039,92 |
| 50944198000130 | HOSPITAL DE CARIDADE S.VICENTE DE PAULA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 114.886.586,02 |
| 46044368000152 | SERVIÇO DE SAÚDE DR. CÂNDIDO FERREIRA | Atividades de assistência psicossocial e à saúde a portadores de distúrbios psíquicos, deficiência mental e dependência química e grupos similares não | 1 | 110.702.515,68 |
| 61699567001245 | SPDM ASSOC PAULISTA P/O DESENV DA MEDICINA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 104.650.564,96 |
| 60924040000151 | TB SERV.TRANSP. LIMP.GERENCIAMENTO DE REC. HU | Locação de automóveis sem condutor | 5 | 100.220.900,93 |
| 62162847000120 | JOFEGE - PAVIMENTACAO E CONSTRUCAO LTDA. | Construção de rodovias e ferrovias | 14 | 89.092.575,67 |
| 47497367000398 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 1 | 87.122.922,31 |
| 06098460000180 | TRATENGE ENGENHARIA LTDA | Construção de rodovias e ferrovias | 2 | 82.940.557,48 |
| 55996615000101 | CONSLADEL - CONST. E LACOS DETET. E ELETRONIC | Construção de edifícios | 9 | 81.190.285,15 |
| 61836813000100 | QUITAUNA SERVICOS LTDA | Coleta de resíduos não-perigosos | 1 | 79.358.400,00 |
| 06291846000104 | CONSTROESTE CONST  E PARTICIPACOES LTDA | Construção de rodovias e ferrovias | 42 | 77.703.229,90 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 8 | 77.373.518,69 |
| 10541089000157 | AZALEIA EMPREENDIMENTOS E PARTICIPACOES S A | Coleta de resíduos não-perigosos | 14 | 75.017.519,23 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 9 | 74.446.242,88 |
| 08493239000152 | CONSORCIO TECAM - TECNOLOGIA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 74.302.707,86 |
| 03829424000151 | PLANETA EDUCACAO  GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 11 | 69.321.522,18 |
| 03189580000103 | DEMOP - PARTICIPACOES LTDA | Outras obras de engenharia civil não especificadas anteriormente | 77 | 64.103.741,78 |
| 02293852000140 | S.P.  ALIMENTAÇÃO E SERVIÇOS LTDA.- | Fornecimento de alimentos preparados preponderantemente para empresas | 7 | 63.684.045,42 |
| 24232886005711 | PRO SAUDE   ASSOCIACAO BENEFICIENTE DE ASSISTENCIA SOCIA | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 1 | 60.533.079,50 |
| 08528442000117 | NUTRICIONALE  COMERCIO DE ALIMENTOS LTDA | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 329 | 59.059.080,08 |
| 46020301000188 | PONTIF. UNIVERSIDADE CATOLICA CAMPINAS | Educação superior - graduação e pós-graduação | 6 | 57.733.042,12 |
| 09294054000181 | ECOOSASCO AMBIENTAL S/A | Coleta de resíduos não-perigosos | 1 | 57.397.518,92 |
| 01059631000149 | EPPO SANEAMENTO AMBIENTAL E OBRAS  LTDA | Coleta de resíduos não-perigosos | 5 | 56.452.259,65 |
