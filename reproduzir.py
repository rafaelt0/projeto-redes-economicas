# /// script
# requires-python = "==3.14.*"
# dependencies = [
#     "contourpy==1.4.0",
#     "cycler==0.12.1",
#     "duckdb==2.0.0",
#     "fonttools==4.68.0",
#     "kiwisolver==1.5.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.4",
#     "packaging==26.3",
#     "pillow==13.0.0",
#     "pyparsing==3.3.3",
#     "python-dateutil==3.0.0",
#     "scipy==1.18.1",
#     "six==1.17.0",
#     "tzdata==2026.6",
# ]
# ///
"""Reproduz as tabelas, as figuras e o relatório regional a partir dos dados da release.

Uso: uv run reproduzir.py          testes, dados, análise e comparação com as saídas do repositório
     uv run reproduzir.py testes   só os testes, sem dados
"""
import csv
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
URL = 'https://github.com/rafaelt0/projeto-redes-economicas/releases/download/dados-v1/dados-reproducao-v1.zip'
SHA256 = '96c8bc5c3d2b5da2ba2cddfa1df255ec2a97a49a75cd5d72b5de479c43282d8c'
ZIP = RAIZ / 'dados' / 'dados-reproducao-v1.zip'
ETAPAS = ['preparar_publicacao', 'perfil_fornecedores', 'estimar_painel', 'decompor_publicacao', 'diagnosticar_tempo',
    'figuras_publicacao', 'tabelas_publicacao', 'medir_regioes']
# Saídas versionadas que a análise regenera. As figuras ficam de fora: a renderização de fontes muda entre sistemas.
SAIDAS = ['docs/publicacao/tabelas/*.csv', 'docs/publicacao/tabelas/*.json', 'docs/publicacao/*.csv',
    'docs/publicacao/amostra-auditada.json', 'docs/publicacao/manifesto-resultados.json',
    'docs/publicacao/fornecedores.html', 'docs/resultados-decomposicao.md', 'relatorios/relatorio_regioes.md']
TOLERANCIA = 1e-9
# -X utf8: console em UTF-8 também no Windows, onde o padrão para pipes é cp1252 (o -I ignora PYTHONIOENCODING).
PYTHON = [sys.executable, '-I', '-X', 'utf8']


def rodar_testes():
    subprocess.run(PYTHON + ['-m', 'unittest', 'discover', '-s', 'codigo', '-p', 'test_*.py'], cwd=RAIZ, check=True)


def sha256(caminho):
    h = hashlib.sha256()
    with caminho.open('rb') as f:
        for bloco in iter(lambda: f.read(1 << 20), b''):
            h.update(bloco)
    return h.hexdigest()


def obter_dados():
    if not (ZIP.exists() and sha256(ZIP) == SHA256):
        ZIP.parent.mkdir(exist_ok=True)
        parcial = ZIP.with_suffix('.parcial')
        print(f'Baixando {URL} (~300 MB)', flush=True)
        urllib.request.urlretrieve(URL, parcial)
        if sha256(parcial) != SHA256:
            raise SystemExit(f'{parcial}: SHA-256 diferente do esperado; apague o arquivo e rode de novo')
        parcial.replace(ZIP)
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(RAIZ)
    print('Dados conferidos e extraídos em dados/', flush=True)


def arquivos_comparados():
    return sorted({p.relative_to(RAIZ).as_posix() for padrao in SAIDAS for p in RAIZ.glob(padrao)})


def valor(texto):
    try:
        return float(texto)
    except ValueError:
        return texto


def diferenca(a, b, onde=''):
    """None se iguais (números com tolerância relativa, o resto exato); senão, onde diferem."""
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            return f'{onde}: chaves {sorted(a.keys() ^ b.keys())}'
        return next((d for k in a if (d := diferenca(a[k], b[k], f'{onde}/{k}'))), None)
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return f'{onde}: {len(a)} itens no repositório, {len(b)} gerados'
        return next((d for i, (x, y) in enumerate(zip(a, b)) if (d := diferenca(x, y, f'{onde}[{i}]'))), None)
    numeros = all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (a, b))
    if numeros and (math.isclose(a, b, rel_tol=TOLERANCIA, abs_tol=1e-12) or (math.isnan(a) and math.isnan(b))):
        return None
    if not numeros and a == b:
        return None
    return f'{onde}: {a!r} no repositório, {b!r} gerado'


def ler(caminho):
    texto = caminho.read_text(encoding='utf-8')
    if caminho.suffix == '.json':
        return json.loads(texto)
    if caminho.suffix == '.csv':
        return [[valor(c) for c in linha] for linha in csv.reader(texto.splitlines())]
    return texto.splitlines()


def comparar(referencia, gerado, arquivos):
    """Lista os arquivos que diferem entre as duas pastas."""
    diferentes = []
    for nome in arquivos:
        ref, novo = referencia / nome, gerado / nome
        if not novo.exists():
            diferentes.append(f'{nome}: não foi gerado')
        elif d := diferenca(ler(ref), ler(novo)):
            diferentes.append(f'{nome} {d}')
    return diferentes


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    rodar_testes()
    if sys.argv[1:] == ['testes']:
        return
    obter_dados()
    arquivos = arquivos_comparados()
    with tempfile.TemporaryDirectory() as tmp:
        referencia = Path(tmp)
        for nome in arquivos:
            (referencia / nome).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(RAIZ / nome, referencia / nome)
        for etapa in ETAPAS:
            print(f'== {etapa}', flush=True)
            subprocess.run(PYTHON + [f'codigo/{etapa}.py'], cwd=RAIZ, check=True)
        diferentes = comparar(referencia, RAIZ, arquivos)
    if diferentes:
        print('Diferenças em relação às saídas do repositório:', *diferentes, sep='\n  ')
        raise SystemExit(1)
    print(f'resultados iguais aos do repositório ({len(arquivos)} arquivos comparados)')


if __name__ == '__main__':
    main()
