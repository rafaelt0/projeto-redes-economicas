#!/usr/bin/env bash
# Confere, sem passar pelo limpar_ano.py, empenhos e valor empenhado de alguns municípios:
# awk no CSV bruto de um lado, o Parquet de empenhos do outro.
# Uso: codigo/origem_dos_dados/conferir_ano.sh 2013 Adamantina "Monte Mor"
set -euo pipefail
ano=$1; shift
raiz=$(cd "$(dirname "$0")/../.." && pwd)
zip="$raiz/dados/brutos/tcesp/despesas-$ano.zip"
parquet="$raiz/dados/limpos/empenhos_$ano.parquet"
alvos=$(printf '%s\n' "$@" | paste -sd '|')

# Chave da cópia igual à do script: município, órgão, empenho, identificador, tipo, data, valor e elemento.
# O layout de 2018 em diante divide o identificador em duas colunas; o awk acha as posições pelo cabeçalho.
awk_saida=$(unzip -p "$zip" | iconv -f latin1 -t utf-8 | awk -F';' -v alvos="$alvos" '
NR == 1 {
    for (i = 1; i <= NF; i++) c[$i] = i
    n = split(alvos, lista, "|"); for (i = 1; i <= n; i++) quer[lista[i]] = 1
    next
}
!($c["ds_municipio"] in quer) || $c["tp_despesa"] != "Empenhado" { next }
{
    ident = ("identificador_despesa" in c) ? $c["identificador_despesa"] : $c["tp_identificador_despesa"] " - " $c["nr_identificador_despesa"]
    emp = $c["ds_municipio"] SUBSEP $c["ds_orgao"] SUBSEP $c["nr_empenho"] SUBSEP ident
    copia = emp SUBSEP $c["dt_emissao_despesa"] SUBSEP $c["vl_despesa"] SUBSEP $c["ds_elemento"]
    if (copia in visto) next
    visto[copia] = 1
    v = $c["vl_despesa"]; gsub(/\./, "", v); sub(/,/, ".", v)
    if (!(emp in empenhos)) { empenhos[emp] = 1; n_emp[$c["ds_municipio"]]++ }
    soma[$c["ds_municipio"]] += v
}
END { for (m in n_emp) printf "awk\t%s\t%d\t%.2f\n", m, n_emp[m], soma[m] }' | sort)

parquet_saida=$("${PYTHON:-$raiz/.venv/bin/python}" -I -c "
import duckdb, sys
for m in sys.argv[2:]:
    n, v = duckdb.execute(\"SELECT count(*), sum(v_empenhado) FROM read_parquet(?) WHERE municipio_tcesp = ? AND n_linhas_empenho > 0\", [sys.argv[1], m]).fetchone()
    print(f'parquet\t{m}\t{n}\t{v or 0:.2f}')
" "$parquet" "$@" | sort)

printf '%s\n' "$awk_saida" "$parquet_saida"
if [ "$(cut -f2- <<<"$awk_saida")" != "$(cut -f2- <<<"$parquet_saida")" ]; then
    echo "conferência de $ano: awk e Parquet divergem" >&2
    exit 1
fi
