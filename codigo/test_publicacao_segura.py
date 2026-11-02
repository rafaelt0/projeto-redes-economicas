"""O repositório é público: nada de CPF ou título eleitoral, e nenhum link para arquivo que ficou de fora."""
from pathlib import Path
import re
import unittest

RAIZ = Path(__file__).resolve().parent.parent
FORA = {'.git', 'dados', '.venv', '__pycache__'}
TEXTO = {'.md', '.csv', '.json', '.html', '.py', '.sh', '.yml', '.toml', '.txt', '.svg'}
# 11 ou 12 dígitos isolados (CPF, título eleitoral) ou CPF com pontuação.
DOCUMENTO = re.compile(r'(?<![\d.,])\d{11,12}(?![\d.,])|\d{3}\.\d{3}\.\d{3}-\d{2}')
LINK = re.compile(r'\]\(([^)\s]+)\)|(?:href|src)="([^"]+)"')


def arquivos():
    for p in sorted(RAIZ.rglob('*')):
        if p.is_file() and p.suffix in TEXTO and not FORA & set(p.relative_to(RAIZ).parts):
            yield p


def documentos(texto):
    return DOCUMENTO.findall(texto)


def links_quebrados(arquivo, texto):
    quebrados = []
    for m in LINK.finditer(texto):
        alvo = (m.group(1) or m.group(2)).split('#')[0]
        if not alvo or re.match(r'[a-z]+:', alvo) or alvo.startswith(('//', '{', '$')):
            continue
        if not (arquivo.parent / alvo).exists():
            quebrados.append(f'{arquivo.relative_to(RAIZ).as_posix()}: {alvo}')
    return quebrados


class PublicacaoSegura(unittest.TestCase):
    def test_sem_documento_pessoal(self):
        achados = {p.relative_to(RAIZ).as_posix(): documentos(p.read_text(encoding='utf-8'))[:3] for p in arquivos()}
        self.assertEqual({k: v for k, v in achados.items() if v}, {})

    def test_detecta_cpf_no_nome(self):
        self.assertTrue(documentos('| 28342220 | FULANO DE TAL ' + '4' * 11 + ' | Agências |'))
        self.assertFalse(documentos('"ef": -0.023812345678901, "cnpj": "33050196017749"'))

    def test_sem_link_quebrado(self):
        self.assertEqual([q for p in arquivos() for q in links_quebrados(p, p.read_text(encoding='utf-8'))], [])


if __name__ == '__main__':
    unittest.main()
