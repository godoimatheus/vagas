from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role


class EmpresasViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username = "empresa"
        self.email = "empresa@email.com"
        self.password = "senha123"
        self.empresa = User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )
        assign_role(self.empresa, "empresa")

    def test_status_pagina_de_cadastro_e_template_empresas(self):
        response = self.client.get(reverse("cadastro_empresas"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "empresas/cadastro.html")

    def test_redirecionamento_apos_cadastro(self):
        response = self.client.post(
            reverse("cadastro_empresas"),
            {
                "username": self.empresa.username,
                "email": self.empresa.email,
                "password": self.empresa.password,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/empresas/login/")

    def test_status_pagina_login_e_template_empresas(self):
        response = self.client.get(reverse("login_empresas"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "empresas/login.html")

    def test_login_empresas_com_sucesso(self):
        response = self.client.post(
            reverse("login_empresas"),
            {"username": self.username, "password": self.password},
        )
        self.assertRedirects(response, reverse("vagas"))

    def test_login_empresas_sem_sucesso(self):
        response = self.client.post(
            reverse("login_empresas"), {"username": self.username, "password": "123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "empresas/login_erro.html")

    def test_logout_view(self):
        self.assertTrue(
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(reverse("logout_view"))
        self.assertRedirects(response, reverse("home"))

    def test_se_usuario_tem_permissao_de_empresa(self):
        response = self.client.get(reverse("vagas"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(has_role(self.empresa, "empresa"))

    def test_se_usuario_nao_tem_permissao_de_empresa(self):
        response = self.client.get(reverse("vagas"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(has_role(self.empresa, "candidato"))
