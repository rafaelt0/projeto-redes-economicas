# Validação e limpeza das despesas do TCESP, 2013


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 23.225.774.
    Registros lidos: 23.225.773.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 315.524 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | nr_empenho | identificador_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3.896 | 3.896 | 0 | 0 | 3.896 | 3.896 | 3.896 | 3.896 | 3.896 | 3.896 | 3.896 | 3.896 | 3.896 | 3.896 | 3.059.673 |


## Codificação

O arquivo é latin-1. Na leitura, 4.848 trechos em UTF-8 foram decodificados como UTF-8
    (171 com segundo byte entre 0x80 e 0x9F, 4.677 entre 0xA0 e 0xBF) e 271 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 10 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| ÉM PARA AS OUTRAS CRECHES E PRɴ- ESCOLAS | 5 |
| ÃO E TRANSPORTE DE PLACAS DA PǪ CORONEL JULIÃO  - MANUTENÇÃO  | 3 |
|  5 LTS  Item 004: SAPÓLIO EM PӠ- 300 G  Item 005: ABRIDOR DE  | 2 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Liquidado | 8.250.482 | 82.438.073.478,82 |
| Valor Pago | 7.881.504 | 76.820.908.474,35 |
| Empenhado | 6.486.620 | 93.122.596.575,60 |
| Anulação | 573.723 | 10.881.402.008,09 |
| Reforço | 33.444 | 1.808.732.119,96 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    16.478 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.486.619 | 134 | 1.692 | 1.982 | 1.448 | 0 | 1.219 | 364 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Campos do Jordão | 123 |
| Itapira | 110 |
| Vinhedo | 29 |
| Campinas | 25 |
| Franca | 11 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Ilhabela | 66 | None |
| Mogi das Cruzes | 9 | None |
| São Bernardo do Campo | 8 | None |
| Artur Nogueira | 6 | None |
| Cajamar | 4 | None |
| Santana de Parnaíba | 4 | None |
| São José do Rio Preto | 4 | 5.785,21 |
| Buri | 3 | 742,00 |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.012 | 1.144 | 798.815,62 |
| 2.013 | 534 | 1.066.729,25 |
| 2.011 | 275 | 8.047.424,49 |
| 2.010 | 23 | 14.704,11 |
| 2.008 | 2 | 0,00 |
| 2.009 | 2 | 0,00 |
| 2.006 | 1 | 0,00 |
| 2.007 | 1 | 0,00 |


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

Órgãos distintos: 1760. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 122 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 69 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 56 | SERVICO DE AGUA E ESGOTO DO MUNICIPIO DE JAU |
| FUNDO | 46 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AGENCIA | 8 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| AUTARQUIA | 8 | AUTARQUIA DE ESPORTE DE ASSIS |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| EMPRESA | 6 | EMPRESA DE TRANSPORTE COLETIVO DE DIADEMA |
| SAAE | 6 | SAAE - AMBIENTE |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 4.218.865 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1.010.739 |
| PESSOA FÍSICA | 858.006 |
| INSCRIÇÃO GENÉRICA-OUTROS | 380.537 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 9.647 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 4.765 |
| None | 1.982 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 1.850 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 220 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 8 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 185.592 | 185.282 | 310 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.218.865 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2013

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%. Linhas da Receita casadas mas malformadas, ignoradas: 0.

| cnpj_basicos | achados_na_receita |
|---|---|
| 175.696 | 175.686 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)

Linhas casadas mas malformadas, ignoradas: 0.

| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 185.282 | 185.210 | 47.704 |











## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 1.982 | -4.256,39 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 682.423 | 10.781.837.429,17 | 57.820 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.028.200 | 29.122.537.068,77 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 3.596 | 65.219.090,03 | 259 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 295.370 | 9.263.012.621,27 | 1.543 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 59.915 | 2.945.274.814,45 | 7.643 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 154.322 | 3.324.996.018,66 | 2.063 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 379.473 | 1.532.067.763,10 | 932 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 37.122 | 1.171.176.977,45 | 253 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 133.655 | -73.345,99 | 41.225 |
| 99 | MANTIDO | None | 2.710.561 | 25.845.363.778,61 | 148.782 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 347.047.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 148.782 | 1,00 | 511 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 597.255 | 8.612.361.111,16 |
| CONCORRÊNCIA | 25.882 | 5.754.988.934,57 |
| DISPENSA DE LICITAÇÃO | 1.575.166 | 4.377.945.681,39 |
| OUTROS/NÃO APLICÁVEL | 332.194 | 3.284.614.187,16 |
| TOMADA DE PREÇOS | 35.467 | 1.018.962.481,80 |
| CONVITE | 93.027 | 979.168.089,87 |
| CONCURSO | 5.358 | 807.211.487,23 |
| INEXIGÍVEL | 24.757 | 709.507.168,18 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 21.455 | 300.604.637,25 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 236 | 281.027.460,35 |
| 02558157000162 | TELECOMUNICACOES DE S PAULO S A TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 575 | 245.005.385,50 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 205 | 160.650.253,70 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 330 | 148.352.755,90 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 31 | 128.464.551,82 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 23 | 116.423.573,54 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 25 | 94.666.250,30 |
| 02449992005638 | BANCO BRASIL | Telefonia móvel celular | 461 | 28.130.417,85 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 25 | 19.815.100,59 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 21 | 19.071.882,18 |
| 07297359000111 | E.D.E. VALE PARANAPANEMA S/A. | Distribuição de energia elétrica | 24 | 18.290.900,35 |
| 02592658001641 | SUSTENTARE SERVICOS AMBIENTAIS S/A | Atividades relacionadas a esgoto, exceto a gestão de redes | 1 | 16.458.918,76 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 165 | 15.718.162,07 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 12.388.252,49 |
| 61416244000144 | C. N. E. E. | Distribuição de energia elétrica | 15 | 12.343.429,06 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 10673394 | SYSPRO-DATA SISTEMA DE PROCESSAMENTO LTDA | Tratamento de dados, provedores de serviços de aplicação e serviços de hospedagem na internet | 47 | 59 | 1.905.293,37 |
| 50807155 | ASSOC.SERV.FUNC.PUBLICOS MUNICIPAIS DA PREF. DE SM | Atividades de associações de defesa de direitos sociais | 64 | 105 | 1.291.040,43 |
| 02626065 | ANA MARIA ZANATA BARTOLOMEU - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 182 | 351 | 740.740,61 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 122 | 211 | 360.509,72 |
| 07122631 | CARVALHO DA SILVA E RODRIGUES SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 129 | 155 | 273.009,50 |
| 45056793 | BARCAS DE SANTOS-GUARUJA S/C LTDA | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 34 | 35 | 240.216,60 |
| 05794245 | PERIN ALIMENTOS LTDA - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 13 | 18 | 203.823,49 |
| 00010639 | ANTONIO CARLOS QUINTINO ME | Comércio varejista de carnes - açougues | 106 | 127 | 203.822,00 |
| 01564249 | DANIEL H. MARINELLI VERA CRUZ | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 13 | 15 | 202.888,97 |
| 02581032 | KATIA REGINA MARTINUCCI DE OLIVEIRA - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 129 | 173 | 182.691,51 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 107 | 183 | 155.218,35 |
| 67191700 | EDUARDO CARLOS BONACI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 38 | 39 | 100.043,80 |
| 07420925 | AUDAX - SERV. ADM. E  FINANCEIROS LTDA. ME | Serviços combinados de escritório e apoio administrativo | 17 | 18 | 84.853,39 |
| 56160203 | ANDREY APARECIDO GARBULIO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 96 | 96 | 81.100,00 |
| 59464537 | A FONTANEZI CABRALIA PAULISTA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 90 | 117 | 72.108,21 |
| 05609611 | MARIA ANGELA V. DA SILVA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 65 | 73 | 56.507,58 |
| 09274132 | NOGUEIRA E LEONEL LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 73 | 83 | 52.100,00 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 13 | 14 | 39.908,00 |
| 48718803 | HAMILTON MENECHELI CIA LTDA/SUPER BRAZIL | Serviços combinados de escritório e apoio administrativo | 50 | 72 | 31.112,72 |
| 02669977 | MERCEARIA COSTA INDIANA LTDA-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 48 | 48 | 28.000,00 |
| 43068030 | JOSE CARLOS BETIO-ME | Comércio varejista de carnes - açougues | 10 | 15 | 27.895,65 |
| 09625409 | EDGAR DA SILVA EMPORIO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 12 | 22.442,02 |
| 17001663 | JULIO CESAR DA SILVA E LOPES LTDA ME | Comércio varejista de carnes - açougues | 12 | 12 | 22.406,00 |
| 05211992 | NAIR CORREA M. PINTO V. CRUZ - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 7 | 13 | 20.931,14 |
| 50743913 | ALCENY GARBULLIO E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 25 | 29 | 20.730,00 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 61699567000192 | SECRETARIA DE ESTADO DA SAUDE | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 6 | 277.138.036,35 |
| 44164606000138 | ERJ ADM E RESTAURANTES DE EMPRESAS LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 16 | 175.069.314,70 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 170 | 163.118.529,86 |
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 9 | 152.773.013,08 |
| 60924040000151 | TB SERVICOS TRANSP LIMP GER E REC.HUMANOS S.A | Locação de automóveis sem condutor | 6 | 141.661.310,79 |
| 16505708000134 | SBC VALORIZACAO DE RESIDUOS SA | Coleta de resíduos não-perigosos | 1 | 138.404.367,68 |
| 06291846000104 | CONSTROESTE  CONST  E PARTICIPACOES LTDA | Construção de rodovias e ferrovias | 73 | 129.104.628,70 |
| 73188336000101 | PROVENCE CONSTRUTORA LTDA | Construção de edifícios | 10 | 128.762.078,12 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 9 | 119.912.936,41 |
| 10541089000157 | AZALEIA EMPREENDIMENTOS E PARTICIPACOES S A | Coleta de resíduos não-perigosos | 20 | 118.236.725,95 |
| 61699567001245 | SPDM ASSOC PAULISTA P/O DESENV DA MEDICINA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 116.763.462,91 |
| 61836813000100 | QUITAUNA SERVICOS LTDA | Coleta de resíduos não-perigosos | 1 | 115.782.724,72 |
| 24232886000167 | PRO SAUDE  ASSOCIACAO BENEFICENTE DE ASSISTENCIA S | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 4 | 112.294.676,27 |
| 47497367000398 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 1 | 106.220.311,70 |
| 55996615000101 | CONSLADEL - CONSTE LD ELETRONICA LTDA | Construção de edifícios | 7 | 94.325.848,64 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 10 | 94.298.142,64 |
| 17154899000108 | CONSTRUTORA MELLO DE AZEVEDO S/A | Construção de edifícios | 1 | 93.640.169,36 |
| 46020301000188 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Educação superior - graduação e pós-graduação | 3 | 92.644.832,97 |
| 43677822000114 | SOEBE CONSTRUCAO  E PAVIMENTACAO LTDA | Construção de rodovias e ferrovias | 11 | 84.639.928,83 |
| 67729178000491 | COM. CIR. RIOCLARENSE LTDA | Comércio atacadista de medicamentos e drogas de uso humano | 439 | 75.650.925,26 |
| 24232886005711 | PRO SAUDE   ASSOCIACAO BENEFICIENTE DE ASSISTENCIA SOCIA | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 1 | 75.471.709,00 |
| 08493239000152 | CONSORCIO TECAM - TECNOLOGIA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 74.474.159,83 |
| 66806555000133 | FBS - CONSTRUCAO CIVIL E PAVIMENTACAO LTDA | Construção de rodovias e ferrovias | 6 | 74.099.467,51 |
| 46044368000152 | SERVIÇO DE SAÚDE DR. CÂNDIDO FERREIRA | Atividades de assistência psicossocial e à saúde a portadores de distúrbios psíquicos, deficiência mental e dependência química e grupos similares não | 1 | 68.745.954,54 |
| 31733363000755 | CORPUS SANEAMENTO E OBRAS LTDA | Coleta de resíduos não-perigosos | 1 | 67.557.293,35 |
| 56473317000108 | EMPARSANCO S/A | Construção de rodovias e ferrovias | 1 | 67.482.826,91 |
| 62779145000190 | ASILO SANTO ANTONIO R/P IRMANDADE STA CASA MISER | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 3 | 67.359.375,91 |
| 55333769000113 | ENCALSO CONSTRUCOES LTDA | Construção de rodovias e ferrovias | 3 | 67.010.103,23 |
| 08528442000117 | COMERCIO DE ALIMENTOS LTDA- NUTRICIONALE | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 372 | 66.946.808,45 |
| 31733363000160 | CORPUS SANEAMENTO E OBRAS LTDA | Coleta de resíduos não-perigosos | 5 | 66.756.894,15 |
