# Validação e limpeza das despesas do TCESP, 2020


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 22.027.667.
    Registros lidos: 22.027.666.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 180.974 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | codigo_municipio_ibge | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa | nr_empenho | identificador_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 25 | 0 | 2 |


## Codificação

O arquivo é latin-1. Na leitura, 174.816 trechos em UTF-8 foram decodificados como UTF-8
    (0 com segundo byte entre 0x80 e 0x9F, 174.816 entre 0xA0 e 0xBF) e 1.451 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 145 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| ISTRATIVA PARA MANUTENCAO DEÃ_ŸILUMINACAO PUBLICA E PARQUE DE | 26 |
| ES COM DOENCAS RESPIRATORIASÃ_Ÿ | 25 |
| ITO E DESENVOLVIMENTO SOCIALÃ_Ÿ | 24 |
| ALMENTE EM AÇO INOXIDÁVEL QUE ɠALTAMENTE DURÁVEL ALEM DE RESI | 12 |
|  FINAL DOS RESIDUOS DE SAUDEÃ_Ÿ | 10 |
| A DE JARDIM COM TRIPLA CAMADA ؽ" COR VERDEREGISTRO DE PREÇOS  | 8 |
|  PVC EMBORRACHADA COR LARANJA ؾREGISTRO DE PREÇOS PARA AQUISI | 6 |
|  PVC EMBORRACHADA COR LARANJA ؽ"REGISTRO DE PREÇOS PARA AQUIS | 5 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Pago | 7.766.438 | 126.492.314.804,69 |
| Valor Liquidado | 7.378.085 | 131.148.941.047,79 |
| Empenhado | 6.219.149 | 154.282.173.908,07 |
| Anulação | 581.758 | 22.355.580.682,68 |
| Reforço | 82.236 | 4.997.591.064,06 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    5.187 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.218.705 | 234 | 370 | 1 | 1 | 0 | 141 | 59 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Paulínia | 21 |
| Ribeirão Preto | 16 |
| São José do Rio Preto | 7 |
| Clementina | 4 |
| São João da Boa Vista | 3 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Mogi das Cruzes | 183 | None |
| Piracicaba | 11 | None |
| São José do Rio Preto | 11 | 2.970.496,54 |
| São João da Boa Vista | 5 | 17.168,03 |
| Bauru | 3 | None |
| Bertioga | 3 | None |
| Ituverava | 3 | None |
| Marília | 3 | None |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.019 | 1 | 0,00 |


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

Órgãos distintos: 1748. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 128 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 62 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 55 | SERVICO AUTONOMO DE AGUA E ESGOTO DE SALTO - SAAE SALTO |
| FUNDO | 41 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AGENCIA | 9 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| EMPRESA | 9 | EMPRESA DE DESENVOLVIMENTO URBANO E SOCIAL DE SOROCABA |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| AUTARQUIA | 7 | AUTARQUIA DE PREVIDÊNCIA PRÓPRIA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| CENTRO | 5 | CENTRO MUNICIPAL DE FORMAÇÃO PROFISSIONAL-CMFP |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 3.922.070 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 1.259.788 |
| PESSOA FÍSICA | 670.702 |
| INSCRIÇÃO GENÉRICA-OUTROS | 360.463 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 4.698 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 554 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 266 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 84 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 79 |
| None | 1 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 175.638 | 175.570 | 68 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 3.922.070 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2020

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.

| cnpj_basicos | achados_na_receita |
|---|---|
| 167.623 | 167.615 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)


| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 175.570 | 175.531 | 24.984 |






## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 1 | 0,00 | 0 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 580.863 | 20.110.826.435,17 | 50.814 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.091.385 | 42.060.695.631,46 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 6.601 | 129.906.186,52 | 41 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 380.610 | 15.144.624.527,57 | 1.444 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 60.557 | 8.556.232.090,99 | 7.863 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 186.526 | 5.809.260.141,72 | 1.978 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 302.044 | 2.479.315.694,24 | 1.003 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 41.792 | 2.557.858.533,56 | 255 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 137.858 | -201.192,57 | 35.848 |
| 99 | MANTIDO | None | 2.430.468 | 40.077.397.336,26 | 138.852 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 322.398.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 138.852 | 1,00 | 503 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 864.955 | 12.058.203.331,93 |
| CONCORRÊNCIA | 18.548 | 8.415.149.224,92 |
| DISPENSA DE LICITAÇÃO | 1.232.831 | 6.432.476.108,15 |
| OUTROS/NÃO APLICÁVEL | 140.435 | 6.404.271.231,09 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 97.544 | 2.492.549.975,80 |
| TOMADA DE PREÇOS | 23.611 | 2.428.576.102,64 |
| INEXIGÍVEL | 19.388 | 1.045.884.502,03 |
| CONVITE | 32.829 | 584.303.999,88 |
| RDC | 111 | 207.447.394,41 |
| CONCURSO | 211 | 8.430.811,78 |
| Leilão | 5 | 104.653,63 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 254 | 694.210.525,28 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 212 | 316.018.681,81 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 346 | 238.530.636,30 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 24 | 203.419.974,57 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 26 | 191.786.143,33 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 30 | 170.616.289,96 |
| 02558157000162 | N-TELEFONICA BRASIL S.A. | Serviços de telecomunicações sem fio não especificados anteriormente | 606 | 162.665.743,72 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 68 | 107.601.325,06 |
| 53859112000169 | CIA JAGUARI DE ENERGIA | Distribuição de energia elétrica | 35 | 60.645.852,21 |
| 02998611000104 | COMPANHIA DE TRANSMDE ENERGIA ELETRICA PAULISTA | Transmissão de energia elétrica | 4 | 30.378.650,09 |
| 33050196017749 | CPFL-CIA PAULISTA DE FORCA E LUZ | Transmissão de energia elétrica | 1 | 23.390.775,23 |
| 46682761000171 | COMPANHIA DE DESENVOLVIMENTO DE GUARATINGUETA - CODESG | Gestão de redes de esgoto | 1 | 20.222.662,67 |
| 90400888000142 | BANCO  SANTANDER (BRASIL) S/A | Bancos múltiplos, com carteira comercial | 212 | 14.582.567,77 |
| 02302100001684 | EDP SAO PAULO DISTRIBUICAO DE ENERGIA S.A. | Distribuição de energia elétrica | 1 | 13.915.154,24 |
| 60746948000112 | BANCO BRADESCO | Bancos múltiplos, com carteira comercial | 187 | 12.367.715,42 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 11517841 | COMPANHIA SULAMERICANA DE DISTRIBUICAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 165 | 169 | 3.450.832,41 |
| 27509356 | RVM DE SOUZA ME | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 83 | 86 | 1.661.644,30 |
| 46464962 | ASSOCIACAO COMERCIAL E EMPRESARIAL DE TUPI PAULIST | Atividades de organizações associativas patronais e empresariais | 30 | 37 | 1.269.848,00 |
| 03402817 | MONTANO EXPRESS TRANSPORTES, TURISMO E LOCADORA DE | Transporte rodoviário de carga, exceto produtos perigosos e mudanças, intermunicipal, interestadual e internacional | 8 | 16 | 1.168.201,72 |
| 00965345 | ASSOCIAÇÃO COMERCIAL E EMPRESARIAL DE ECP. | Atividades de associações de defesa de direitos sociais | 12 | 12 | 1.158.705,00 |
| 02581032 | KATIA REGINA MARTINUCCI DE OLIVEIRA EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 127 | 141 | 890.271,58 |
| 53913075 | SUPERMERCADO RASTELAO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 72 | 91 | 675.170,39 |
| 07275201 | MENDES ESPINHA E MENDES ESPINHA LTDA-EPP | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 230 | 297 | 494.206,14 |
| 07993190 | ESPINHA E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 204 | 294 | 422.189,10 |
| 03354724 | PAVONI E SALAZAR SUPERMERCADOS LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 36 | 318.998,79 |
| 03451241 | ASPUMC-ASSOC.SERV.PUBL.MUNIC.CRUZALIA | Atividades de associações de defesa de direitos sociais | 11 | 11 | 303.072,50 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 105 | 115 | 270.289,93 |
| 47619309 | CICERO PONTES DA SILVA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 73 | 95 | 206.406,32 |
| 07629859 | AGENCIA DE VIAGENS E TRANSPORTES VICAMPE LTDA - ME | Agências de viagens | 29 | 38 | 186.754,80 |
| 07122631 | CARVALHO DA SILVA E RODRIGUES SUPERMERCADO LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 57 | 62 | 173.154,11 |
| 50538362 | CEYA COMERCIAL LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 46 | 173.048,34 |
| 20524113 | SUPERMERCADO NOVA PROMISSAO | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 36 | 43 | 131.529,52 |
| 07303268 | MARIA ROSANGELA DE OLIVEIRA COUTO-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 12 | 86.685,00 |
| 92556539 | KAPPE SOFTWARE CONSULTORIA DE INFORMATICA LTDA | Desenvolvimento de programas de computador sob encomenda | 4 | 5 | 84.931,66 |
| 06021676 | CASA DE CARNES CAMACHO PSSAO LTDA | Comércio varejista de carnes - açougues | 33 | 33 | 82.496,46 |
| 24129437 | CONGONHAS COMERCIO DE COMBUSTIVEIS LTDA. | Comércio varejista de combustíveis para veículos automotores | 22 | 22 | 75.840,00 |
| 31132797 | JOSEFA JOVINO FERREIRA *** | Comércio varejista de carnes - açougues | 9 | 9 | 74.335,00 |
| 08025537 | ADILSON LIMA DOS SANTOS TRANSPORTES ME | Comércio atacadista de sementes, flores, plantas e gramas | 4 | 6 | 70.026,00 |
| 17139426 | J.W.T. DONAIRE - ME | Comércio varejista de carnes - açougues | 11 | 17 | 55.797,90 |
| 47618087 | MAON PEOA  CIA LTDA | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 19 | 38 | 52.399,06 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 12 | 694.991.019,04 |
| 61699567000192 | ASSOCIAÇÃO PAULISTA PARA O DESENVOLVIMENTO DA MEDICINA-SPDM | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 4 | 278.951.349,01 |
| 62162847000120 | JOFEGE   PAVIMENTACAO E CONSTRUCAO LTDA | Construção de rodovias e ferrovias | 16 | 250.434.821,75 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 11 | 193.193.432,01 |
| 53437315000167 | COM. JOAO AFONSO LTDA. | Comércio atacadista de produtos alimentícios em geral | 209 | 187.549.864,14 |
| 05497348000150 | TRAIL INFRAESTRUTURA EIRELI | Construção de rodovias e ferrovias | 5 | 186.522.313,90 |
| 06291846000104 | CONSTROESTE   CONSTR  E PARTIC  LTDA | Construção de rodovias e ferrovias | 171 | 183.734.976,48 |
| 61699567001830 | SPDM-ASSOCIAÇÃO PAULISTA P/ DESENVOLV.DA MEDICINA | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 1 | 176.597.388,71 |
| 46020301000188 | SOCIEDADE CAMPINEIRA DE EDUCACAO E INSTRUCAO | Educação superior - graduação e pós-graduação | 3 | 158.578.651,73 |
| 10558895000138 | NORAMIX CONCRETO S/A | Obras de urbanização - ruas, praças e calçadas | 180 | 157.757.890,06 |
| 33507785000142 | CONSORCIO SAO BERNARDO AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 149.684.037,90 |
| 67642496000178 | INSTITUTO DE DESENVOLVIMENTO DE GESTAO TECNOLOGIA E PESQUISA EM SAUDE ASSISTENCIA SOCIAL IDGT | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 3 | 147.632.367,28 |
| 22315713000187 | INSTITUTO SOCIAL HOSPITAL ALEMÃO OSWALDO CRUZ | Serviços de assistência social sem alojamento | 1 | 145.870.045,97 |
| 60003761000129 | FUND. FACULDADE REG. DE MED. SAO JOSE DO RIO PRETO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 27 | 136.039.310,84 |
| 08528442000117 | COMERCIO DE ALIMENTOS LTDA- NUTRICIONALE | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 309 | 133.340.344,46 |
| 09294054000181 | ECOOSASCO AMBIENTAL S A | Coleta de resíduos não-perigosos | 1 | 132.406.150,99 |
| 13034156000135 | TETO CONSTRUCOES COM E EMPREEND LTDA | Construção de edifícios | 29 | 131.900.053,95 |
| 71485056000121 | IRMANDADE SANTA CASA DE MISERICORDIA SOROCABA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 130.298.097,20 |
| 12538448000142 | COTIA AMBIENTAL S.A | Coleta de resíduos não-perigosos | 1 | 127.516.517,35 |
| 19224814000138 | CONSORCIO RENOVA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 107.009.789,43 |
| 47078019000114 | HOSPITAL MAHATMA GANDHI | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 17 | 106.554.355,76 |
| 55996615000101 | CLD CONSTRUTORA, LACOS DETETORES E ELETRONICA LTDA | Construção de edifícios | 6 | 105.962.836,94 |
| 10541089000157 | ESTRE SPI AMBIENTAL S.A | Coleta de resíduos não-perigosos | 14 | 105.126.167,16 |
| 09033330000158 | COMPEC GALASSO ENG E CONST LTDA | Outras obras de engenharia civil não especificadas anteriormente | 7 | 104.545.450,24 |
| 57623761000117 | D N P TERRAPL E PAVIMENT FORESTO LTDA | Obras de urbanização - ruas, praças e calçadas | 36 | 103.700.328,05 |
| 07118264000193 | QUALITY MED COM  E DIS DE MEDIC LTDA EPP | Comércio atacadista de medicamentos e drogas de uso humano | 118 | 102.863.565,20 |
| 13370183000189 | FUNDACAO HOSPITAL SANTA LYDIA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 102.526.905,34 |
| 02666114000109 | MICLEAN COMERCIOS E SERVICOS LTDA | Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente | 11 | 101.486.198,49 |
| 47708771000282 | IRMANDADE DA S. CASA DE M. DE S. BERNARDO DO CAMPO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 99.231.402,67 |
| 10995737000145 | ORGANIZACAO PRO VIDA | Atividades de apoio à gestão de saúde | 2 | 98.159.944,07 |
