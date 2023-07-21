from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login, name="login"),
    path("plataforma/", views.plataforma, name="plataforma"),
    path("vagas/", views.vagas_home, name="vagas_home"),
    path("vagas/<int:vaga_id>", views.vagas_detalhes, name="vagas_detalhes"),
    path("vagas/<int:vaga_id>/candidatar", views.vagas_candidatar, name="vagas_candidatar"),
]
