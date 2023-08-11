from django.db import models

# Create your models here.


class Vagas(models.Model):
    empresa = models.CharField(max_length=100)
    titulo = models.CharField(max_length=150)
    salario = models.CharField(max_length=50)
    escolaridade = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.titulo} - {self.empresa}"
