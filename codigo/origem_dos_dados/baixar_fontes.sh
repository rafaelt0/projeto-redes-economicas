#!/usr/bin/env bash
# Baixa as fontes que não dependem do ano do TCESP: municípios do IBGE, candidaturas do TSE e cadastro da Receita
# (seguido do extrato em Parquet). Pula o que já existe; um download interrompido continua de onde parou.
# Uso: codigo/origem_dos_dados/baixar_fontes.sh [ibge] [tse] [receita]   (sem argumento, as três)
# APAGAR_BRUTOS=1 apaga os zips da Receita (6,4 GB) depois do extrato.
set -euo pipefail
raiz=$(cd "$(dirname "$0")/../.." && pwd)
brutos="$raiz/dados/brutos"
limpos="$raiz/dados/limpos"
python=${PYTHON:-$raiz/.venv/bin/python}
# Lote do cadastro usado no trabalho. Outro lote muda as exclusões por natureza jurídica e CNAE, e com elas os resultados.
lote_receita=2026-10

baixar() {  # url destino [opções extras do curl]
    local url=$1 destino=$2
    shift 2
    [ -s "$destino" ] && return
    mkdir -p "$(dirname "$destino")"
    curl -sfL --retry 10 --retry-all-errors -C - "$@" -o "$destino.parcial" "$url"
    mv "$destino.parcial" "$destino"
}

ibge() {
    baixar "https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios" "$brutos/ibge/municipios_sp.json"
}

tse() {
    local ano csv zip
    for ano in 2008 2012 2016 2020; do
        csv="$brutos/tse/$ano/consulta_cand_${ano}_SP.csv"
        [ -s "$csv" ] && continue
        zip="$brutos/tse/consulta_cand_$ano.zip"
        baixar "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_$ano.zip" "$zip"
        mkdir -p "$(dirname "$csv")"
        unzip -p "$zip" "consulta_cand_${ano}_SP.csv" > "$csv.parcial"
        mv "$csv.parcial" "$csv"
        rm "$zip"
    done
}

receita() {
    local nome
    if [ -s "$limpos/receita_empresas.parquet" ] && [ -s "$limpos/receita_estabelecimentos.parquet" ] \
        && [ -s "$limpos/receita_naturezas.parquet" ] && [ -s "$limpos/receita_cnaes.parquet" ]; then
        return
    fi
    for nome in Empresas{0..9} Estabelecimentos{0..9} Naturezas Cnaes; do
        baixar "https://arquivos.receitafederal.gov.br/public.php/webdav/Dados/Cadastros/CNPJ/$lote_receita/$nome.zip" \
            "$brutos/receita/$nome.zip" -u "gn672Ad4CF8N6TK:"  # token público de compartilhamento
        unzip -tq "$brutos/receita/$nome.zip" >/dev/null
    done
    "$python" -I "$raiz/codigo/origem_dos_dados/extrair_receita.py"
    if [ "${APAGAR_BRUTOS:-0}" = 1 ]; then
        rm -f "$brutos/receita/"*.zip
    fi
}

[ $# -gt 0 ] || set -- ibge tse receita
for fonte in "$@"; do
    case $fonte in
        ibge | tse | receita) "$fonte" ;;
        *) echo "fonte desconhecida: $fonte (use ibge, tse ou receita)" >&2; exit 2 ;;
    esac
done
