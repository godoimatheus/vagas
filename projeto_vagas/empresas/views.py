from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
# from django.contrib.auth.decorators import login_required
from .models import Vagas

# Create your views here.


def cadastro_empresas(request):
    if request.method == "GET":
        return render(request, "empresas/cadastro.html")
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse("Já cadastrado")

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return HttpResponse("Usuário cadastrado com sucesso")


def login_empresas(request):
    if request.method == "GET":
        return render(request, "empresas/login.html")
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            return HttpResponse("autenticado")
        else:
            return HttpResponse("Email ou senha inválidos")


def vagas(request):
    vagas = Vagas.objects.all()
    return render(request, "empresas/vagas.html", {"vagas": vagas})

def criar_vaga(request):
    return render(request, "empresas/criar_vaga.html")


def salvar_vaga(request):
    titulo = request.POST.get("titulo")
    salario_value = request.POST.get("salario")
    dict_salarios = {
        1: "Até 1000",
        2: "De 1000 a 2000",
        3: "De 2000 a 3000",
        4: "Acima de 4000"
    }
    salario = dict_salarios[int(salario_value)]
    escolaridade_value = request.POST.get("escolaridade")
    dict_escolaridade = {
        1: "Ensino fundamental",
        2: "Ensino médio",
        3: "Tecnólogo",
        4: "Ensino Superior",
        5: "Pós / MBA / Mestrado",
        6: "Doutorado"
    }
    escolaridade = dict_escolaridade[int(escolaridade_value)]
    vaga = Vagas(
        titulo=titulo,
        salario=salario,
        escolaridade=escolaridade
    )
    vaga.save()
    return HttpResponse("Vaga salva com sucesso")
