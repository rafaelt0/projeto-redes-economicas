<img src="assets/icon.svg" width="64" height="64" alt="">

# Persistência da rede prefeitura-fornecedor

A rede que liga empresas às prefeituras sobrevive quando muda o prefeito? O trabalho acompanha as ligações
prefeitura-fornecedor nos municípios paulistas fiscalizados pelo TCESP (a capital fica de fora), de 2009 a 2024:
quatro mandatos e três transições, nas eleições de 2012, 2016 e 2020.

Este repositório reproduz as tabelas, as figuras e a comparação regional do trabalho com um único comando, em
Windows, macOS ou Linux. O texto do trabalho é entregue à parte.

## Resultados

Amostra final: 1.951.293 ligações comparáveis em 635 municípios.

- Em média, 37,7% das ligações continuam no mandato seguinte.
- Quando mudam o prefeito e o partido, a continuidade é 2,38 pontos percentuais menor que nas sucessões sem troca
  de partido (IC 95%: −3,02 a −1,73). Trocar só o prefeito ou só a legenda não faz diferença detectável.
- Na decomposição padronizada, 71,4% dessa queda corresponde a fornecedores que perdem aquela prefeitura mas seguem
  vendendo a outras da rede observada. É uma alocação contábil, não um mecanismo.
- A hipótese de que fornecedores que fazem ponte entre partidos sobrevivem melhor à troca não se confirmou: atender
  só o partido que assume, comparado a atender só o que sai, dá +0,04 pp (IC 95%: −0,46 a 0,54).

O desenho é observacional e mostra associação, não efeito causal. Continuar não é favorecimento (pode ser
fornecedor único ou contrato longo), e sair não é necessariamente punição: muitas empresas fecharam depois.

Para ver sem rodar nada: [resultados em uma página](docs/publicacao/resultados.html),
[síntese](docs/publicacao/sintese.html), [quem são os fornecedores](docs/publicacao/fornecedores.html) e o
[desenho do projeto](docs/diagrama-projeto.html). Abra os arquivos baixados no navegador.

## Reproduzir

1. Instale o [uv](https://docs.astral.sh/uv/getting-started/installation/). Ele baixa o Python 3.14 e as
   bibliotecas nas versões usadas no trabalho, sem mexer no Python do sistema.
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - macOS e Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Clone o repositório e rode:

   ```
   git clone https://github.com/rafaelt0/projeto-redes-economicas.git
   cd projeto-redes-economicas
   uv run reproduzir.py
   ```

O comando roda os testes, baixa os dados da [release `dados-v1`](https://github.com/rafaelt0/projeto-redes-economicas/releases/tag/dados-v1)
(300 MB), confere o SHA-256 do arquivo, refaz a análise e compara o resultado com as tabelas versionadas. Termina
com `resultados iguais aos do repositório` ou com a lista do que mudou.

- Tempo: cerca de 5 minutos num notebook, mais o download. O painel com bootstrap leva a maior parte.
- Disco: cerca de 1 GB, quase tudo em `dados/` (pode apagar depois).
- `uv run reproduzir.py testes` roda só os testes, sem dados, em segundos.

A comparação aceita diferenças a partir do nono algarismo significativo, que surgem porque a álgebra linear muda
de biblioteca entre sistemas. No Linux, as saídas saem idênticas byte a byte, figuras inclusive. As figuras não
são comparadas em outros sistemas, porque a renderização das fontes muda.

## O que cada etapa faz

| Etapa (`codigo/`) | Faz | Saída |
|---|---|---|
| `preparar_publicacao.py` | Amostra auditada: exclui transições com eleição suplementar ou identidade duvidosa do prefeito | `docs/publicacao/*.csv`, `amostra-auditada.json` |
| `perfil_fornecedores.py` | Perfil descritivo dos fornecedores | `tabelas/perfil_fornecedores.json`, `fornecedores.html` |
| `estimar_painel.py` | Modelos de painel com efeitos fixos e erros-padrão agrupados | `tabelas/painel_*` |
| `decompor_publicacao.py` | Decomposição da menor continuidade pelo destino das ligações | `tabelas/decomposicao_*`, `docs/resultados-decomposicao.md` |
| `diagnosticar_tempo.py` | Continuidade ano a ano em torno da eleição | `tabelas/temporal_resultados.json` |
| `figuras_publicacao.py` | Figuras | `docs/publicacao/figuras/` |
| `tabelas_publicacao.py` | Correção de multiplicidade e manifesto | `tabelas/painel_multiplicidade.csv`, `manifesto-resultados.json` |
| `medir_regioes.py` | Comparação entre as 11 regiões intermediárias do IBGE | `relatorios/relatorio_regioes.md` |

O plano de análise, com o conjunto fechado de modelos e a regra de divulgação de nulos, está em
[`docs/protocolo-publicacao.md`](docs/protocolo-publicacao.md).

## De onde vêm os dados

A release traz os Parquets intermediários: a rede município-fornecedor de cada ano (2009 a 2024), a permanência
das ligações em cada transição, os mandatos e as transições, e extratos do TSE, da Receita e do IBGE. Eles saem
da cadeia completa em [`codigo/origem_dos_dados/`](codigo/origem_dos_dados/README.md), que limpa os 16 anos de
despesas do TCESP (cerca de 23 GB). Essa cadeia roda só em Linux e leva horas; está aqui para leitura e conferência
das regras de limpeza, não faz parte da reprodução. Os relatórios de cada etapa estão em `relatorios/`.

Dados pessoais que não entram em nenhuma conta foram retirados: o CPF que a Receita põe no nome de empresários
individuais aparece como `***`, e não há título eleitoral, CPF, e-mail ou data de nascimento de candidatos.

Fontes, todas públicas:

- TCESP, despesas municipais: <https://transparencia.tce.sp.gov.br/>
- TSE, candidaturas 2008 a 2020: <https://dadosabertos.tse.jus.br/>
- Receita Federal, cadastro CNPJ (lote de outubro de 2026): <https://arquivos.receitafederal.gov.br/>
- IBGE, municípios e regiões intermediárias de SP: <https://servicodados.ibge.gov.br/api/docs/localidades>

## Licença

Código sob a licença MIT. Tabelas, figuras, relatórios e dados da release sob CC BY 4.0, citando as fontes acima.
Detalhes em [`LICENSE`](LICENSE).
