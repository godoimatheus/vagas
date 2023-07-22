from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro_empresas, name="cadastro_empresas"),
    path("login/", views.login_empresas, name="login_empresas"),
    path("logout/", views.logout_view, name="logout_view"),
    path("vagas/", views.vagas, name="vagas"),
    path("vagas/criar", views.criar_vaga, name="criar_vaga"),
    path("vagas/salvar", views.salvar_vaga, name="salvar_vaga"),
    path("vagas/<int:vaga_id>", views.detalhes_vaga, name="detalhes_vaga"),
    path("vagas/<int:vaga_id>/editar", views.editar_vaga, name="editar_vaga"),
    path("vagas/<int:vaga_id>/deletar", views.deletar_vaga, name="deletar_vaga"),
    path("vagas/<int:vaga_id>/candidatos", views.candidatos_vaga, name="candidatos_vaga")
]
