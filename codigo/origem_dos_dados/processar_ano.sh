#!/usr/bin/env bash
# Baixa, limpa e confere um ano. Por padrão não apaga nada: o zip e o bruto ficam até a revisão do relatório.
# Uso: codigo/origem_dos_dados/processar_ano.sh 2009
# APAGAR_BRUTOS=1 apaga o zip do TCESP e o Parquet bruto depois da conferência por awk (1 a 2 GB por ano).
set -euo pipefail
ano=$1
raiz=$(cd "$(dirname "$0")/../.." && pwd)
python=${PYTHON:-$raiz/.venv/bin/python}
zip="$raiz/dados/brutos/tcesp/despesas-$ano.zip"
cd "$raiz"
if [ ! -f "$zip" ]; then
    mkdir -p "$(dirname "$zip")"
    curl -sf --retry 10 --retry-all-errors -C - -A "Mozilla/5.0" -o "$zip.parcial" "https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-$ano.zip"
    mv "$zip.parcial" "$zip"
fi
unzip -tq "$zip"
"$python" -I codigo/origem_dos_dados/limpar_ano.py "$ano"
codigo/origem_dos_dados/conferir_ano.sh "$ano" Adamantina "Monte Mor" Campinas
if [ "${APAGAR_BRUTOS:-0}" = 1 ]; then
    rm -f "$zip" "$raiz/dados/limpos/despesas_${ano}_bruto.parquet"
fi
