from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role


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
        response = self.client.post(
            reverse("login_candidatos"),
            {"username": self.username, "password": self.password},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "candidatos/vagas_home.html")

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
