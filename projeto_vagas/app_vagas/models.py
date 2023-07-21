from django.db import models
from django.contrib.auth.models import User
from empresas.models import Vagas


class Candidatura(models.Model):
    CANDIDATURA_CHOICES = [
        ("Até 1000", "Até 1000"),
        ("De 1000 a 2000", "De 1000 a 2000"),
        ("De 2000 a 3000", "De 2000 a 3000"),
        ("Acima de 3000", "Acima de 3000"),
    ]
    EXPERIENCIA_CHOICES = [
        ("Até 1 ano", "Até 1 ano"),
        ("De 1 ano a 2 anos", "De 1 ano a 2 anos"),
        ("De 2 anos a 3 anos", "De 2 anos a 3 anos"),
        ("Acima de 3 anos", "Acima de 3 anos"),
    ]
    ESCOLARIDADE_CHOICES = [
        ("Ensino fundamental", "Ensino fundamental"),
        ("Ensino médio", "Ensino médio"),
        ("Tecnólogo", "Tecnólogo"),
        ("Ensino Superior", "Ensino Superior"),
        ("Pós / MBA / Mestrado", "Pós / MBA / Mestrado"),
        ("Doutorado", "Doutorado"),
    ]

    candidato = models.ForeignKey(User, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vagas, on_delete=models.CASCADE)
    pretensao_salario = models.CharField(max_length=50, choices=CANDIDATURA_CHOICES, default="Até 1000")
    experiencia = models.CharField(max_length=50, choices=EXPERIENCIA_CHOICES, default='Até 1 ano')
    ultima_escolaridade = models.CharField(max_length=50, choices=ESCOLARIDADE_CHOICES, default="Ensino fundamental")

    def __str__(self):
        return f"Candidatura de {self.candidato.username} para {self.vaga.titulo}"
