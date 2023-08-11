from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from empresas.models import Vagas
from ..models import Candidatura

# pylint: disable=E1101


class CandidatosViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username = "candidato"
        self.email = "candidato@email.com"
        self.password = "senha123"

        self.candidato = User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )
        assign_role(self.candidato, "candidato")

        self.empresa = User.objects.create_user(
            username="empresa", email="empresa@email.com", password="senha123"
        )
        assign_role(self.empresa, "empresa")

    def test_status_pagina_cadastro_e_template(self):
        response = self.client.get(reverse("cadastro_candidatos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "candidatos/cadastro.html")

    def test_redirecionamento_apos_cadastro(self):
        response = self.client.post(
            reverse("cadastro_candidatos"),
            {"username": self.username, "email": self.email, "password": self.password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/candidatos/login/")

    def test_status_pagina_login_e_template(self):
        response = self.client.get(reverse("login_candidatos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "candidatos/login.html")

    def test_login_com_sucesso(self):
        self.client.login(
            username=self.candidato.username, password=self.candidato.password
        )
        response = self.client.get(reverse("vagas_home"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/?next=" + reverse("vagas_home"))

    def test_login_com_erro(self):
        response = self.client.post(
            reverse("login_candidatos"), {"username": self.username, "password": "123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "candidatos/login_erro.html")

    def test_se_usuario_tem_permissao_de_candidato(self):
        response = self.client.get(reverse("vagas_home"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(has_role(self.candidato, "candidato"))

    def test_se_usuario_nao_tem_permissao(self):
        response = self.client.get(reverse("vagas_home"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(has_role(self.candidato, "empresa"))

    def test_pagina_de_detalhes_vagas(self):
        vaga = Vagas.objects.create(
            empresa=self.empresa.username,
            titulo="Vaga de Teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("vagas_detalhes", args=[vaga.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "candidatos/vagas_detalhes.html")

    def test_pagina_candidatar_a_vagas(self):
        vaga = Vagas.objects.create(
            empresa=self.empresa.username,
            titulo="Vaga de Teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("candidatar_vaga", args=[vaga.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "candidatos/candidatar_vaga.html")

    def test_candidatura_com_sucesso(self):
        vaga = Vagas.objects.create(
            empresa=self.empresa.username,
            titulo="Vaga de Teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )

        Candidatura.objects.create(candidato=self.candidato, vaga=vaga)
        self.client.login(
            username=self.candidato.username, password=self.candidato.password
        )
        response = self.client.post(
            reverse("candidatar_vaga", args=[vaga.id]),
            {
                "pretensao_salario": "Até 1000",
                "experiencia": "Até 1 ano",
                "ultima_escolaridade": "Ensino fundamental",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?next=" + reverse("candidatar_vaga", args=[vaga.id])
        )

    def test_candidatura_sem_sucesso(self):
        vaga = Vagas.objects.create(
            empresa=self.empresa.username,
            titulo="Vaga de Teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )
        Candidatura.objects.create(candidato=self.candidato, vaga=vaga)
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(
            reverse("candidatar_vaga", args=[vaga.id]),
            {
                "pretensao_salarial": "Até 1000",
                "experiencia": "Até 1 ano",
                "ultima_escolaridade": "Ensino fundamental",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "candidatos/candidatura_existente.html")
