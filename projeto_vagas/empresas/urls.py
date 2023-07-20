from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro_empresas, name="cadastro_empresas"),
    path("login/", views.login_empresas, name="login_empresas"),
    path("vagas/", views.vagas, name="vagas"),
    path("vagas/criar", views.criar_vaga, name="criar_vaga"),
    path("vagas/salvar", views.salvar_vaga, name="salvar_vaga"),
]
