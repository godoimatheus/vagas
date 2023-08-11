from django.test import TestCase
from ..models import Vagas

# pylint: disable=E1101


class VagasTest(TestCase):
    def test_vagas_str(self):
        # Crie uma instância de Vagas para teste
        vaga = Vagas.objects.create(
            empresa="Empresa Teste",
            titulo="Vaga de Teste",
            salario="1000",
            escolaridade="Ensino Médio",
        )

        # Verifique se a representação da vaga em forma de string é igual ao esperado
        esperado = "Vaga de Teste - Empresa Teste"
        self.assertEqual(str(vaga), esperado)
