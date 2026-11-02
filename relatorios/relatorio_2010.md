# Validação e limpeza das despesas do TCESP, 2010


## Integridade do arquivo

Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: 22.399.541.
    Registros lidos: 22.399.540.
    Registros rejeitados pelo parser: 0.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: 0.
    

## Valores, datas e ano


| ano_diferente | mes_invalido | valor_ilegivel | valor_com_ponto | valor_negativo | data_ilegivel |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 600.135 | 0 |


## Campos vazios


| id_despesa_detalhe | ano_exercicio | ds_municipio | ds_orgao | mes_referencia | mes_ref_extenso | tp_despesa | nr_empenho | identificador_despesa | ds_despesa | dt_emissao_despesa | vl_despesa | ds_funcao_governo | ds_subfuncao_governo | cd_programa | ds_programa | cd_acao | ds_acao | ds_fonte_recurso | ds_cd_aplicacao_fixo | ds_modalidade_lic | ds_elemento | historico_despesa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 21.512 | 21.512 | 0 | 0 | 21.512 | 21.512 | 21.512 | 21.512 | 21.512 | 21.512 | 21.512 | 21.512 | 21.512 | 21.512 | 6.348.552 |


## Codificação

O arquivo é latin-1. Na leitura, 4.272 trechos em UTF-8 foram decodificados como UTF-8
    (220 com segundo byte entre 0x80 e 0x9F, 4.052 entre 0xA0 e 0xBF) e 3 bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    
| duplo_encoding | controle_c1 | fora_do_latin1 |
|---|---|---|
| 0 | 0 | 12 |

Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:

| trecho | linhas |
|---|---|
| , DIAS 15 E 16/09/2010 NO MUNCʹPIO DE SÃO PAULO) | 6 |
| A COPERSERV, DIA 08/07/2010-PRӴ-JOVEM - RECURSO FEDERAL | 3 |
| NECA ¨A PRIMEIRA BONECA DO BEBʨ- COLEÇÃO PIM PAM PUM - IDADE  | 3 |


## Tipos de linha

Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.

| tp_despesa | linhas | valor |
|---|---|---|
| Valor Liquidado | 8.004.880 | 61.133.478.346,15 |
| Valor Pago | 7.521.714 | 55.777.278.486,49 |
| Empenhado | 6.336.956 | 68.373.242.023,81 |
| Anulação | 504.815 | 7.655.569.020,65 |
| Reforço | 31.175 | 1.470.607.865,09 |


## Empenhos

Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    13.252 números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.

| empenhos | linhas_duplicadas_removidas | chave_com_mais_de_um_empenhado | sem_linha_empenhado | numero_de_outro_ano | numero_sem_ano | elemento_muda_dentro_do_empenho | liquidado_maior_que_empenhado |
|---|---|---|---|---|---|---|---|
| 6.330.338 | 12.492 | 3.047 | 9.978 | 185 | 0 | 1.227 | 1.512 |

Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:

| municipio_tcesp | liquidado_maior_que_empenhado |
|---|---|
| Jundiaí | 898 |
| Itapira | 220 |
| Caraguatatuba | 121 |
| Diadema | 57 |
| Três Fronteiras | 47 |


## Linhas duplicadas por município (as 8 maiores)


| municipio_tcesp | linhas_duplicadas | valor_empenhado_duplicado |
|---|---|---|
| Franca | 3.723 | 14.824.814,21 |
| Itirapuã | 3.644 | 9.494.057,73 |
| São José da Bela Vista | 2.611 | 5.413.352,91 |
| São José do Rio Pardo | 1.962 | 3.466.133,21 |
| Rincão | 300 | 591.457,36 |
| São José dos Campos | 92 | 263.353,30 |
| Diadema | 67 | 3.365.555,16 |
| Embu das Artes | 22 | 41.938,06 |


## Empenhos sem linha 'Empenhado', pelo ano do número do empenho


| ano_empenho | empenhos | pago |
|---|---|---|
| 2.010 | 9.975 | 473.782.860,35 |
| 2.009 | 3 | 0,00 |


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

Órgãos distintos: 1741. Municípios com uma prefeitura: 644.

Municípios com zero ou mais de uma prefeitura:

| municipio_tcesp | prefeituras |
|---|---|


## Órgãos que não são prefeitura, pela primeira palavra


| primeira_palavra | orgaos | exemplo |
|---|---|---|
| CAMARA | 644 | CÂMARA MUNICIPAL DA ESTANCIA HIDROMINERAL DE SERRA NEGRA |
| INSTITUTO | 111 | INSTITUTO DA PREVIDÊNCIA MUNICIPAL DE DIRCE REIS |
| FUNDACAO | 66 | FUNDACAO DE PESQUISA E TECNOLOGIA AGRICOLA |
| SERVICO | 53 | SERVICO DE AGUA E ESGOTO DO MUNICIPIO DE JAU |
| FUNDO | 46 | FUNDO APOSENTADORIA DO MUNICÍPIO DE CRAVINHOS |
| DEPARTAMENTO | 11 | DEPARTAMENTO AUT DE AGUA E ESGOTO DE PENAPOLIS |
| AUTARQUIA | 8 | AUTARQUIA DE ESPORTE DE ASSIS |
| CAIXA | 8 | CAIXA BENEFICENTE DOS SERV. MUNICIPAIS FLORIDA PTA |
| INST | 7 | INST PREVID SOC FUNC PÚBL DA EST TUR PARANAPANEMA |
| SAAE | 7 | SAAE - AMBIENTE |
| AGENCIA | 6 | AGENCIA REGUL.SERV. AGUA E ESGOTO - ARSAE |
| EMPRESA | 6 | EMPRESA DE TRANSPORTES COLETIVOS DE SÃO BERNARDO DO CAMPO |


## Identificador do fornecedor


| tipo_identificador | empenhos |
|---|---|
| CNPJ - PESSOA JURÍDICA | 4.039.664 |
| IDENTIFICAÇÃO ESPECIAL - SEM CPF/CNPJ | 945.366 |
| PESSOA FÍSICA | 880.724 |
| INSCRIÇÃO GENÉRICA-OUTROS | 441.422 |
| None | 9.975 |
| INSCRIÇÃO GENÉRICA-RESTOS A PAGAR-EXERCÍCIOS ANTERIORES | 8.590 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-NATUREZA ALIMENTAR | 3.500 |
| INSCRIÇÃO GENÉRICA-SENTENÇAS JUDICIAIS-OUTROS | 657 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-OUTROS | 413 |
| INSCRIÇÃO GENÉRICA-PRECATÓRIOS-NATUREZA ALIMENTAR | 27 |

| cnpjs_distintos | validos | invalidos | exemplo_invalido |
|---|---|---|---|
| 184.253 | 183.724 | 529 | 00000000000000 |

| digitos_no_arquivo | empenhos |
|---|---|
| 14 | 4.039.664 |


## Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de 2010

Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%. Linhas da Receita casadas mas malformadas, ignoradas: 0.

| cnpj_basicos | achados_na_receita |
|---|---|
| 174.379 | 174.357 |


## Cobertura do CNAE (estabelecimentos, snapshot 2026-10)

Linhas casadas mas malformadas, ignoradas: 0.

| cnpjs_validos | achados | baixados_hoje |
|---|---|---|
| 183.724 | 183.519 | 50.325 |










## Funil de limpeza

Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.

| ordem | motivo | descricao | empenhos | valor_liquido | cnpjs |
|---|---|---|---|---|---|
| 1 | sem_empenho_no_ano | sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento) | 9.978 | -8.129.024,32 | 1 |
| 2 | orgao_nao_prefeitura | órgão não é a prefeitura (Câmara, autarquia, fundo, fundação) | 706.782 | 8.196.190.618,92 | 59.072 |
| 4 | nao_cnpj | fornecedor não é pessoa jurídica (pessoa física, identificação especial) | 2.030.236 | 20.546.136.902,95 | 0 |
| 5 | cnpj_invalido | CNPJ com dígito verificador inválido | 12.196 | 70.260.339,27 | 478 |
| 6 | elemento_fora | elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões | 275.732 | 6.471.405.608,64 | 1.848 |
| 7 | nao_aplicacao_direta | modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário | 64.982 | 1.905.077.868,13 | 7.548 |
| 8 | ente_publico | natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038) | 136.139 | 2.187.226.453,31 | 2.182 |
| 9 | concessionaria_ou_banco | CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco | 386.186 | 1.430.842.542,80 | 934 |
| 10 | emissora_de_vale | emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores | 28.679 | 683.679.363,20 | 206 |
| 11 | valor_nao_positivo | valor líquido empenhado menor ou igual a zero | 104.864 | -497.562,36 | 35.796 |
| 99 | MANTIDO | None | 2.574.564 | 20.666.315.834,44 | 149.248 |

| municipios_na_rede |
|---|
| 644 |


## Rede prefeitura-fornecedor

Arestas município-CNPJ: 340.342.

| fornecedores | mediana_municipios_por_fornecedor | max_municipios |
|---|---|---|
| 149.248 | 1,00 | 434 |


## Modalidade de licitação dos empenhos mantidos


| modalidade_licitacao | empenhos | valor |
|---|---|---|
| PREGÃO | 370.928 | 5.391.010.171,52 |
| CONCORRÊNCIA | 29.283 | 4.879.219.806,00 |
| DISPENSA DE LICITAÇÃO | 1.361.506 | 3.438.555.322,03 |
| OUTROS/NÃO APLICÁVEL | 560.024 | 3.309.059.636,31 |
| TOMADA DE PREÇOS | 50.591 | 1.416.901.899,90 |
| CONVITE | 113.209 | 1.368.918.055,57 |
| INEXIGÍVEL | 72.858 | 513.657.768,01 |
| BEC-BOLSA ELETRÔNICA DE COMPRAS | 15.870 | 293.347.769,99 |
| CONCURSO | 295 | 55.645.405,11 |


## Removidos pela regra de CNAE (os 15 maiores)


| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 33050196000188 | C P F L | Distribuição de energia elétrica | 228 | 283.287.332,75 |
| 02558157000162 | TELECOMUNICACOES .DE S.PAULO S.A. TELESP | Serviços de telecomunicações sem fio não especificados anteriormente | 523 | 224.050.825,25 |
| 02328280000197 | E L E K T R O  -  Eletricidade e Serviços S.A. | Distribuição de energia elétrica | 199 | 151.484.774,54 |
| 43776517000180 | CIA  DE  SANEAM  BAS  EST  S  PAULO SABESP | Captação, tratamento e distribuição de água | 320 | 112.768.375,82 |
| 02302100000106 | BANDEIRANTE  ENERGIA S.A | Distribuição de energia elétrica | 29 | 109.107.798,06 |
| 61695227000193 | ELETROPAULO ELETRICIDADE DE SAO PAULO S/A | Distribuição de energia elétrica | 22 | 108.690.793,37 |
| 04172213000151 | CIA PIRATININGA DE FORCA E LUZ | Distribuição de energia elétrica | 26 | 103.761.201,98 |
| 43642727000185 | TELEC.DE SAO PAULO S/A. TELESP | Serviços de telefonia fixa comutada - STFC | 121 | 26.705.808,75 |
| 61116265000306 | CIA LUZ  E FORÇA SANTA CRUZ | Distribuição de energia elétrica | 24 | 20.179.475,18 |
| 61695227000517 | ELETROPAULO ELET. DE S.PAULO | Distribuição de energia elétrica | 3 | 18.339.383,02 |
| 02449992005638 | BANCO BRASIL | Telefonia móvel celular | 435 | 15.581.111,43 |
| 07282377000120 | CAIUA DISTRIBUICAO DE ENERGIA S A | Distribuição de energia elétrica | 19 | 15.500.184,14 |
| 07297359000111 | E.D.E. VALE PARANAPANEMA S/A. | Distribuição de energia elétrica | 22 | 14.634.971,52 |
| 90400888000142 | BANCO  SANTANDER | Bancos múltiplos, com carteira comercial | 154 | 11.630.133,84 |
| 61416244000144 | C. N. E. E. | Distribuição de energia elétrica | 14 | 10.568.003,28 |


## Fornecedores mantidos que parecem emissoras de vale

Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.

| raiz | fornecedor | cnae | empenhos_vale | empenhos | valor |
|---|---|---|---|---|---|
| 05810218 | MARIA ELENA SANITA BONFIETTI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 157 | 255 | 287.159,94 |
| 05112616 | LUIZ CARLOS PATRIAN - ME | Comércio varejista de carnes - açougues | 217 | 229 | 133.869,19 |
| 67191700 | EDUARDO CARLOS BONACI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 48 | 55 | 129.369,15 |
| 29055993 | SINDICATO DAS EMPRESAS DE TRANSP DE PASSAGEIROS DE B MANSA E V REDONDA | Atividades de organizações associativas patronais e empresariais | 32 | 38 | 101.117,46 |
| 47716873 | ZANATTA E CIA LTDA | Serviços combinados de escritório e apoio administrativo | 11 | 19 | 81.950,00 |
| 01564249 | DANIEL H. MARINELLI VERA CRUZ | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 12 | 16 | 72.303,73 |
| 11419663 | ONIX - PARTICIPACOES E EMPREENDIMENTOS LTDA | Gestão e administração da propriedade imobiliária | 44 | 48 | 56.361,70 |
| 06129146 | CRISTOVAO ALBARRACIM FILHO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 26 | 28 | 55.190,00 |
| 02911243 | ASSOCIACAO DOS MORADORES DO BAIRRO DO JD ELDORADO | Atividades de associações de defesa de direitos sociais | 8 | 11 | 49.951,60 |
| 06259395 | ASSOC DOS AMIGOS DO BAIRRO OURO FINO | Atividades de associações de defesa de direitos sociais | 8 | 11 | 49.440,72 |
| 06186144 | ASSOC DOS MOR DOS B CACHOEIRA E CHAC ITAPETI | Atividades de organizações religiosas ou filosóficas | 8 | 11 | 45.685,35 |
| 09376777 | ARLETE ALECIA MOREIRA DE SOUZA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 44 | 45 | 39.260,00 |
| 54791470 | ASSOC DOS AMIGOS  B V GUILHERME E V GUMERCINDO | Atividades de associações de defesa de direitos sociais | 8 | 11 | 23.198,60 |
| 05211992 | NAIR CORREA M. PINTO V. CRUZ - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 11 | 18 | 22.785,51 |
| 52368644 | ASSOC DOS MOR DOS B VL N S ISABEL E CRUZEIRO | Atividades de associações de defesa de direitos sociais | 8 | 11 | 21.644,64 |
| 48804561 | MIGUEL CASTILHO FERRES | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 12 | 12 | 19.850,00 |
| 04293918 | S.J. DE LIMA TAQUARIVAI - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados | 44 | 53 | 17.380,00 |
| 08468981 | BRITO E PIAM COMERCIAL DE ALIMENTOS LTDA- ME | Comércio varejista de bebidas | 123 | 123 | 16.656,00 |
| 05700803 | JOSE ANTONIO RODRIGUES ACOUGUE - ME | Comércio varejista de carnes - açougues | 12 | 12 | 13.040,00 |
| 02669977 | MERCEARIA COSTA INDIANA LTDA-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 27 | 27 | 12.900,00 |
| 02766212 | C.E.DE SOUZA ALVARES MACAHDO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 24 | 11.820,00 |
| 64696396 | DIRCE FUSO MINCA-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 24 | 8.520,00 |
| 09625409 | EDGAR DA SILVA EMPORIO - ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 12 | 8.360,00 |
| 50743913 | ALCENY GARBULLIO E CIA LTDA ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 4 | 6 | 8.250,00 |
| 04069189 | SUPERMERCADO NOVA AMERICA LTDA-ME | Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns | 12 | 24 | 7.860,00 |


## Os 30 maiores fornecedores mantidos

Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.

| cnpj | fornecedor | cnae | municipios | valor |
|---|---|---|---|---|
| 73188336000101 | LOGIC ENGENHARIA E CONSTRUCAO LTDA | Construção de edifícios | 14 | 210.216.843,66 |
| 61699567000192 | SECRETARIA DE ESTADO DA SAUDE | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 5 | 179.143.847,21 |
| 49957137000128 | TERMAQ   TERRAPLENAGEM  CONSTR  CIVIL E ESCAVACOES LTDA | Construção de edifícios | 11 | 149.668.037,82 |
| 62436282000121 | GERALDO J  COAN   CIA  LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 32 | 128.267.657,90 |
| 56473317000108 | EMPARSANCO S A | Construção de rodovias e ferrovias | 3 | 115.211.364,24 |
| 53437315000167 | COMERCIAL JOAO AFONSO  N | Comércio atacadista de produtos alimentícios em geral | 162 | 101.722.948,79 |
| 14310577000104 | CONSORCIO NOVO CANUDOS | Outras obras de engenharia civil não especificadas anteriormente | 4 | 100.211.953,27 |
| 50944198000130 | HOSPITAL DE CARIDADE S.VICENTE DE PAULA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 96.942.398,25 |
| 46044368000152 | SERVIÇO DE SAÚDE DR. CÂNDIDO FERREIRA | Atividades de assistência psicossocial e à saúde a portadores de distúrbios psíquicos, deficiência mental e dependência química e grupos similares não | 1 | 96.859.966,80 |
| 47497367000126 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 7 | 92.753.329,32 |
| 08493239000152 | CONSORCIO TECAM - TECNOLOGIA AMBIENTAL | Coleta de resíduos não-perigosos | 1 | 88.535.369,65 |
| 62162847000120 | JOFEGE - PAVIMENTACAO E CONSTRUCAO LTDA | Construção de rodovias e ferrovias | 14 | 83.138.397,17 |
| 49254634000160 | NUTRIPLUS ALIMENTACAO E TECNOLOGIA LTDA | Fornecimento de alimentos preparados preponderantemente para empresas | 11 | 79.042.922,35 |
| 61699567001245 | SPDM ASSOC PAULISTA P/O DESENV DA MEDICINA | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 1 | 77.108.948,99 |
| 24232886005711 | PRO SAUDE   ASSOCIACAO BENEFICIENTE DE ASSISTENCIA SOCIA | Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências | 1 | 76.125.286,00 |
| 75154385000140 | CONSTRUTORA ESTRUTURAL LTDA | Construção de rodovias e ferrovias | 37 | 74.808.346,34 |
| 55333769000113 | ENCALSO CONSTRUCOES LTDA | Construção de rodovias e ferrovias | 7 | 73.085.542,09 |
| 46020301000269 | SOCIEDADE CAMPINEIRA DE EDUCAÇÃO E INSTRUÇÃO | Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências | 2 | 72.181.066,88 |
| 47497367000398 | TERRACOM CONSTRUCOES LTDA | Coleta de resíduos não-perigosos | 1 | 70.738.388,94 |
| 61836813000100 | QUITAUNA SERVICOS LTDA | Coleta de resíduos não-perigosos | 1 | 68.230.899,28 |
| 02671087000154 | M.W.E. - PAVIMENTACAO E CONSTRUCAO LTDA. | Obras de urbanização - ruas, praças e calçadas | 6 | 65.610.331,15 |
| 55996615000101 | CONSLADEL - CONST. E LACOS DETET. E ELETRONIC | Construção de edifícios | 9 | 64.225.595,38 |
| 99999999000191 | CONSORCIO SBC AMBIENTAL | None | 1 | 63.846.283,91 |
| 57543001000108 | LARA CENTRAL DE TRATAMENTO DE RESIDUOS LTDA | Coleta de resíduos não-perigosos | 7 | 62.986.948,45 |
| 05252462000110 | YTAQUITI CONSTRUTORA LTDA | Obras de urbanização - ruas, praças e calçadas | 4 | 61.108.934,70 |
| 02293852000140 | S.P.  ALIMENTAÇÃO E SERVIÇOS LTDA.- | Fornecimento de alimentos preparados preponderantemente para empresas | 7 | 58.169.450,67 |
| 01059631000149 | EPPO SANEAMENTO AMBIENTAL E OBRAS  LTDA | Coleta de resíduos não-perigosos | 4 | 55.496.577,07 |
| 03189580000103 | DEMOP - PARTICIPACOES LTDA | Outras obras de engenharia civil não especificadas anteriormente | 73 | 54.855.332,72 |
| 62011788000199 | LITUCERA LIMPEZA E ENGENHARIA LTDA | Coleta de resíduos não-perigosos | 10 | 53.864.210,65 |
| 08528442000117 | NUTRICIONALE  COMERCIO  DE ALIMENTOS  LTDA | Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente | 328 | 51.986.400,34 |
