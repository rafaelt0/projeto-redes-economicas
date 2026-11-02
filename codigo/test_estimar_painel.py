import unittest
import numpy as np
from estimar_painel import (NaoIdentificado, absorver, descartar_singletons, estimar, posto_dois_efeitos,
                            validar_fonte, CAMPOS_OBRIGATORIOS)


class TestePainel(unittest.TestCase):
    def test_absorcao_e_covariancia_equivalem_a_dummies(self):
        rng = np.random.default_rng(42)
        a = np.repeat(np.arange(6), 12)
        b = np.tile(np.repeat(np.arange(4), 3), 6)
        x = rng.normal(size=(72, 2))
        y = x @ np.array([0.7, -0.4]) + a * .1 + b * .2 + rng.normal(size=72)
        Z = np.column_stack([x, np.eye(6)[a], np.eye(4)[b, 1:]])
        beta = np.linalg.lstsq(Z, y, rcond=None)[0]
        resid = y - Z @ beta
        bread = np.linalg.inv(Z.T @ Z)
        def meat(labels):
            sums = np.array([(Z[labels == g] * resid[labels == g, None]).sum(axis=0)
                             for g in np.unique(labels)])
            G = len(sums)
            return G / (G - 1) * (len(y) - 1) / (len(y) - Z.shape[1]) * sums.T @ sums
        inter = a * 4 + b
        covariance = bread @ (meat(a) + meat(b) - meat(inter)) @ bread
        out = estimar(y, x, [a, b], a, b, ['x', 'z'])
        np.testing.assert_allclose(out['beta'], beta[:2], atol=1e-9)
        np.testing.assert_allclose(out['cov'], covariance[:2, :2], atol=1e-9)
        self.assertEqual(out['posto_fe_limite'], 9)

    def test_componentes_desconexos(self):
        a = np.array([0, 0, 1, 1, 2, 2, 3, 3])
        b = np.array([0, 1, 0, 1, 2, 3, 2, 3])
        self.assertEqual(posto_dois_efeitos(a, b), 6)
        v = np.arange(8., dtype=float)[:, None]
        residual, it, erro = absorver(v, [a, b])
        self.assertLess(erro, 1e-10)
        for group in [a, b]:
            for label in np.unique(group):
                self.assertAlmostEqual(residual[group == label].mean(), 0., places=10)

    def test_colinearidade_falha(self):
        a = np.repeat(np.arange(3), 5)
        b = np.tile(np.arange(5), 3)
        with self.assertRaisesRegex(ValueError, 'colinear'):
            estimar(np.random.default_rng(3).normal(size=15), np.column_stack([a, b]), [a, b], a, b, ['a', 'b'])

    def test_singletons_equivalem_a_amostra_sem_eles(self):
        rng = np.random.default_rng(7)
        a = np.repeat(np.arange(6), 12)
        b = np.tile(np.repeat(np.arange(4), 3), 6)
        x = rng.normal(size=(72, 1))
        y = x[:, 0] * .5 + a * .1 + rng.normal(size=72)
        # 5 linhas extras, cada uma sozinha num nível novo do efeito b
        a2 = np.concatenate([a, np.arange(5) % 6])
        b2 = np.concatenate([b, 10 + np.arange(5)])
        x2 = np.vstack([x, rng.normal(size=(5, 1))])
        y2 = np.concatenate([y, rng.normal(size=5)])
        self.assertEqual((~descartar_singletons([a2, b2])).sum(), 5)
        cheio = estimar(y2, x2, [a2, b2], a2, b2, ['x'])
        base = estimar(y, x, [a, b], a, b, ['x'])
        np.testing.assert_allclose(cheio['beta'], base['beta'], atol=1e-9)
        np.testing.assert_allclose(cheio['cov'], base['cov'], atol=1e-9)
        self.assertEqual(cheio['n_singletons_descartados'], 5)
        self.assertNotAlmostEqual(cheio['cov_conservadora'][0, 0], base['cov'][0, 0], places=6)

    def test_singletons_em_cascata(self):
        # remover o nível único de b deixa o nível 1 de a com uma só linha
        a = np.array([0, 0, 0, 1, 2, 2])
        b = np.array([0, 1, 1, 2, 0, 1])
        self.assertEqual(list(descartar_singletons([a, b])), [True, True, True, False, True, True])

    def test_desfecho_constante_no_efeito_nao_e_identificado(self):
        a = np.repeat(np.arange(6), 12)
        b = np.tile(np.repeat(np.arange(4), 3), 6)
        x = np.random.default_rng(1).normal(size=(72, 1))
        with self.assertRaises(NaoIdentificado):
            estimar(a * 1., x, [a, b], a, b, ['x'])  # y depende só do efeito a

    def test_validar_fonte_exige_filtro_e_campos_exatos(self):
        colunas = set(CAMPOS_OBRIGATORIOS) | {'continua'}
        validar_fonte({'filtro_identidade_conservador': True}, colunas)
        with self.assertRaisesRegex(ValueError, 'filtro_identidade_conservador'):
            validar_fonte({}, colunas)
        with self.assertRaisesRegex(ValueError, 'filtro_identidade_conservador'):
            validar_fonte({'filtro_identidade_conservador': 'true'}, colunas)
        for ausente in CAMPOS_OBRIGATORIOS:
            with self.assertRaisesRegex(ValueError, ausente):
                validar_fonte({'filtro_identidade_conservador': True}, colunas - {ausente})
        self.assertIn('continua_anos2a4', CAMPOS_OBRIGATORIOS)

    def test_posto_dos_regressores_e_dimensoes_reportados(self):
        rng = np.random.default_rng(5)
        a = np.repeat(np.arange(6), 12)
        b = np.tile(np.repeat(np.arange(4), 3), 6)
        x = rng.normal(size=(72, 2))
        out = estimar(x @ [1., 2.] + rng.normal(size=72), x, [a, b], a, b, ['x1', 'x2'])
        self.assertEqual((out['posto_regressores'], out['n_regressores']), (2, 2))
        self.assertEqual((out['n_municipios'], out['n_fornecedores']), (6, 4))

    def test_categoria_ausente_na_subamostra_e_colinearidade_explicita(self):
        # uma categoria vazia (como numa subamostra sem 2012) deixa o regressor nulo: deve falhar com posto
        a = np.repeat(np.arange(6), 12)
        b = np.tile(np.repeat(np.arange(4), 3), 6)
        x = np.column_stack([np.random.default_rng(2).normal(size=72), np.zeros(72)])
        with self.assertRaisesRegex(ValueError, r'colinear.*posto 1 de 2'):
            estimar(np.random.default_rng(9).normal(size=72), x, [a, b], a, b, ['x', 'vazia'])


if __name__ == '__main__':
    unittest.main()
