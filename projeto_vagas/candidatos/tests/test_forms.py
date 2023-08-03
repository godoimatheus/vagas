from django.test import TestCase
from ..forms import CandidaturaForm


# Create your tests here.
class FormsCandidaturaTest(TestCase):
    def test_forms_candidatura_valido(self):
        dados_candidatura = {
            "pretensao_salario": "Até 1000",
            "experiencia": "Até 1 ano",
            "ultima_escolaridade": "Ensino médio",
        }
        form = CandidaturaForm(data=dados_candidatura)
        self.assertTrue(form.is_valid())
