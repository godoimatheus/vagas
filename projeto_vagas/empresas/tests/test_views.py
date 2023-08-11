from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from candidatos.models import Candidatura
from ..models import Vagas

# pylint: disable=E1101


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

    def test_pagina_de_criar_vagas(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("criar_vaga"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "empresas/criar_vaga.html")

    def test_form_criar_vagas_redirecionamento_e_se_esta_salvando(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(
            reverse("salvar_vaga"),
            {
                "titulo": "Vaga de teste",
                "salario": "1",
                "escolaridade": "1",
            },
        )
        nova_vaga = Vagas.objects.get(titulo="Vaga de teste")
        self.assertEqual(nova_vaga.empresa, self.username)
        self.assertEqual(nova_vaga.salario, "Até 1000")
        self.assertEqual(nova_vaga.escolaridade, "Ensino fundamental")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("vagas"))

    def test_pagina_de_detalhes_vagas(self):
        vaga = Vagas.objects.create(
            empresa=self.empresa.username,
            titulo="Vaga de Teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("detalhes_vaga", args=[vaga.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "empresas/detalhes_vaga.html")

    def test_pagina_de_editar_vagas(self):
        vaga = Vagas.objects.create(
            empresa=self.empresa.username,
            titulo="Vaga de teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("editar_vaga", args=[vaga.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "empresas/editar_vaga.html")

    def test_form_edicao_de_vagas_verifica_redirecionamento_e_salvamento(self):
        self.client.login(username=self.username, password=self.password)
        vaga = Vagas.objects.create(
            empresa=self.empresa.username,
            titulo="Vaga de teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )
        response = self.client.post(
            reverse("editar_vaga", args=[vaga.id]),
            {"titulo": "Vaga de teste editada", "salario": "2", "escolaridade": "2"},
        )
        vaga_editada = Vagas.objects.get(titulo="Vaga de teste editada")
        self.assertEqual(vaga_editada.empresa, self.username)
        self.assertEqual(vaga_editada.titulo, "Vaga de teste editada")
        self.assertEqual(vaga_editada.salario, "De 1000 a 2000")
        self.assertEqual(vaga_editada.escolaridade, "Ensino médio")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("detalhes_vaga", args=[vaga.id]))

    def test_deletar_vagas(self):
        self.client.login(username=self.username, password=self.password)
        vaga = Vagas.objects.create(
            empresa=self.username,
            titulo="Vaga de teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )
        response = self.client.post(reverse("deletar_vaga", args=[vaga.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("vagas"))

        try:
            self.assertTrue(Vagas.objects.get(titulo="Vaga de teste"))
        except Vagas.DoesNotExist:
            pass

    def test_pagina_de_detalhes_dos_candidatos(self):
        self.client.login(username=self.username, password=self.password)
        vaga = Vagas.objects.create(
            empresa=self.username,
            titulo="Vaga de teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )
        candidato = User.objects.create_user(username="candidato", password="senha123")
        candidatura = Candidatura.objects.create(
            candidato=candidato,
            vaga=vaga,
            pretensao_salario="Até 1000",
            experiencia="Até 1 ano",
            ultima_escolaridade="Ensino fundamental",
        )
        response = self.client.get(reverse("candidatos_vaga", args=[vaga.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "empresas/candidatos_vaga.html")
        self.assertIn(candidatura, response.context["candidaturas"])
        candidatura.refresh_from_db()
        self.assertEqual(candidatura.pontuacao, 2)

    def test_vaga_sem_candidatos(self):
        self.client.login(username=self.username, password=self.password)
        vaga = Vagas.objects.create(
            empresa=self.username,
            titulo="Vaga de teste",
            salario="Até 1000",
            escolaridade="Ensino fundamental",
        )
        response = self.client.get(reverse("candidatos_vaga", args=[vaga.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "empresas/candidatos_vaga.html")
        self.assertEqual(len(response.context["candidaturas"]), 0)
