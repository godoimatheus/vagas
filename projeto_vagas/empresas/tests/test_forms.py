from django.test import TestCase
from ..models import Vagas
from ..forms import FormVagas

# pylint: disable=E1101


# Create your tests here.
class FormVagasTest(TestCase):
    def setUp(self) -> None:
        self.vaga = Vagas.objects.create(
            empresa="Nome empresa",
            titulo="Nome da vaga",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )

    def test_form_vagas_valida(self):
        dados_vagas = {
            "titulo": self.vaga.titulo,
            "salario": self.vaga.salario,
            "escolaridade": self.vaga.escolaridade,
        }
        form = FormVagas(data=dados_vagas)
        self.assertTrue(form.is_valid())

    def test_form_vagas_invalida(self):
        dados_vagas = {
            "salario": self.vaga.salario,
            "escolaridade": self.vaga.escolaridade,
        }
        form = FormVagas(data=dados_vagas)
        self.assertFalse(form.is_valid())
