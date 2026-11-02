"""Amostra de resultado conhecido, sem depender dos dados locais.

Uso: .venv/bin/python -I -m unittest discover -s codigo -p 'test_*.py'
"""

import contextlib
import importlib.util
import io
import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import duckdb

SPEC = importlib.util.spec_from_file_location("medir_regioes", Path(__file__).with_name("medir_regioes.py"))
regional = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(regional)


class ComparacaoRegional(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.limpos = self.raiz / "dados/limpos"
        self.limpos.mkdir(parents=True)
        self.ibge = self.raiz / "dados/brutos/ibge/municipios_sp.json"
        self.ibge.parent.mkdir(parents=True)
        self.relatorio = self.raiz / "relatorio.md"
        self.codigos = [f"35{i:05d}" for i in range(1, 645)]
        self.mapa = [{"id": int(c), "regiao-imediata": {"regiao-intermediaria": {
            "id": 3501 if c in self.codigos[:4] else 3502,
            "nome": "Região A" if c in self.codigos[:4] else "Região B", "UF": {"id": 35}}}}
            for c in self.codigos + ["3550308"]]
        self.ibge.write_text(json.dumps(self.mapa), encoding='utf-8', newline='\n')
        self.con = duckdb.connect()
        self.addCleanup(self.con.close)
        self.con.execute("""CREATE TABLE p (codigo_ibge VARCHAR, eleicao INT, raiz VARCHAR,
            mandatos_inteiros BOOLEAN, alternancia BOOLEAN, n_clientes INT,
            atende_partido_novo BOOLEAN, atende_partido_antigo BOOLEAN, faixa_clientes VARCHAR,
            setor VARCHAR, eleicao_transicao INT, destino VARCHAR)""")
        # Duas transições de cada um dos dois municípios ligados a partidos opostos.
        # Novo: +100 pp; antigo: -100 pp; diferença pareada: +200 pp.
        linhas = []
        for t in (2012, 2016):
            linhas += [(self.codigos[0], t-4, "00000001", True, True, 2, True, False, "2", "01", t, "continua"),
                       (self.codigos[1], t-4, "00000002", True, True, 2, False, True, "2", "01", t, "saiu")]
        # Alternância: 2/4 contra 0/1 = +50 pp. A aresta de 1 cliente não tem
        # controle no seu estrato: entra na população, mas não no suporte.
        linhas += [(self.codigos[2], 2008, "00000003", True, False, 2, False, False, "2", "01", 2012, "saiu"),
                   (self.codigos[3], 2008, "00000004", True, True, 1, False, False, "1", "01", 2012, "continua")]
        # Completa a cobertura geográfica antes do filtro de comparabilidade.
        linhas += [(c, 2008, "00000005", False, None, 2, True, False, "2", "01", 2012, "continua")
                   for c in self.codigos[4:]]
        self.con.executemany("INSERT INTO p VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", linhas)
        self.gravar()

    def gravar(self):
        self.con.execute(f"COPY p TO '{self.limpos / 'permanencia.parquet'}'")

    def executar(self):
        with patch.multiple(regional, RAIZ=self.raiz, LIMPOS=self.limpos, RELATORIO=self.relatorio), \
                contextlib.redirect_stdout(io.StringIO()):
            regional.main()
        return self.relatorio.read_text(encoding='utf-8')

    def linhas(self, texto, regiao):
        secao = texto.split(f"## {regiao} — ", 1)[1].split("\n## ", 1)[0]
        tabela = [linha for linha in secao.splitlines() if linha.startswith("|")]
        colunas = [v.strip() for v in tabela[0].strip("|").split("|")]
        return {valores[0]: dict(zip(colunas, valores)) for linha in tabela[2:]
                if (valores := [v.strip() for v in linha.strip("|").split("|")])}

    def test_estimativas_suporte_e_bootstrap_pareado(self):
        texto = self.executar()
        linhas = self.linhas(texto, 3501)
        for contraste, estimativa in [("partido novo", 100), ("partido antigo", -100),
                                      (regional.DIFERENCA, 200)]:
            self.assertEqual(float(linhas[contraste]["diferenca_pp"]), estimativa)
            self.assertEqual(float(linhas[contraste]["ic95_inf_pp"]), estimativa)
            self.assertEqual(float(linhas[contraste]["ic95_sup_pp"]), estimativa)
        rng = random.Random(2026)
        validas = sum(len(set(rng.choices(self.codigos[:2], k=2))) == 2 for _ in range(200))
        for contraste in ("partido novo", "partido antigo", regional.DIFERENCA):
            self.assertEqual(int(linhas[contraste]["replicas_validas"]), validas)
        self.assertEqual(linhas["partido novo"]["n"], "4")
        self.assertEqual(linhas["partido novo"]["n_suporte"], "4")
        self.assertEqual(linhas["alternância"]["n"], "6")
        self.assertEqual(linhas["alternância"]["n_suporte"], "3")
        self.assertEqual(float(linhas["alternância"]["diferenca_pp"]), 50)
        for linha in self.linhas(texto, 3502).values():
            self.assertEqual(linha["diferenca_pp"], "NA")
            self.assertEqual(linha["replicas_validas"], "0")
        self.assertEqual(texto, self.executar())

    def test_falta_de_municipio_inelegivel_interrompe_antes_do_filtro(self):
        self.con.execute("DELETE FROM p WHERE codigo_ibge = ?", [self.codigos[-1]])
        self.gravar()
        with self.assertRaisesRegex(ValueError, "Cobertura"):
            self.executar()
        self.assertFalse(self.relatorio.exists())

    def test_mapa_duplicado_nao_multiplica_arestas(self):
        with self.assertRaisesRegex(ValueError, "duplicado"):
            regional.mapa_regioes(self.mapa + [self.mapa[0]])


if __name__ == "__main__":
    unittest.main()
