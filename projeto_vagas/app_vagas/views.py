from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from empresas.models import Vagas
from .models import Candidatura
from .forms import CandidaturaForm
from rolepermissions.decorators import has_role_decorator

# Create your views here.


def home(request):
    return render(request, "home.html")


@login_required(login_url="/")
@has_role_decorator("candidato")
def vagas_home(request):
    vagas = Vagas.objects.all()
    return render(request, "vagas_home.html", {"vagas": vagas})


@login_required(login_url="/")
@has_role_decorator("candidato")
def vagas_detalhes(request, vaga_id):
    vaga = get_object_or_404(Vagas, pk=vaga_id)
    return render(request, "vagas_detalhes.html", {"vaga": vaga})


@login_required(login_url="/")
@has_role_decorator("candidato")
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vagas, pk=vaga_id)
    candidato = request.user

    candidatura_existente = Candidatura.objects.filter(candidato=candidato, vaga=vaga).exists()

    if candidatura_existente:
        return render(request, "candidatura_existente.html", {"vaga": vaga})

    if request.method == "POST":
        form = CandidaturaForm(request.POST)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.candidato = candidato
            candidatura.vaga = vaga
            candidatura.save()
            return render(request, "candidatura_sucesso.html", {"vaga": vaga})
    else:
        form = CandidaturaForm()

    return render(request, "candidatar_vaga.html", {"form": form, "vaga": vaga})
