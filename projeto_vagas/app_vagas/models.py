from django.db import models
from django.contrib.auth.models import User
from empresas.models import Vagas


class Candidatura(models.Model):
    candidato = models.ForeignKey(User, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vagas, on_delete=models.CASCADE)
    data_candidatura = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['candidato', 'vaga']
