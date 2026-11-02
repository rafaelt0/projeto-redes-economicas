"""Sem encoding explícito, o Windows lê e grava em cp1252 e quebra no "−" das tabelas."""
import ast
from pathlib import Path
import unittest

RAIZ = Path(__file__).resolve().parent.parent
FUNCOES = {'open', 'read_text', 'write_text'}


def sem_encoding(arquivo):
    faltas = []
    for no in ast.walk(ast.parse(arquivo.read_text(encoding='utf-8'))):
        if not isinstance(no, ast.Call):
            continue
        nome = no.func.attr if isinstance(no.func, ast.Attribute) else getattr(no.func, 'id', None)
        if nome not in FUNCOES or any(k.arg == 'encoding' for k in no.keywords):
            continue
        modo = next((a.value for a in no.args if isinstance(a, ast.Constant) and isinstance(a.value, str)), '')
        if 'b' not in modo:
            faltas.append(f'{arquivo.relative_to(RAIZ).as_posix()}:{no.lineno}')
    return faltas


class Portabilidade(unittest.TestCase):
    def test_leituras_e_escritas_dizem_o_encoding(self):
        arquivos = sorted((RAIZ / 'codigo').glob('*.py')) + [RAIZ / 'reproduzir.py']
        self.assertEqual([f for a in arquivos for f in sem_encoding(a)], [])


if __name__ == '__main__':
    unittest.main()
