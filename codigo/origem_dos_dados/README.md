# Origem dos dados

Estes scripts geraram os Parquets da release `dados-v1`, a partir das fontes públicas. Eles **não fazem parte da
reprodução**: `reproduzir.py` parte da release. Ficam aqui para que as regras de limpeza possam ser lidas e
conferidas, em especial a lista `REGRAS` de `limpar_ano.py`, que decide quais empenhos saem da rede e por quê.

Rodam só em Linux (usam `bash`, `curl`, `unzip`, `iconv`, `awk` e pipe nomeado) e levam de 8 a 14 horas, quase
tudo nos 16 anos do TCESP, com cerca de 30 GB de downloads.

| Ordem | Script | Faz | Saída |
|---|---|---|---|
| 1 | `baixar_fontes.sh` | Baixa IBGE, TSE (2008 a 2020) e o cadastro CNPJ da Receita (lote de outubro de 2026); chama `extrair_receita.py` | `dados/brutos/`, `dados/limpos/receita_*.parquet` |
| 2 | `processar_ano.sh ANO` | Baixa um ano do TCESP, limpa com `limpar_ano.py` e confere contagens e valores por `awk` no CSV bruto (`conferir_ano.sh`) | `dados/limpos/{empenhos,rede}_{ano}.parquet`, `relatorios/relatorio_{ano}.md` |
| 3 | `juntar_tse.py` | Prefeitos eleitos, mandatos e transições | `dados/limpos/{prefeitos,mandatos,transicoes}.parquet`, `relatorios/relatorio_tse.md` |
| 4 | `medir_rede.py` | Rede por mandato e permanência das ligações em cada transição | `dados/limpos/{arestas_mandato,permanencia}.parquet`, `relatorios/relatorio_rede.md` |
| 5 | `montar_release.py` | Seleciona o que a reprodução lê e retira dados pessoais | `dados-reproducao-v1.zip` |

O passo 5 retira o que é dado pessoal e não entra em nenhuma conta: o CPF que a Receita põe no nome de
empresários individuais vira `***`, o título eleitoral dos prefeitos sai de `mandatos.parquet` e, do TSE, ficam
só as linhas de prefeito e as sete colunas usadas. Os relatórios em `relatorios/` passaram pela mesma máscara;
gerados de novo, voltam a mostrar o CPF.

Ambiente: Python 3.14 e DuckDB 2.0.0, por exemplo

```bash
uv venv --python 3.14 .venv && uv pip install --python .venv/bin/python duckdb==2.0.0
codigo/origem_dos_dados/baixar_fontes.sh
for ano in $(seq 2009 2024); do codigo/origem_dos_dados/processar_ano.sh $ano; done
.venv/bin/python -I codigo/origem_dos_dados/juntar_tse.py
.venv/bin/python -I codigo/origem_dos_dados/medir_rede.py
.venv/bin/python -I codigo/origem_dos_dados/montar_release.py . dados-reproducao-v1.zip
```

O resultado pode diferir da release: a Receita publica um lote por mês e retira os antigos, e o TCESP pode revisar
arquivos de anos passados. Particularidades das fontes, como encoding misto, mudança de layout em 2014 e zips em
Deflate64, estão comentadas nos próprios scripts.
