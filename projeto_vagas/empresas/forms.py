from django import forms
from .models import Vagas


class FormVagas(forms.ModelForm):
    class Meta:
        model = Vagas
        fields = [
            "titulo",
            "salario",
            "escolaridade"
        ]
