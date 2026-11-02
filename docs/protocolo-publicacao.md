# Protocolo da revisão para publicação

31 de outubro de 2026. Plano registrado depois de conhecidos os resultados
estaduais e regionais originais. Não constitui pré-registro prospectivo.

## Objetivo e critério de encerramento

Produzir manuscrito completo em português, referências verificadas, figuras,
resultados reproduzíveis e auditoria independente. A autorização do usuário
abrange mudanças de modelos e especificações e trabalho delegado. A aceitação
por periódico e a existência de um resultado surpreendente não são garantidas.
Encerra-se a busca após executar e auditar o conjunto finito abaixo, mesmo que
as conclusões sejam nulas. Novidade deve resultar de uma distinção substantiva
ou de medição, jamais da seleção de um valor-p.

## População e estimandos

Preservar os dados e relatórios legados. Unidade principal: aresta
município–raiz CNPJ no mandato anterior × transição. Comparáveis: mandatos
sem suplementares registradas e partidos/prefeitos conhecidos. Ausência de
suplementar não garante exercício do mesmo prefeito durante todo o mandato.
Região, CNAE e cadastro são os retratos disponíveis, sujeitos aos limites já
documentados. Todos os novos resultados são análises retrospectivas.

1. Reproduzir a associação original de alternância e sua decomposição em
   continuidade, perda do município com permanência em outro cliente e saída
   da rede observada. Usar a mesma população, estratos e pesos nos destinos
   para obter uma identidade contábil; não condicionar a permanência futura.
2. Separar quatro transições: mantém prefeito/partido; mantém prefeito e muda
   partido; muda prefeito e mantém partido; muda ambos. Comparar mudanças de
   partido entre sucessões de prefeito, sem equiparar diferenças a causalidade.
3. Comparar conjuntamente os vínculos prévios com partido novo e antigo:
   nenhum, apenas novo, apenas antigo e ambos. O contraste apenas novo menos
   apenas antigo tem suporte próprio e não é a diferença de duas médias sobre
   estratos distintos. Vínculo comercial não mede filiação ou relação pessoal.
4. Auditar a janela temporal: fornecedores presentes em algum dos quatro anos
   versus presentes no último ano anterior à eleição; continuidade no primeiro
   ano seguinte e em qualquer ano do mandato seguinte. Eventual diferença
   identifica sensibilidade de medição, não prova efeito da eleição.

## Especificações e inferência

- Reproduzir a diferença padronizada de riscos com estratos de faixa de
  clientes × divisão CNAE × transição e pesos n1*n0/(n1+n0).
- Reamostrar municípios em pelo menos 1.999 réplicas para os contrastes
  principais novos; conservar juntas as observações do mesmo município.
- Modelos lineares de probabilidade com controles anteriores, efeitos fixos
  municipais e de transição/setor; sensibilidade com efeitos fixos de
  fornecedor × transição, se identificável e convergente. Para vínculos
  partidários, efeitos de município × transição e fornecedor × transição.
- Covariância agrupada por município e fornecedor, com correção da interseção,
  contagens de grupos e diagnóstico de matrizes/convergência explícitos.
- Informar todas as especificações planejadas, precisão, suporte e limitações.
  Contrastes adicionais e regionais são exploratórios; corrigir a família de
  testes quando apresentada como busca de heterogeneidade. ICs individuais não
  testam diferenças entre regiões. Não converter não significância em equivalência.
- Não implementar regressão descontínua sem votos, variável de ordenação e
  hipótese de identificação válidos. Falta desse desenho deve constar como limite.

## Implementação e verificação

Scripts separados em `codigo/`, resultados leves em
`dados/limpos/publicacao/`, tabelas/figuras/manuscrito em `docs/`. Python do
`.venv`, DuckDB, NumPy, SciPy e Matplotlib. Funções estatísticas testadas em
amostras com resposta conhecida e comparadas a cálculos independentes. Comando
de testes: `uv run reproduzir.py testes`.
Incluir comandos de reprodução e versões das dependências na entrega.

## Divisão de trabalho e limites

Agente de inferência: modelos e testes. Agente de desenho: auditoria independente
das definições, população e identificação. Agente de literatura de outro modelo:
fontes primárias, contribuição e crítica editorial. Agente principal: protocolo,
decomposições, integração, manuscrito e conferência final. Revisão adversarial
final recebe artefatos e contrato; objeções são resolvidas ou registradas.
Não alterar bases originais, não apagar dados, não fazer commit/push, não
publicar nem submeter a periódico sem autorização específica.

## Adendo após a primeira rodada

Os quatro grupos e a janela temporal revelaram diferenças que devem ser
testadas diretamente: incluir o contraste de interação
`ambos − só prefeito − só partido` no mesmo modelo, e repetir as especificações
de quatro transições na população presente no último ano, com retorno no
primeiro ano e em qualquer ano seguinte. Repetir a decomposição de continuidade
e perda do cliente com permanência em outro município com covariância em duas
dimensões. Essas extensões foram definidas após observar os resultados de
decomposição e são explicitamente exploratórias, não confirmação prospectiva.
Não abrir uma sequência de novos subgrupos se algum contraste não funcionar.

Após a auditoria, a fonte única das estimativas novas é
`dados/limpos/publicacao/permanencia_auditada.parquet`, produzida por
`preparar_publicacao.py`. Detectar suplementares em todas as candidaturas,
independentemente do vencedor; excluir os dois lados de cada mandato afetado.
Exposições partidárias usam só clientes externos sem suplementar registrada
no mandato anterior. Acrescentar retorno nos anos 2–4 do novo mandato como
sensibilidade à herança de despesas no primeiro ano, motivada pela literatura.
O primeiro ano não é todo determinado pelo antecessor: a exclusão é teste de
sensibilidade, não correção que isola compras do novo governo.

Diagnóstico temporal adicional, definido antes de calculá-lo: taxas de retorno
anual de cada município entre três anos antes e três depois da fronteira do
mandato, agrupadas pela categoria política da eleição. Mesmo peso por
município–eleição e bootstrap por município. Comparar a mudança na fronteira
com a média das três taxas anteriores; diferenças anteriores entre os grupos
enfraquecem a interpretação de ruptura concentrada na transição. As janelas
se sobrepõem e não constituem estudo de evento causal nem teste completo de
tendências paralelas; nenhuma seleção de largura de janela após os resultados.

## Reparo motivado pelos pareceres independentes

O arquivo de candidaturas de 2008 não contém todas as suplementares de
2009–2012. Status eleitorais podem ser retrospectivos. A amostra principal
passa a excluir conservadoramente transições com candidatura ordinária cassada,
cassada com recurso ou cancelada em qualquer mandato adjacente, e casos de
2016 cujo vencedor declara reeleição mas difere do titular anterior. A regra
é aplicada a todos os municípios, não apenas aos casos que alteram o resultado.
Preservar a amostra intermediária e registrar as exclusões. Não chamar isso de
reconstrução completa da história de posse; ela permanece indisponível.

Sensibilidades adicionais fechadas: repetir M4 e E2 sem a transição de 2012;
repetir E2 sem qualquer cliente externo com partido incerto, suplementar ou
outro sinal observável de identidade duvidosa no mandato anterior. Essas
exclusões mudam a população e devem ser apresentadas, inclusive se os resultados
contrariarem o texto anterior. Incluir todos os destinos e todos os contrastes
já calculados nos apêndices. Atualizar rastreabilidade por hash em cada etapa.

## Adendo após o parecer independente de 31/10/2026

Um parecer independente, que não acompanha este repositório, registrou que a parcela de
71,4% podia ser lida como mecanismo de recomposição, quando a composição dos
destinos entre quem perde o cliente é quase invariante. Antes de alterar o
pipeline, um registro de reparo (também fora deste repositório) fixou um diagnóstico com os dados já
existentes: parcela condicional de cada destino entre as ligações que não
continuam, decomposição da diferença de “segue na rede” em nível e composição,
e parcelas por tamanho de carteira. A regra de leitura foi registrada antes da
execução. Não é nova especificação, subgrupo ou janela, e não seleciona
resultados por significância; se a composição fosse pequena, o texto passaria a
tratar a parcela como identidade contábil. O diagnóstico foi incorporado ao
pipeline e ao apêndice, com os mesmos estratos, pesos e bootstrap.
