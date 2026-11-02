import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('reproduzir', Path(__file__).resolve().parent.parent / 'reproduzir.py')
reproduzir = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reproduzir)


class Comparacao(unittest.TestCase):
    def comparar(self, referencia, gerado, nome='t.csv'):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            (Path(a) / nome).write_text(referencia, encoding='utf-8', newline='')
            (Path(b) / nome).write_text(gerado, encoding='utf-8', newline='')
            return reproduzir.comparar(Path(a), Path(b), [nome])

    def test_diferenca_no_12o_digito_passa(self):
        self.assertEqual(self.comparar('m,ef\nM4,-0.0238123456789\n', 'm,ef\nM4,-0.0238123456788\n'), [])

    def test_um_centavo_falha(self):
        self.assertTrue(self.comparar('valor\n1000.00\n', 'valor\n1000.01\n'))

    def test_texto_diferente_falha(self):
        self.assertTrue(self.comparar('{"modelo": "M4"}', '{"modelo": "M5"}', 't.json'))

    def test_sha256_dos_bytes_nao_e_comparado(self):
        self.assertEqual(self.comparar('{"sha256_fonte": "aa", "n": 1}', '{"sha256_fonte": "bb", "n": 1}', 't.json'), [])

    def test_fim_de_linha_nao_importa(self):
        self.assertEqual(self.comparar('a\r\nb\r\n', 'a\nb\n', 't.md'), [])

    def test_arquivo_ausente_falha(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            (Path(a) / 't.md').write_text('x', encoding='utf-8')
            self.assertTrue(reproduzir.comparar(Path(a), Path(b), ['t.md']))


if __name__ == '__main__':
    unittest.main()
