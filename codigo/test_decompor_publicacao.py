"""Casos conhecidos para o estimador e a identidade entre destinos."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np

spec = importlib.util.spec_from_file_location("decompor", Path(__file__).with_name("decompor_publicacao.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class Decomposicao(unittest.TestCase):
    def test_padronizacao_e_destinos_somam_zero(self):
        # Dois estratos: pesos MH 1 e 2. Riscos de continuidade +1 e -0,5.
        n = np.array([[2., 2.], [4., 4.]])
        k = np.array([[[0., 2.], [2., 0.]], [[4., 0.], [2., 2.]]])
        efeito = mod.mantel_haenszel(n, k)
        np.testing.assert_allclose(efeito, [0., 0.], atol=1e-14)
        self.assertAlmostEqual(float(efeito.sum()), 0.)

    def test_estrato_sem_controle_fica_fora(self):
        n = np.array([[2., 2.], [0., 10.]])
        k = np.array([[[0.], [2.]], [[0.], [0.]]])
        np.testing.assert_allclose(mod.mantel_haenszel(n, k), [1.])

    def test_reamostragem_municipal_reproduzivel_e_pareada(self):
        n = np.ones((5, 1, 2)) * 4
        k = np.zeros((5, 1, 2, 2))
        k[:, :, 0, 1] = 4
        k[:, :, 1, 0] = 4
        a = mod.bootstrap(n, k, replicas=37, semente=31)
        b = mod.bootstrap(n, k, replicas=37, semente=31)
        np.testing.assert_equal(a, b)
        np.testing.assert_allclose(a, np.tile([1., -1.], (37, 1)))

    def test_sem_suporte_retorna_nan(self):
        self.assertTrue(np.isnan(mod.mantel_haenszel(np.array([[0., 1.]]), np.array([[[0.], [1.]]]))).all())

    def test_parcelas_condicionais_e_decomposicao(self):
        # Dois estratos, pesos 5 e 10. Continuidade cai de 0,5 para 0,4 no
        # estrato 2 e sobe de 0,5 para 0,6 no estrato 1; a taxa de "segue na
        # rede" fica igual, de modo que nível e composição se cancelam.
        n = np.array([[[10., 10.], [20., 20.]]])
        k = np.array([[
            [[5., 3., 1., 1.], [6., 2., 1., 1.]],
            [[10., 6., 2., 2.], [8., 7., 2., 3.]],
        ]])
        v = mod.condicional_estratos(n, k)
        # Parcelas entre quem não continua, por destino e grupo.
        self.assertAlmostEqual(v[0], .6, places=12)
        self.assertAlmostEqual(v[1], (5*(2/10) + 10*(7/20))/(5*(4/10) + 10*(12/20)), places=12)
        self.assertAlmostEqual(v[2], v[1] - v[0], places=12)
        self.assertAlmostEqual(v[0] + v[3] + v[6], 1., places=12)
        self.assertAlmostEqual(v[1] + v[4] + v[7], 1., places=12)
        # Nível e composição somam a diferença da taxa de "segue na rede".
        self.assertAlmostEqual(v[9] + v[10], 0., places=12)
        self.assertAlmostEqual(v[9], (0.5 - 7/15) * (.6 + .5625)/2, places=12)

    def test_decomposicao_reproduz_diferenca_de_destino(self):
        rng = np.random.default_rng(7)
        n = rng.integers(20, 80, size=(30, 5, 2)).astype(float)
        k = np.zeros((30, 5, 2, 4))
        for m in range(30):
            for s in range(5):
                for g in (0, 1):
                    cont = rng.binomial(int(n[m, s, g]), .4)
                    resto = int(n[m, s, g]) - cont
                    k[m, s, g] = [cont, *rng.multinomial(resto, [.5, .25, .25])]
        total, kt = n.sum(0), k.sum(0)
        efeito = mod.mantel_haenszel(total, kt)[1]
        v = mod.condicional_estratos(n, k)
        self.assertAlmostEqual(v[9] + v[10], efeito, places=12)

    def test_decomposicao_nao_exclui_estrato_por_desfecho(self):
        # No primeiro estrato o grupo 0 só tem continuadores. Ainda assim,
        # esse estrato pertence ao suporte MH e deve entrar na identidade.
        n = np.array([[10., 10.], [20., 20.]])
        k = np.array([
            [[10., 0., 0., 0.], [5., 3., 1., 1.]],
            [[10., 6., 2., 2.], [8., 7., 2., 3.]],
        ])
        v = mod.condicional_estratos(n, k)
        efeitos = mod.mantel_haenszel(n, k)
        np.testing.assert_allclose(v[9::2] + v[10::2], efeitos[1:], atol=1e-14)
        self.assertAlmostEqual(v[9::2].sum(), -efeitos[0], places=12)
        self.assertAlmostEqual(v[10::2].sum(), 0., places=12)

    def test_bootstrap_condicional_reproduzivel(self):
        n = np.ones((5, 1, 2)) * 4
        k = np.zeros((5, 1, 2, 4))
        k[:, :, 0, 0] = 2
        k[:, :, 0, 1] = 2
        k[:, :, 1, 0] = 1
        k[:, :, 1, 1] = 3
        a = mod.bootstrap_condicional(n, k, replicas=11, semente=31)
        b = mod.bootstrap_condicional(n, k, replicas=11, semente=31)
        np.testing.assert_equal(a, b)
        np.testing.assert_allclose(a[:, 2], 0.0)


if __name__ == "__main__":
    unittest.main()
