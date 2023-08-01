from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_vagas.urls")),
    path("empresas/", include("empresas.urls")),
    path("candidatos/", include("candidatos.urls")),
]
