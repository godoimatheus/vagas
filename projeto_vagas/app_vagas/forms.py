from django import forms
from .models import Candidatura


class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = ["pretensao_salario", "experiencia", "ultima_escolaridade"]
        labels = {
            "pretensao_salario": "Pretensão Salarial",
            "experiencia": "Experiência",
            "ultima_escolaridade": "Última Escolaridade",
        }
