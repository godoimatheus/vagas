from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro_empresas, name="cadastro_empresas"),
    path("login/", views.login_empresas, name="login_empresas")
]
