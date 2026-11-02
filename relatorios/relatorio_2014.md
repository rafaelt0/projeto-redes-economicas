# Validação e limpeza das despesas do TCESP, 2014


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 23.437.349.
    Registros lidos: 23.437.348.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 297.906 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2.630.364 | 0 | 0 |


## Codificação

O arquivo é latin-1. Na leitura, 4.282 trechos em UTF-8 foram decodificados como UTF-8
    (0 com segundo byte entre 0x80 e 0x9F, 4.282 entre 0xA0 e 0xBF) e 8 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 32 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| 900ML  Item 006: FERMENTO EM PӠ- EMBALAGE | 6 |
|  1 LT  Item 002: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 003: | 3 |
|  1 LT  Item 003: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 004: | 3 |
|  340G  Item 003: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 004: | 3 |
|  340G  Item 005: FERMENTO EM PӠ- EMBALAGEM C/ 250G  Item 006: | 3 |
| EICULOS DA SECRETARIA DE EDUCAǴ~AO | 3 |
| MANUTENÇÃO DE VIAS PÚBLICAS PRӿ- ESTRADA ,DEBITADO EM 04.02.. | 3 |
| MANUTENÇÃO DE VIAS PÚBLICAS PRӿ- ESTRADA ,DEBITADO EM 07.01.2 | 3 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Liquidado | 8.369.722 | 90.396.605.757,83 |
| Valor Pago | 7.896.075 | 85.706.496.456,63 |
| Empenhado | 6.534.498 | 104.285.002.722,12 |
| Anulação | 595.591 | 12.552.884.604,06 |
| Reforço | 41.462 | 2.353.218.941,47 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    17.441 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.532.412 | 49 | 1.767 | 6 | 0 | 0 | 1.290 | 432 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Ilhabela | 223 |
| Mairinque | 43 |
| Campinas | 33 |
| Jundiaí | 22 |
| São José do Rio Preto | 16 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| São José do Rio Preto | 17 | 98.027,82 |
| Ribeira | 11 | 31.700,85 |
| Cerqueira César | 4 | None |
| Iacri | 3 | 15.717,41 |
| Araçatuba | 2 | None |
| Assis | 2 | 4.400,00 |
| Parapuã | 2 | 1.968,00 |
| Piraju | 2 | None |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.014 | 6 | 4.328,35 |


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
| INSTITUTO | 123 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 67 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 58 | SERVICO DE AGUA E ESGOTO DO MUNICIPIO DE JAU |
| FUNDO | 45 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
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
| CNPJ - PESSOA JURÍDICA | 4.208.811 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1.035.676 |
| PESSOA FÍSICA | 877.643 |
| INSCRIÇÃO GENÉRICA-OUTROS | 396.102 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 7.659 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 4.319 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 1.993 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 197 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 12 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 185.485 | 185.276 | 209 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.208.811 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2014

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%. Linhas da Receita casadas mas malformadas, ignoradas: 0.

| cnpj_basicos | achados_na_receita |
|---|---|
| 176.001 | 175.991 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)

Linhas casadas mas malformadas, ignoradas: 0.

| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 185.276 | 185.209 | 46.509 |










## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 6 | -3.110,00 | 4 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 674.411 | 12.153.584.002,08 | 57.253 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.084.938 | 31.871.365.186,99 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 3.908 | 49.726.807,39 | 173 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 311.152 | 10.174.607.096,85 | 1.380 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 59.821 | 3.782.787.292,07 | 7.599 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 166.169 | 3.525.021.152,91 | 2.097 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 350.738 | 1.618.928.629,16 | 906 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 41.237 | 1.426.381.580,67 | 262 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 136.103 | -20.042,65 | 39.837 |
| 99 | MANTIDO | None | 2.703.929 | 29.482.846.720,68 | 148.575 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 347.238.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 148.575 | 1,00 | 518 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 750.936 | 10.469.607.591,05 |
| CONCORRÊNCIA | 25.544 | 6.367.895.134,31 |
| DISPENSA DE LICITAÇÃO | 1.407.449 | 4.595.710.269,43 |
| OUTROS/NÃO APLICÁVEL | 348.016 | 3.443.696.112,66 |
| TOMADA DE PREÇOS | 36.008 | 1.522.234.053,55 |
| CONCURSO | 5.459 | 1.022.804.342,55 |
| CONVITE | 85.959 | 975.712.077,88 |
| INEXIGÍVEL | 22.094 | 685.516.140,48 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 22.464 | 399.670.998,77 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 239 | 332.641.262,49 |
| 02558157000162 | TELECOMUNICACOES DE S PAULO S A TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 578 | 238.853.568,33 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 206 | 184.066.303,93 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 326 | 151.643.386,59 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 23 | 126.924.787,93 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 31 | 117.731.802,33 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 25 | 111.229.039,18 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 25 | 23.925.242,15 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 21 | 22.305.873,82 |
| 07297359000111 | E.D.E. VALE PARANAPANEMA S/A. | Distribuição de energia elétrica | 26 | 21.419.640,91 |
| 02449992005638 | BANCO BRASIL | Telefonia móvel celular | 326 | 18.012.218,76 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 174 | 16.256.816,08 |
| 61416244000144 | C. N. E. E. | Distribuição de energia elétrica | 15 | 14.078.053,44 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 13.951.610,48 |
| 43776517059400 | CIA DE SANEAM.BAS.DO EST.DE SAO PAULO-SABESP | Captação, tratamento e distribuição de água | 1 | 9.549.005,75 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 02626065 | ANA MARIA ZANATA BARTOLOMEU - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 200 | 325 | 698.927,53 |
| 09368528 | ASSOCIAÇÃO RIOPARDENSE RURAL E URBANA DE FUTEBOL AMADOR | Clubes sociais, esportivos e similares | 6 | 7 | 682.123,54 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 120 | 163 | 397.455,71 |
| 07122631 | CARVALHO DA SILVA E RODRIGUES SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 125 | 149 | 273.185,00 |
| 01564249 | DANIEL H. MARINELLI VERA CRUZ | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 13 | 24 | 242.061,24 |
| 00010639 | ANTONIO CARLOS QUINTINO ME | Comércio varejista de carnes - açougues | 110 | 132 | 234.800,00 |
| 45056793 | BARCAS DE SANTOS-GUARUJA S/C LTDA | Transporte por navegação de travessia intermunicipal, interestadual e internacional | 29 | 29 | 232.307,90 |
| 08453035 | PONTHAL TRANSPORTES RODOVIÁRIOS E LOGÍSTICA LTDA. | Transporte rodoviário de carga, exceto produtos perigosos e mudanças, municipal. | 14 | 17 | 212.043,00 |
| 02581032 | KATIA REGINA MARTINUCI DE OLIVEIRA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 112 | 143 | 201.060,41 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 98 | 154 | 190.020,62 |
| 06129146 | CRISTOVAO ALBARRACIM FILHO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 27 | 27 | 122.550,00 |
| 67191700 | EDUARDO CARLOS BONACI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 36 | 50 | 115.805,00 |
| 09274132 | NOGUEIRA E LEONEL LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 86 | 99 | 61.737,78 |
| 60780889 | MARIA ODETE CHECHETTO BERTINOTTI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 63 | 95 | 58.003,94 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 12 | 51.830,00 |
| 59464537 | A FONTANEZI CABRALIA PAULISTA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 98 | 113 | 51.237,04 |
| 17001663 | JULIO CESAR DA SILVA E LOPES LTDA ME | Comércio varejista de carnes - açougues | 14 | 14 | 34.864,00 |
| 56160203 | ANDREY APARECIDO GARBULIO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 60 | 60 | 32.500,00 |
| 09625409 | EDGAR DA SILVA EMPORIO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 13 | 13 | 30.762,00 |
| 01894316 | ELIZEU GERVASIO ACOUGUE ME | Comércio varejista de carnes - açougues | 53 | 53 | 22.000,00 |
| 19895581 | R. L. PARRILHA SUPERMERCADO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 45 | 45 | 16.750,00 |
| 50743913 | ALCENY GARBULLIO E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 27 | 31 | 15.287,50 |
| 60237229 | JOSE ANTONIO AGOSTINHO -ME | Serviços de reservas e outros serviços de turismo não especificados anteriormente | 17 | 23 | 14.043,05 |
| 08594304 | ANTONIO RENALDO SPEDO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 4 | 7 | 8.774,27 |
| 08265726 | CASA DE CARNES BETTIO DE STO. EXPED | Comércio varejista de carnes - açougues | 12 | 12 | 8.090,00 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 61699567000192 | SECRETARIA DE ESTADO DA SAUDE | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 4 | 255.970.775,90 |
| 44164606000138 | ERJ ADM E RESTAURANTES DE EMPRESAS LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 13 | 180.821.043,80 |
| 73188336000101 | PROVENCE CONSTRUTORA LTDA | Construção de edifícios | 7 | 172.852.331,76 |
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 9 | 163.218.046,62 |
| 60924040000151 | TB SERVICOS TRANSP LIMP GER E REC.HUMANOS S.A | Locação de automóveis sem condutor | 6 | 161.551.216,65 |
| 24232886000167 | PRO SAUDE  ASSOCIACAO BENEFICENTE DE ASSISTENCIA S | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 5 | 149.785.754,80 |
| 16505708000134 | SBC VALORIZACAO DE RESIDUOS SA | Coleta de resíduos não-perigosos | 1 | 143.968.999,98 |
| 61699567001245 | SPDM ASSOC PAULISTA P/O DESENV DA MEDICINA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 142.745.743,71 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 161 | 140.929.373,54 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 9 | 133.284.399,92 |
| 10541089000157 | AZALEIA EMPREENDIMENTOS E PARTICIPACOES S A | Coleta de resíduos não-perigosos | 20 | 132.785.955,27 |
| 46020301000188 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Educação superior - graduação e pós-graduação | 2 | 108.150.036,41 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 12 | 105.691.321,47 |
| 47497367000398 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 1 | 97.990.661,64 |
| 55996615000101 | CONSLADEL - CONSTE LD ELETRONICA LTDA | Construção de edifícios | 7 | 97.378.946,22 |
| 03829424000151 | PLANETA EDUCACAO  GRAFICA E EDITORA LTDA | Outras atividades de ensino não especificadas anteriormente | 12 | 87.122.865,61 |
| 61836813000100 | QUITAUNA SERVICOS LTDA | Coleta de resíduos não-perigosos | 1 | 82.716.666,51 |
| 19224814000138 | CONSORCIO RENOVA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 81.416.020,70 |
| 55333769000113 | ENCALSO CONSTRUCOES LTDA | Construção de rodovias e ferrovias | 1 | 81.171.781,48 |
| 67729178000491 | COM. CIR. RIOCLARENSE LTDA | Comércio atacadista de medicamentos e drogas de uso humano | 492 | 79.713.216,25 |
| 62162847000120 | JOFEGE - PAVIMENTACAO E CONSTRUCAO LTDA. | Construção de rodovias e ferrovias | 12 | 79.143.129,04 |
| 06291846000104 | CONSTROESTE  CONST  E PARTICIPACOES LTDA | Construção de rodovias e ferrovias | 90 | 75.671.292,12 |
| 02671087000154 | M.W.E PAVIMENTACAO E CONSTRUCAO LTDA | Obras de urbanização - ruas, praças e calçadas | 6 | 68.734.913,35 |
| 24232886005711 | PRO SAUDE   ASSOCIACAO BENEFICIENTE DE ASSISTENCIA SOCIA | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 1 | 66.950.614,00 |
| 31733363000755 | CORPUS SANEAMENTO E OBRAS LTDA | Coleta de resíduos não-perigosos | 1 | 66.867.173,79 |
| 62779145000190 | IRMANDADE DA SANTA CASA DE MISERICORDIA DE SAO PAULO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 2 | 66.216.928,26 |
| 58198524000119 | IRMANDADE DA SANTA CASA DE MISERIC DE SANTOS | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 4 | 66.113.501,83 |
| 12162177000173 | COLEPAV AMBIENTAL LTDA | Coleta de resíduos não-perigosos | 3 | 65.622.440,84 |
| 13461965000123 | EPPO ITU SOLUCOES AMBIENTAIS S/A | Coleta de resíduos não-perigosos | 1 | 64.534.462,00 |
| 48096044000193 | DEMAX - SERVICOS E COMERCIO LTDA | Limpeza em prédios e em domicílios | 8 | 62.574.134,12 |
