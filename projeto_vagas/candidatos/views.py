from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from empresas.models import Vagas
from .models import Candidatura
from .forms import CandidaturaForm

# pylint: disable=E1101


# Create your views here.
def cadastro_candidatos(request):
    if request.method == "GET":
        return render(request, "candidatos/cadastro.html")
    username = request.POST.get("username")
    email = request.POST.get("email")
    senha = request.POST.get("senha")

    user = User.objects.filter(username=username).first()

    if user:
        return redirect("login_candidatos")
    if not (username and email and senha):
        return redirect("cadastro_candidatos")
    user = User.objects.create_user(username=username, email=email, password=senha)
    user.save()
    assign_role(user, "candidato")
    return redirect("login_candidatos")


def login_candidatos(request):
    if request.method == "GET":
        return render(request, "candidatos/login.html")
    username = request.POST.get("username")
    senha = request.POST.get("senha")

    user = authenticate(username=username, password=senha)

    if user:
        login_django(request, user)
        return redirect("vagas_home")
    return render(request, "candidatos/login_erro.html")


@login_required(login_url="/")
@has_role_decorator("candidato")
def vagas_home(request):
    vagas = Vagas.objects.all()
    return render(request, "candidatos/vagas_home.html", {"vagas": vagas})


@login_required(login_url="/")
@has_role_decorator("candidato")
def vagas_detalhes(request, vaga_id):
    vaga = get_object_or_404(Vagas, pk=vaga_id)
    return render(request, "candidatos/vagas_detalhes.html", {"vaga": vaga})


@login_required(login_url="/")
@has_role_decorator("candidato")
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vagas, pk=vaga_id)
    candidato = request.user

    candidatura_existente = Candidatura.objects.filter(
        candidato=candidato, vaga=vaga
    ).exists()

    if candidatura_existente:
        return render(request, "candidatos/candidatura_existente.html", {"vaga": vaga})

    if request.method == "POST":
        form = CandidaturaForm(request.POST)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.candidato = candidato
            candidatura.vaga = vaga
            candidatura.save()
            return render(
                request, "candidatos/candidatura_sucesso.html", {"vaga": vaga}
            )
    else:
        form = CandidaturaForm()

    return render(
        request, "candidatos/candidatar_vaga.html", {"form": form, "vaga": vaga}
    )
