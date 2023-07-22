from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro_candidatos, name="cadastro_candidatos"),
    path("login/", views.login_candidatos, name="login_candidatos"),
]
