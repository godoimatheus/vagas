from django.test import TestCase
from django.contrib.auth.models import User
from empresas.models import Vagas
from ..models import Candidatura

# pylint: disable=E1101


class CandidaturaTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testeuser", email="testeemail@email.com", password="password"
        )
        self.vaga = Vagas.objects.create(
            titulo="Vaga de teste", salario="1000", escolaridade="Ensino Superior"
        )

    def test_candidatura_str(self):
        candidatura = Candidatura.objects.create(
            candidato=self.user,
            vaga=self.vaga,
            pretensao_salario="Até 1000",
            experiencia="Até 1 ano",
            ultima_escolaridade="Ensino médio",
        )

        esperado = f"Candidatura de {self.user.username} para {self.vaga.titulo}"
        self.assertEqual(str(candidatura), esperado)
