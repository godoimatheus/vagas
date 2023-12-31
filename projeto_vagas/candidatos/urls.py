from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro_candidatos, name="cadastro_candidatos"),
    path("login/", views.login_candidatos, name="login_candidatos"),
    path("vagas/", views.vagas_home, name="vagas_home"),
    path("vagas/<int:vaga_id>", views.vagas_detalhes, name="vagas_detalhes"),
    path(
        "vagas/<int:vaga_id>/candidatar", views.candidatar_vaga, name="candidatar_vaga"
    ),
]
