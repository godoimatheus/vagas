from django.test import TestCase
from django.contrib.auth.models import User
from empresas.models import Vagas
from ..forms import CandidaturaForm


# pylint: disable=E1101


# Create your tests here.
class FormsCandidaturaTest(TestCase):
    def setUp(self) -> None:
        self.candidato = User.objects.create_user(username="usuario")
        self.vaga = Vagas.objects.create(
            empresa="Teste empresa",
            titulo="Título vaga",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )

    def test_forms_candidatura_valida(self):
        dados_candidatura = {
            "candidato": self.candidato.id,
            "vaga": self.vaga.id,
            "pretensao_salario": "Até 1000",
            "experiencia": "Até 1 ano",
            "ultima_escolaridade": "Ensino fundamental",
        }
        form = CandidaturaForm(data=dados_candidatura)
        self.assertTrue(form.is_valid())

    def test_forms_candidatura_invalida(self):
        dados_candidatura = {
            "vaga": self.vaga.id,
            "pretensao_salario": "Até 1000",
            "experiencia": "Até 1 ano",
            "ultima_experiencia": "Ensino fundamental",
        }
        form = CandidaturaForm(data=dados_candidatura)
        self.assertFalse(form.is_valid())
