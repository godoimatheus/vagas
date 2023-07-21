from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from empresas.models import Vagas
from .models import Candidatura
from .forms import CandidaturaForm
# Create your views here.


def home(request):
    return render(request, "home.html")


def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")

    username = request.POST.get("username")
    email = request.POST.get("email")
    senha = request.POST.get("senha")

    user = User.objects.filter(username=username).first()

    if user:
        return HttpResponse("Já cadastrado")

    user = User.objects.create_user(username=username, email=email, password=senha)
    user.save()

    return HttpResponse("Usuário cadastrado com sucesso")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    username = request.POST.get("username")
    senha = request.POST.get("senha")

    user = authenticate(username=username, password=senha)

    if user:
        login_django(request, user)
        return HttpResponse("autenticado")
    return HttpResponse("Email ou senha inválidos")


@login_required(login_url="/auth/login/")
def plataforma():
    return HttpResponse("Plataforma")


def vagas_home(request):
    vagas = Vagas.objects.all()
    return render(request, "vagas_home.html", {"vagas": vagas})


def vagas_detalhes(request, vaga_id):
    vaga = get_object_or_404(Vagas, pk=vaga_id)
    return render(request, "vagas_detalhes.html", {"vaga": vaga})


@login_required
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
