import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('preparar', Path(__file__).with_name('preparar_publicacao.py'))
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class EleicoesSuplementares(unittest.TestCase):
    def test_evento_sem_vencedor_tambem_interrompe_mandato(self):
        linhas = [dict(DS_CARGO='PREFEITO', NM_TIPO_ELEICAO='ELEIÇÃO SUPLEMENTAR',
            NM_UE='PAULÍNIA', DT_ELEICAO='01/09/2019', DS_SIT_TOT_TURNO='#NULO#')]
        eventos = mod.contar_eventos(linhas, 2016, {'PAULINIA': '3536505'})
        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0]['eleitos'], 0)
        self.assertEqual(eventos[0]['codigo_ibge'], '3536505')
        self.assertEqual(mod.transicoes_afetadas(eventos), {('3536505', 2016), ('3536505', 2020)})

    def test_eventos_repetidos_e_outros_cargos_nao_inflam_exclusoes(self):
        base = dict(DS_CARGO='PREFEITO', NM_TIPO_ELEICAO='ELEIÇÃO SUPLEMENTAR',
            NM_UE='EMBU', DT_ELEICAO='01/09/2019', DS_SIT_TOT_TURNO='ELEITO')
        linhas = [base, dict(base, DS_SIT_TOT_TURNO='#NULO#'), dict(base, DS_CARGO='VEREADOR')]
        eventos = mod.contar_eventos(linhas, 2016, {'EMBU': '3500000'})
        self.assertEqual(eventos[0]['candidaturas'], 2)
        self.assertEqual(eventos[0]['eleitos'], 1)
        self.assertEqual(len(mod.transicoes_afetadas(eventos)), 2)

    def test_municipio_nao_mapeado_interrompe(self):
        base = dict(DS_CARGO='PREFEITO', NM_TIPO_ELEICAO='ELEIÇÃO SUPLEMENTAR',
            NM_UE='DESCONHECIDO', DT_ELEICAO='01/09/2019', DS_SIT_TOT_TURNO='ELEITO')
        with self.assertRaisesRegex(ValueError, 'Município'):
            mod.contar_eventos([base], 2016, {})


if __name__ == '__main__':
    unittest.main()
