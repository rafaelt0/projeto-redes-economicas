"""Protótipo: valida e limpa um ano de despesas do TCESP.

Uso: .venv/bin/python -I codigo/origem_dos_dados/limpar_ano.py 2012
"""

import csv
import gzip
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import duckdb

ANO = int(sys.argv[1])
RAIZ = Path(__file__).resolve().parents[2]
TCESP = RAIZ / "dados/brutos/tcesp"
IBGE = RAIZ / "dados/brutos/ibge/municipios_sp.json"
LIMPOS = RAIZ / "dados/limpos"
ZIP = TCESP / f"despesas-{ANO}.zip"
CSV_UTF8 = LIMPOS / "tmp" / f"despesas-{ANO}.utf8.csv.gz"
REPAROS = LIMPOS / f"despesas_{ANO}_reparos_encoding.json"
BRUTO = LIMPOS / f"despesas_{ANO}_bruto.parquet"
REJEITADAS = LIMPOS / f"despesas_{ANO}_rejeitadas.parquet"
EMPENHOS = LIMPOS / f"empenhos_{ANO}.parquet"
REDE = LIMPOS / f"rede_{ANO}.parquet"
RELATORIO = RAIZ / f"relatorios/relatorio_{ANO}.md"

# Grafias do TCESP que não batem com o nome atual do IBGE, preenchidas após a primeira rodada.
APELIDOS = {"Florínia": "Florínea", "São Luís do Paraitinga": "São Luiz do Paraitinga"}

# Histórico que fala de vale. Exclui empenho a empenho nas empresas de ônibus (CNAE 492), que vendem vale-transporte e
# também fazem fretamento, e nos sindicatos (9420100), que repassam vale-alimentação; nos demais ramos serve para achar
# emissoras novas.
HISTORICO_VALE = r"VALE[ -]*(ALIMENTA|REFEI|TRANSPORTE|COMPRA)|CARTA?O[ -]*(ALIMENTA|REFEI)|TICKET|AUXILIO[ -]*ALIMENTA"

# Emissoras de cartão-benefício que a Receita classifica fora do CNAE 8299702 (Trivale, Planinvest, VS Card, Ticket),
# achadas pelo nome ou pelo histórico e conferidas à mão. O relatório lista candidatas a cada ano.
VALES_FORA_DO_CNAE = [
    "00604122", "02959392", "09517584", "47866934",  # 2012: Trivale, Planinvest, VS Card, Ticket
    "04432048", "12826444", "62876768", "49609365", "08422119",  # 2013: Empório Card, Ecopag, Accredito, ACI Rio Pardo, Unik
    "12988406", "04141393", "57494130", "74504937", "05208850",  # 2013: associações que vendem vale-transporte
    "46481529", "00373484", "03007699",  # 2009: Translitoral (holding de ônibus), ACI Rio Pardo, RP Adm. de Convênios
    "05650182", "01178287",  # 2015: Bancred, Via Nova (vale-transporte)
    "03964735", "16814330", "21659864",  # 2018: AESA (vale-transporte), Berlin Finance, BR Mobilidade Baixada Santista
    "26069189", "02365154",  # 2019: M S Serviços Administrativos, R. S. Administradora
    "29387303", "48424063",  # 2020: Pamella R. Nardelli (cartão alimentação, Itapevi), ACE Penápolis
    "20895286", "49887805",  # 2022: Rom Card, ACI Garça
    "49930514", "49801756",  # 2024: Pluxee (ex-Sodexo Benefícios), ACE Itapeva
]

# Empresas de ônibus que a Receita de hoje classifica fora do CNAE 492; recebem a mesma regra empenho a empenho.
ONIBUS_FORA_DO_CNAE = ["01778444", "62152657", "53962296", "45215365"]  # Rápido São Paulo, Princesa Tecelã, TBB, Cidade Natureza

# Ordem importa: cada empenho recebe o primeiro motivo que se aplica, e o funil segue esta ordem.
REGRAS = [
    ("sem_empenho_no_ano", "sem linha 'Empenhado' no ano (restos a pagar, só liquidação/pagamento)", "n_linhas_empenho = 0"),
    ("orgao_nao_prefeitura", "órgão não é a prefeitura (Câmara, autarquia, fundo, fundação)", "NOT orgao_prefeitura"),
    ("municipio_sem_ibge", "nome do município não casou com o IBGE", "codigo_ibge IS NULL"),
    ("nao_cnpj", "fornecedor não é pessoa jurídica (pessoa física, identificação especial)", "coalesce(tipo_identificador, '') NOT LIKE 'CNPJ%'"),
    ("cnpj_invalido", "CNPJ com dígito verificador inválido", "NOT coalesce(cnpj_valido, false)"),
    ("elemento_fora", "elemento fora de custeio (3.3) e investimento (4.4): pessoal, dívida, inversões", "coalesce(categoria_grupo, '') NOT IN ('33', '44')"),
    ("nao_aplicacao_direta", "modalidade de aplicação diferente de 90: subvenções, consórcios, intraorçamentário", "coalesce(modalidade_aplicacao, '') <> '90'"),
    ("ente_publico", "natureza jurídica pública (1xxx), empresa pública (2011) ou economia mista (2038)", "natureza_juridica LIKE '1%' OR natureza_juridica IN ('2011', '2038')"),
    ("concessionaria_ou_banco", "CNAE principal de energia, gás, água, esgoto, telefonia fixa ou móvel, ou banco", "regexp_matches(coalesce(cnae_principal, ''), '^(35|36|37|611|612|642)')"),
    ("emissora_de_vale", "emissora de vale-alimentação, refeição ou transporte, ou vale repassado por empresa de ônibus ou sindicato: benefício dos servidores",
     "cnae_principal = '8299702' OR ((cnae_principal LIKE '492%' OR cnae_principal = '9420100' OR left(cnpj, 8) IN ("
     + ", ".join(f"'{b}'" for b in ONIBUS_FORA_DO_CNAE) + ")) AND menciona_vale) OR left(cnpj, 8) IN ("
     + ", ".join(f"'{b}'" for b in VALES_FORA_DO_CNAE) + ")"),
    ("valor_nao_positivo", "valor líquido empenhado menor ou igual a zero", "v_liquido <= 0"),
]


def cnpj_valido(cnpj: str) -> bool:
    if len(cnpj) != 14 or not cnpj.isdigit() or len(set(cnpj)) == 1:
        return False
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for n in (12, 13):
        soma = sum(int(d) * p for d, p in zip(cnpj[:n], pesos[-n:] if n == 12 else [6] + pesos))
        dv = 11 - soma % 11
        if int(cnpj[n]) != (0 if dv >= 10 else dv):
            return False
    return True


assert cnpj_valido("34028316136609") and cnpj_valido("05615940000109"), "CNPJs reais conhecidos devem passar"
assert not cnpj_valido("34028316136608") and not cnpj_valido("11111111111111"), "CNPJs adulterados devem falhar"

# O arquivo é latin-1, mas alguns registros trazem trechos em UTF-8 e bytes do cp1252 (0x80-0x9F),
# que o decodificador latin-1 do DuckDB recusa. Cada trecho é decodificado pelo que realmente é.
UTF8 = re.compile(rb"[\xc2-\xdf][\x80-\xbf]|[\xe0-\xef][\x80-\xbf]{2}")
C1 = re.compile(rb"[\x80-\x9f]")
TABELA_C1 = str.maketrans({chr(b): bytes([b]).decode("cp1252", errors="replace").replace("\ufffd", "?") for b in range(0x80, 0xA0)})


def transcodificar():
    reparos = Counter()
    with subprocess.Popen(["unzip", "-p", str(ZIP)], stdout=subprocess.PIPE) as proc, \
            gzip.open(CSV_UTF8, "wt", encoding="utf-8", compresslevel=1, newline="") as saida:
        while bloco := proc.stdout.read(1 << 26):
            bloco += proc.stdout.readline()
            reparos["linhas_fisicas"] += bloco.count(b"\n")
            pedacos, fim = [], 0
            for m in UTF8.finditer(bloco):
                try:
                    trecho = m.group().decode("utf-8")
                except UnicodeDecodeError:
                    continue
                reparos["utf8_c1" if m.group()[1] < 0xA0 else "utf8_alto"] += 1
                pedacos += [bloco[fim:m.start()].decode("latin-1"), trecho]
                fim = m.end()
            pedacos.append(bloco[fim:].decode("latin-1"))
            texto = "".join(pedacos)
            if C1.search(bloco):
                reparos["cp1252"] += sum(texto.count(chr(b)) for b in range(0x80, 0xA0))
            saida.write(texto.translate(TABELA_C1))
    if proc.returncode:
        raise RuntimeError("unzip falhou")
    return reparos


(LIMPOS / "tmp").mkdir(parents=True, exist_ok=True)
TRABALHO = LIMPOS / "tmp" / f"trabalho_{ANO}.duckdb"
TRABALHO.unlink(missing_ok=True)
con = duckdb.connect(str(TRABALHO))
con.execute(f"SET memory_limit='1500MB'; SET temp_directory='{LIMPOS / 'tmp'}'; SET preserve_insertion_order=false")
con.execute("CREATE MACRO norm(s) AS trim(regexp_replace(upper(strip_accents(s)), '[^A-Z0-9]+', ' ', 'g'))")
con.execute("CREATE MACRO valor(s) AS try_cast(replace(replace(s, '.', ''), ',', '.') AS DECIMAL(18, 2))")

relatorio = [f"# Validação e limpeza das despesas do TCESP, {ANO}\n"]


def secao(titulo, texto=""):
    relatorio.append(f"\n## {titulo}\n\n{texto}")


def tabela(sql, params=None):
    res = con.execute(sql, params or [])
    cols = [d[0] for d in res.description]
    linhas = res.fetchall()
    fmt = lambda v: f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if isinstance(v, float) else (f"{v:,}".replace(",", ".") if isinstance(v, int) else str(v))
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(fmt(v) for v in linha) + " |" for linha in linhas]
    relatorio.append("\n".join(out) + "\n")
    return linhas


def escalar(sql):
    return con.execute(sql).fetchone()[0]


def br(n):
    return f"{n:,}".replace(",", ".")


def carregar(nome, colunas, linhas):
    con.execute(f"CREATE TABLE {nome} ({', '.join(f'{c} {t}' for c, t in colunas)})")
    if not linhas:
        return
    caminho = LIMPOS / "tmp" / f"{nome}.csv"
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(linhas)
    tipos = ", ".join(f"'{c}': '{t}'" for c, t in colunas)
    con.execute(f"INSERT INTO {nome} SELECT * FROM read_csv('{caminho}', header=false, delim=',', quote='\"', escape='\"', columns={{{tipos}}})")


def montar_final():
    """Passos 1 a 5: do zip (ou do Parquet bruto) até a tabela final de empenhos, sem o motivo de exclusão."""
    # 1. CSV -> Parquet bruto, guardando as linhas que o parser rejeita.
    if not BRUTO.exists():
        REPAROS.write_text(json.dumps(transcodificar()))
        con.execute(f"""
            COPY (SELECT * FROM read_csv('{CSV_UTF8}', delim=';', quote='"', escape='"', header=true,
                                         all_varchar=true, store_rejects=true, rejects_table='rej', rejects_scan='rej_scan'))
            TO '{BRUTO}' (FORMAT parquet, COMPRESSION zstd)""")
        con.execute(f"COPY (SELECT * FROM rej) TO '{REJEITADAS}' (FORMAT parquet)")
        CSV_UTF8.unlink()
    reparos = json.loads(REPAROS.read_text())
    linhas_fisicas = reparos["linhas_fisicas"]
    # O layout novo separa tipo e número do identificador e põe espaço antes do número do empenho;
    # a view devolve as colunas no formato do layout antigo para o resto do script valer para os dois.
    colunas_brutas = {r[0] for r in con.execute(f"DESCRIBE SELECT * FROM '{BRUTO}'").fetchall()}
    LAYOUT_NOVO = "tp_identificador_despesa" in colunas_brutas
    if LAYOUT_NOVO:
        con.execute(f"""CREATE VIEW bruto AS SELECT * EXCLUDE (nr_empenho, tp_identificador_despesa, nr_identificador_despesa),
            trim(nr_empenho) AS nr_empenho, tp_identificador_despesa || ' - ' || nr_identificador_despesa AS identificador_despesa
            FROM '{BRUTO}'""")
    else:
        con.execute(f"CREATE VIEW bruto AS SELECT * FROM '{BRUTO}'")
    con.execute(f"CREATE VIEW rejeitadas AS SELECT * FROM '{REJEITADAS}'")

    n_linhas = escalar("SELECT count(*) FROM bruto")
    n_rej = escalar("SELECT count(*) FROM rejeitadas")
    secao("Integridade do arquivo", f"""Linhas físicas no CSV contadas com wc -l, cabeçalho incluído: {br(linhas_fisicas)}.
    Registros lidos: {br(n_linhas)}.
    Registros rejeitados pelo parser: {br(n_rej)}.
    Linhas físicas que sobram, isto é, quebras de linha dentro de campos: {br(linhas_fisicas - n_linhas - n_rej - 1)}.
    """)
    if n_rej:
        tabela("SELECT error_type, count(*) AS n, min(left(csv_line, 160)) AS exemplo FROM rejeitadas GROUP BY 1 ORDER BY 2 DESC, 1")

    secao("Valores, datas e ano")
    tabela(f"""SELECT
        count(*) FILTER (ano_exercicio <> '{ANO}') AS ano_diferente,
        count(*) FILTER (try_cast(mes_referencia AS INT) NOT BETWEEN 1 AND 12 OR mes_referencia IS NULL) AS mes_invalido,
        count(*) FILTER (valor(vl_despesa) IS NULL) AS valor_ilegivel,
        count(*) FILTER (vl_despesa LIKE '%.%') AS valor_com_ponto,
        count(*) FILTER (valor(vl_despesa) < 0) AS valor_negativo,
        count(*) FILTER (try_strptime(dt_emissao_despesa, '%d/%m/%Y') IS NULL) AS data_ilegivel
        FROM bruto""")

    secao("Campos vazios")
    colunas = [r[0] for r in con.execute("DESCRIBE bruto").fetchall()]
    tabela("SELECT " + ", ".join(f"count(*) FILTER (trim(coalesce({c}, '')) = '') AS {c}" for c in colunas) + " FROM bruto")

    secao("Codificação", f"""O arquivo é latin-1. Na leitura, {br(reparos.get('utf8_c1', 0) + reparos.get('utf8_alto', 0))} trechos em UTF-8 foram decodificados como UTF-8
    ({br(reparos.get('utf8_c1', 0))} com segundo byte entre 0x80 e 0x9F, {br(reparos.get('utf8_alto', 0))} entre 0xA0 e 0xBF) e {br(reparos.get('cp1252', 0))} bytes soltos entre 0x80 e 0x9F foram lidos como cp1252.
    Depois do reparo, sobra de duplo encoding ('Ã' seguido de caractere acentuado) e de caracteres de controle C1:
    """)
    tabela("""SELECT
        count(*) FILTER (regexp_matches(ds_despesa || ds_orgao || ds_municipio, 'Ã[\x80-\xbf§£©¡³ºª‡‰]')) AS duplo_encoding,
        count(*) FILTER (regexp_matches(ds_despesa || ds_orgao || coalesce(historico_despesa, ''), '[\x80-\x9f]')) AS controle_c1,
        count(*) FILTER (regexp_matches(ds_despesa || ds_orgao || ds_municipio || coalesce(historico_despesa, ''), '[\\x{0100}-\\x{1FFF}]')) AS fora_do_latin1
        FROM bruto""")
    relatorio.append("Um reparo errado de UTF-8 sobre latin-1 legítimo geraria caracteres fora do latin-1 (U+0100 a U+1FFF). Exemplos, se houver:\n")
    tabela("""SELECT left(regexp_extract(ds_despesa || ' | ' || coalesce(historico_despesa, ''), '.{0,30}[\\x{0100}-\\x{1FFF}].{0,30}'), 70) AS trecho, count(*) AS linhas
        FROM bruto WHERE regexp_matches(ds_despesa || coalesce(historico_despesa, ''), '[\\x{0100}-\\x{1FFF}]') GROUP BY 1 ORDER BY 2 DESC, 1 LIMIT 8""")

    secao("Tipos de linha", "Cada empenho aparece em várias linhas, uma por etapa. Só a linha 'Empenhado' representa a escolha do fornecedor.\n")
    tabela("SELECT tp_despesa, count(*) AS linhas, sum(valor(vl_despesa))::DOUBLE AS valor FROM bruto GROUP BY 1 ORDER BY 2 DESC, 1")

    # 2. Um registro por empenho e fornecedor. Alguns municípios reusam o número do empenho em compras
    # diferentes, e algumas prefeituras reenviam a mesma linha em outro mês; cópias exatas contam uma vez.
    con.execute(f"""
    CREATE TABLE compromisso AS
    SELECT ds_municipio AS municipio_tcesp, ds_orgao AS orgao, nr_empenho, identificador_despesa AS identificador,
        tp_despesa, dt_emissao_despesa, vl_despesa, ds_elemento AS elemento, count(*) AS copias,
        min(ds_despesa) AS fornecedor, min(ds_modalidade_lic) AS modalidade_licitacao, min(ds_funcao_governo) AS funcao,
        bool_or(regexp_matches(upper(strip_accents(coalesce(historico_despesa, ''))), '{HISTORICO_VALE}')) AS menciona_vale
    FROM bruto WHERE tp_despesa IN ('Empenhado', 'Reforço', 'Anulação') GROUP BY ALL""")
    con.execute("""
    CREATE TABLE execucao AS
    SELECT ds_municipio AS municipio_tcesp, ds_orgao AS orgao, nr_empenho, identificador_despesa AS identificador,
        coalesce(sum(valor(vl_despesa)) FILTER (tp_despesa = 'Valor Liquidado'), 0) AS v_liquidado,
        coalesce(sum(valor(vl_despesa)) FILTER (tp_despesa = 'Valor Pago'), 0) AS v_pago
    FROM bruto WHERE tp_despesa IN ('Valor Liquidado', 'Valor Pago') GROUP BY ALL""")
    con.execute(f"""
    CREATE TABLE empenho AS
    WITH c AS (
        SELECT municipio_tcesp, orgao, nr_empenho, identificador,
            count(*) FILTER (tp_despesa = 'Empenhado') AS n_linhas_empenho,
            sum(copias - 1) AS linhas_duplicadas,
            coalesce(sum(valor(vl_despesa)) FILTER (tp_despesa = 'Empenhado'), 0) AS v_empenhado,
            coalesce(sum(valor(vl_despesa)) FILTER (tp_despesa = 'Reforço'), 0) AS v_reforco,
            coalesce(sum(valor(vl_despesa)) FILTER (tp_despesa = 'Anulação'), 0) AS v_anulado,
            min(elemento) <> max(elemento) AS elemento_muda, bool_or(menciona_vale) AS menciona_vale,
            coalesce(arg_max(fornecedor, row(valor(vl_despesa), fornecedor)) FILTER (tp_despesa = 'Empenhado'), min(fornecedor)) AS fornecedor,
            coalesce(arg_max(elemento, row(valor(vl_despesa), elemento)) FILTER (tp_despesa = 'Empenhado'), min(elemento)) AS elemento,
            coalesce(arg_max(modalidade_licitacao, row(valor(vl_despesa), modalidade_licitacao)) FILTER (tp_despesa = 'Empenhado'), min(modalidade_licitacao)) AS modalidade_licitacao,
            coalesce(arg_max(funcao, row(valor(vl_despesa), funcao)) FILTER (tp_despesa = 'Empenhado'), min(funcao)) AS funcao,
            CAST(min(try_strptime(dt_emissao_despesa, '%d/%m/%Y')) FILTER (tp_despesa = 'Empenhado') AS DATE) AS data_empenho
        FROM compromisso GROUP BY ALL)
    SELECT municipio_tcesp, orgao, nr_empenho, identificador,
        try_cast(regexp_extract(nr_empenho, '-(\\d{{4}})\\s*$', 1) AS INT) AS ano_empenho,
        coalesce(c.n_linhas_empenho, 0) AS n_linhas_empenho, coalesce(c.linhas_duplicadas, 0) AS linhas_duplicadas,
        coalesce(c.v_empenhado, 0) AS v_empenhado, coalesce(c.v_reforco, 0) AS v_reforco, coalesce(c.v_anulado, 0) AS v_anulado,
        coalesce(x.v_liquidado, 0) AS v_liquidado, coalesce(x.v_pago, 0) AS v_pago,
        coalesce(c.elemento_muda, false) AS elemento_muda, coalesce(c.menciona_vale, false) AS menciona_vale, c.fornecedor, c.elemento, c.modalidade_licitacao, c.funcao, c.data_empenho
    FROM c FULL JOIN execucao x USING (municipio_tcesp, orgao, nr_empenho, identificador)""")
    con.execute("""CREATE TABLE duplicadas_municipio AS
    SELECT municipio_tcesp, sum(copias - 1) AS linhas_duplicadas, sum(valor(vl_despesa) * (copias - 1)) FILTER (tp_despesa = 'Empenhado')::DOUBLE AS valor_empenhado_duplicado
    FROM compromisso WHERE copias > 1 GROUP BY 1""")
    n_compartilhados = escalar("SELECT count(*) FROM (SELECT 1 FROM empenho WHERE n_linhas_empenho > 0 GROUP BY municipio_tcesp, orgao, nr_empenho HAVING count(*) > 1)")
    con.execute("DROP TABLE compromisso; DROP TABLE execucao")
    con.execute("""ALTER TABLE empenho ADD COLUMN tipo_identificador VARCHAR;
    ALTER TABLE empenho ADD COLUMN cnpj VARCHAR;
    UPDATE empenho SET
        tipo_identificador = trim(regexp_extract(identificador, '^(.*) - [^-]*$', 1)),
        cnpj = CASE WHEN identificador LIKE 'CNPJ%' THEN lpad(regexp_replace(regexp_extract(identificador, '- *([0-9./ -]+)$', 1), '[^0-9]', '', 'g'), 14, '0') END""")

    secao("Empenhos", f"""Chave: município, órgão, número do empenho e fornecedor. O fornecedor entra na chave porque
    {br(n_compartilhados)} números de empenho aparecem com fornecedores diferentes no mesmo órgão (numeração reaproveitada).
    Linhas de empenho, reforço e anulação idênticas em tudo menos o mês de referência contam uma vez.\n""")
    tabela(f"""SELECT count(*) AS empenhos,
        sum(linhas_duplicadas) AS linhas_duplicadas_removidas,
        count(*) FILTER (n_linhas_empenho > 1) AS chave_com_mais_de_um_empenhado,
        count(*) FILTER (n_linhas_empenho = 0) AS sem_linha_empenhado,
        count(*) FILTER (ano_empenho <> {ANO}) AS numero_de_outro_ano,
        count(*) FILTER (ano_empenho IS NULL) AS numero_sem_ano,
        count(*) FILTER (elemento_muda) AS elemento_muda_dentro_do_empenho,
        count(*) FILTER (n_linhas_empenho > 0 AND v_liquidado > v_empenhado + v_reforco - v_anulado + 0.01) AS liquidado_maior_que_empenhado
        FROM empenho""")
    relatorio.append("Liquidações e pagamentos não passam pela remoção de cópias, então municípios que reenviaram tudo aparecem com liquidado maior que empenhado. Por município:\n")
    tabela(f"""SELECT municipio_tcesp, count(*) AS liquidado_maior_que_empenhado FROM empenho
        WHERE n_linhas_empenho > 0 AND v_liquidado > v_empenhado + v_reforco - v_anulado + 0.01 GROUP BY 1 ORDER BY 2 DESC, 1 LIMIT 5""")
    secao("Linhas duplicadas por município (as 8 maiores)")
    tabela("SELECT * FROM duplicadas_municipio ORDER BY linhas_duplicadas DESC, 1 LIMIT 8")
    secao("Empenhos sem linha 'Empenhado', pelo ano do número do empenho")
    tabela("SELECT ano_empenho, count(*) AS empenhos, sum(v_pago)::DOUBLE AS pago FROM empenho WHERE n_linhas_empenho = 0 GROUP BY 1 ORDER BY 2 DESC, 1 LIMIT 8")

    # 3. Municípios: nome do TCESP contra a lista oficial do IBGE.
    ibge = [(str(m["id"]), m["nome"]) for m in json.loads(IBGE.read_text())]
    carregar("ibge", [("codigo_ibge", "VARCHAR"), ("nome_ibge", "VARCHAR")], ibge)
    carregar("apelido", [("tcesp", "VARCHAR"), ("ibge", "VARCHAR")], list(APELIDOS.items()))
    con.execute("""CREATE TABLE municipio AS
    SELECT m.municipio_tcesp, i.codigo_ibge, i.nome_ibge
    FROM (SELECT DISTINCT municipio_tcesp FROM empenho) m
    LEFT JOIN apelido a ON norm(a.tcesp) = norm(m.municipio_tcesp)
    LEFT JOIN ibge i ON norm(i.nome_ibge) = norm(coalesce(a.ibge, m.municipio_tcesp))""")
    secao("Municípios", f"Nomes distintos no TCESP: {escalar('SELECT count(*) FROM municipio')}. "
          f"Casados com o IBGE: {escalar('SELECT count(*) FROM municipio WHERE codigo_ibge IS NOT NULL')} de 645 "
          f"(a capital não é fiscalizada pelo TCESP).\n\nNão casados:\n")
    tabela("SELECT municipio_tcesp FROM municipio WHERE codigo_ibge IS NULL ORDER BY 1")
    if LAYOUT_NOVO:
        relatorio.append("O arquivo traz o código IBGE. Nomes cujo código casado pelo nome difere do código do arquivo:\n")
        tabela("""SELECT DISTINCT b.ds_municipio, b.codigo_municipio_ibge AS codigo_arquivo, m.codigo_ibge AS codigo_pelo_nome
            FROM bruto b JOIN municipio m ON m.municipio_tcesp = b.ds_municipio
            WHERE m.codigo_ibge IS DISTINCT FROM b.codigo_municipio_ibge ORDER BY 1""")
    secao("Municípios do IBGE ausentes no TCESP")
    tabela("SELECT codigo_ibge, nome_ibge FROM ibge WHERE codigo_ibge NOT IN (SELECT codigo_ibge FROM municipio WHERE codigo_ibge IS NOT NULL) ORDER BY 2")

    # 4. Órgãos: precisa haver exatamente uma prefeitura por município.
    con.execute("CREATE TABLE orgao AS SELECT DISTINCT municipio_tcesp, orgao, norm(orgao) LIKE '%PREFEITURA%' AS orgao_prefeitura FROM empenho")
    secao("Órgãos", f"Órgãos distintos: {escalar('SELECT count(*) FROM orgao')}. "
          f"Municípios com uma prefeitura: {escalar('SELECT count(*) FROM (SELECT municipio_tcesp FROM orgao GROUP BY 1 HAVING count(*) FILTER (orgao_prefeitura) = 1)')}.\n\n"
          "Municípios com zero ou mais de uma prefeitura:\n")
    tabela("SELECT municipio_tcesp, list(orgao ORDER BY orgao) FILTER (orgao_prefeitura) AS prefeituras FROM orgao GROUP BY 1 HAVING count(*) FILTER (orgao_prefeitura) <> 1 ORDER BY 1")
    secao("Órgãos que não são prefeitura, pela primeira palavra")
    tabela("SELECT split_part(norm(orgao), ' ', 1) AS primeira_palavra, count(*) AS orgaos, min(orgao) AS exemplo FROM orgao WHERE NOT orgao_prefeitura GROUP BY 1 ORDER BY 2 DESC, 1 LIMIT 12")

    # 5. CNPJ: dígito verificador e natureza jurídica na Receita.
    cnpjs = [r[0] for r in con.execute("SELECT DISTINCT cnpj FROM empenho WHERE cnpj IS NOT NULL").fetchall()]
    carregar("cnpj_check", [("cnpj", "VARCHAR"), ("cnpj_valido", "BOOLEAN")], [(c, cnpj_valido(c)) for c in cnpjs])
    secao("Identificador do fornecedor")
    tabela("SELECT tipo_identificador, count(*) AS empenhos FROM empenho GROUP BY 1 ORDER BY 2 DESC, 1")
    tabela("""SELECT count(*) AS cnpjs_distintos, count(*) FILTER (cnpj_valido) AS validos, count(*) FILTER (NOT cnpj_valido) AS invalidos,
        min(cnpj) FILTER (NOT cnpj_valido) AS exemplo_invalido FROM cnpj_check""")
    tabela("""SELECT length(regexp_replace(regexp_extract(identificador, '- *([0-9./ -]+)$', 1), '[^0-9]', '', 'g')) AS digitos_no_arquivo, count(*) AS empenhos
        FROM empenho WHERE identificador LIKE 'CNPJ%' GROUP BY 1 ORDER BY 2 DESC, 1""")

    # Receita (extrato de extrair_receita.py, Brasil todo). Natureza jurídica vem da empresa (raiz do CNPJ); CNAE e
    # situação vêm do estabelecimento, porque filial e matriz podem ter atividades diferentes.
    con.execute(f"""CREATE TABLE natureza AS SELECT e.*, d.descricao AS natureza_descricao
        FROM '{LIMPOS / "receita_empresas.parquet"}' e LEFT JOIN '{LIMPOS / "receita_naturezas.parquet"}' d ON d.codigo = e.natureza_juridica
        WHERE e.cnpj_basico IN (SELECT left(cnpj, 8) FROM cnpj_check WHERE cnpj_valido)""")
    con.execute(f"""CREATE TABLE cnae AS SELECT e.*, d.descricao AS cnae_descricao
        FROM '{LIMPOS / "receita_estabelecimentos.parquet"}' e LEFT JOIN '{LIMPOS / "receita_cnaes.parquet"}' d ON d.codigo = e.cnae_principal
        WHERE e.cnpj IN (SELECT cnpj FROM cnpj_check WHERE cnpj_valido)""")
    secao(f"Cobertura da Receita (snapshot 2026-10) para CNPJs válidos de {ANO}",
          "Se empresas fechadas não estivessem na base, a cobertura seria bem menor que 100%.\n")
    tabela("""SELECT count(*) AS cnpj_basicos, count(n.cnpj_basico) AS achados_na_receita
        FROM (SELECT DISTINCT left(cnpj, 8) AS b FROM cnpj_check WHERE cnpj_valido) c LEFT JOIN natureza n ON n.cnpj_basico = c.b""")
    secao("Cobertura do CNAE (estabelecimentos, snapshot 2026-10)")
    tabela("""SELECT count(*) AS cnpjs_validos, count(e.cnpj) AS achados, count(*) FILTER (e.situacao_cadastral = '08') AS baixados_hoje
        FROM cnpj_check c LEFT JOIN cnae e USING (cnpj) WHERE c.cnpj_valido""")

    # 6. Funil: cada empenho recebe o primeiro motivo de exclusão, ou fica.
    con.execute(f"""CREATE TABLE final AS
    SELECT e.*, m.codigo_ibge, m.nome_ibge, o.orgao_prefeitura, c.cnpj_valido,
        left(regexp_extract(e.elemento, '^(\\d+)', 1), 2) AS categoria_grupo,
        substr(regexp_extract(e.elemento, '^(\\d+)', 1), 3, 2) AS modalidade_aplicacao,
        n.natureza_juridica, n.natureza_descricao, n.porte, k.cnae_principal, k.cnae_descricao, k.situacao_cadastral, k.data_inicio_atividade,
        e.v_empenhado + e.v_reforco - e.v_anulado AS v_liquido
    FROM empenho e
    JOIN municipio m USING (municipio_tcesp)
    JOIN orgao o USING (municipio_tcesp, orgao)
    LEFT JOIN cnpj_check c USING (cnpj)
    LEFT JOIN natureza n ON n.cnpj_basico = left(e.cnpj, 8)
    LEFT JOIN cnae k ON k.cnpj = e.cnpj""")


# Sem o zip e sem o Parquet bruto, reaplica as REGRAS ao extrato já feito e refaz só o relatório do funil em diante.
if ZIP.exists() or BRUTO.exists():
    montar_final()
elif EMPENHOS.exists():
    anterior = RELATORIO.read_text()
    relatorio[:] = [anterior[:anterior.index("\n## Funil de limpeza")]]
    con.execute(f"CREATE TABLE final AS SELECT * EXCLUDE (motivo_exclusao) FROM '{EMPENHOS}'")
    con.execute("ALTER TABLE final ADD COLUMN IF NOT EXISTS menciona_vale BOOLEAN")
else:
    sys.exit(f"faltam {ZIP} e {EMPENHOS}")
casos = " ".join(f"WHEN {cond} THEN '{nome}'" for nome, _, cond in REGRAS)
con.execute(f"ALTER TABLE final ADD COLUMN motivo_exclusao VARCHAR; UPDATE final SET motivo_exclusao = CASE {casos} END")
con.execute(f"COPY final TO '{EMPENHOS}' (FORMAT parquet, COMPRESSION zstd)")

con.execute("CREATE TABLE regra (ordem INT, motivo VARCHAR, descricao VARCHAR)")
con.executemany("INSERT INTO regra VALUES (?, ?, ?)", [(i, n, d) for i, (n, d, _) in enumerate(REGRAS, 1)])
secao("Funil de limpeza", "Cada linha remove os empenhos que sobraram da linha anterior e caem na regra.\n")
tabela("""SELECT coalesce(r.ordem, 99) AS ordem, coalesce(f.motivo_exclusao, 'MANTIDO') AS motivo, min(r.descricao) AS descricao,
    count(*) AS empenhos, sum(f.v_liquido)::DOUBLE AS valor_liquido, count(DISTINCT f.cnpj) AS cnpjs
    FROM final f LEFT JOIN regra r ON r.motivo = f.motivo_exclusao GROUP BY 1, 2 ORDER BY 1""")
tabela("SELECT count(DISTINCT codigo_ibge) AS municipios_na_rede FROM final WHERE motivo_exclusao IS NULL")

# 7. Rede bipartida prefeitura-fornecedor.
con.execute(f"""COPY (SELECT codigo_ibge, nome_ibge AS municipio, cnpj, min(fornecedor) AS fornecedor, min(natureza_juridica) AS natureza_juridica,
    min(cnae_principal) AS cnae_principal, count(*) AS empenhos, sum(v_liquido) AS valor FROM final WHERE motivo_exclusao IS NULL GROUP BY ALL)
    TO '{REDE}' (FORMAT parquet)""")
n_arestas = escalar(f"SELECT count(*) FROM '{REDE}'")
secao("Rede prefeitura-fornecedor", f"Arestas município-CNPJ: {br(n_arestas)}.\n")
tabela(f"SELECT count(DISTINCT cnpj) AS fornecedores, median(n) AS mediana_municipios_por_fornecedor, max(n) AS max_municipios FROM (SELECT cnpj, count(*) AS n FROM '{REDE}' GROUP BY 1)")
secao("Modalidade de licitação dos empenhos mantidos")
tabela("SELECT modalidade_licitacao, count(*) AS empenhos, sum(v_liquido)::DOUBLE AS valor FROM final WHERE motivo_exclusao IS NULL GROUP BY 1 ORDER BY 3 DESC, 1")
secao("Removidos pela regra de CNAE (os 15 maiores)")
tabela("""SELECT cnpj, min(fornecedor) AS fornecedor, min(cnae_descricao) AS cnae, count(DISTINCT codigo_ibge) AS municipios,
    sum(v_liquido)::DOUBLE AS valor FROM final WHERE motivo_exclusao = 'concessionaria_ou_banco' GROUP BY 1 ORDER BY 5 DESC, 1 LIMIT 15""")
secao("Fornecedores mantidos que parecem emissoras de vale",
      "Raízes de CNPJ mantidas com ao menos 5 empenhos e metade ou mais deles com histórico de vale. "
      "Confira o histórico e, se for emissora, inclua em VALES_FORA_DO_CNAE.\n")
tabela("""SELECT left(cnpj, 8) AS raiz, min(fornecedor) AS fornecedor, min(cnae_descricao) AS cnae, count(*) FILTER (menciona_vale) AS empenhos_vale,
    count(*) AS empenhos, sum(v_liquido)::DOUBLE AS valor FROM final WHERE motivo_exclusao IS NULL GROUP BY 1
    HAVING count(*) >= 5 AND count(*) FILTER (menciona_vale) >= count(*) / 2 ORDER BY 6 DESC, 1 LIMIT 25""")
secao("Os 30 maiores fornecedores mantidos", "Esta lista é para revisão manual: o que ainda parece não ser escolha discricionária do prefeito.\n")
tabela("""SELECT cnpj, min(fornecedor) AS fornecedor, min(cnae_descricao) AS cnae, count(DISTINCT codigo_ibge) AS municipios,
    sum(v_liquido)::DOUBLE AS valor FROM final WHERE motivo_exclusao IS NULL GROUP BY 1 ORDER BY 5 DESC, 1 LIMIT 30""")

RELATORIO.write_text("\n".join(relatorio))
con.close()
TRABALHO.unlink()
print(f"relatório: {RELATORIO}\nempenhos: {EMPENHOS}\nrede: {REDE}")
