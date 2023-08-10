from django.test import TestCase, Client
from django.urls import reverse


class EmpresasViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_status_pagina_de_cadastro_e_template_empresas(self):
        response = self.client.get(reverse("cadastro_empresas"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "empresas/cadastro.html")

    def test_redirecionamento_apos_cadastro(self):
        response = self.client.post(
            reverse("cadastro_empresas"),
            {
                "username": "empresa",
                "email": "empresa@email.com",
                "password": "senha123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/empresas/cadastro/")
