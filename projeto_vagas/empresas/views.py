from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .models import Vagas
from .forms import FormVagas
from app_vagas.models import Candidatura
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator

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
            return redirect("login_empresas")

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        assign_role(user, "empresa")
        return redirect("login_empresas")


def login_empresas(request):
    if request.method == "GET":
        return render(request, "empresas/login.html")
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            return redirect("vagas")
        else:
            return render(request, "empresas/login_erro.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/empresas/login")
@has_role_decorator("empresa")
def vagas(request):
    vagas = Vagas.objects.all()
    return render(request, "empresas/vagas.html", {"vagas": vagas})


@login_required(login_url="/empresas/login")
@has_role_decorator("empresa")
def criar_vaga(request):
    return render(request, "empresas/criar_vaga.html")


@login_required(login_url="/empresas/login")
@has_role_decorator("empresa")
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
    return redirect("detalhes_vagas")


@login_required(login_url="/empresas/login")
@has_role_decorator("empresa")
def detalhes_vaga(request, vaga_id):
    vaga = get_object_or_404(Vagas, pk=vaga_id)
    return render(request, "empresas/detalhes_vaga.html", {"vaga": vaga})


@login_required(login_url="/empresas/login")
@has_role_decorator("empresa")
def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vagas, pk=vaga_id)
    form = FormVagas(instance=vaga)

    if request.method == "POST":
        form = FormVagas(request.POST, instance=vaga)

        if form.is_valid():
            salario_value = form.cleaned_data["salario"]
            dict_salarios = {
                1: "Até 1000",
                2: "De 1000 a 2000",
                3: "De 2000 a 3000",
                4: "Acima de 4000"
            }
            salario = dict_salarios[int(salario_value)]
            vaga.salario = salario

            escolaridade_value = form.cleaned_data["escolaridade"]
            dict_escolaridade = {
                1: "Ensino fundamental",
                2: "Ensino médio",
                3: "Tecnólogo",
                4: "Ensino Superior",
                5: "Pós / MBA / Mestrado",
                6: "Doutorado"
            }
            escolaridade = dict_escolaridade[int(escolaridade_value)]
            vaga.escolaridade = escolaridade

            form.save()
            return redirect("detalhes_vaga", vaga_id=vaga.id)

    return render(request, "empresas/editar_vaga.html", {"form": form, "vaga": vaga})


@login_required(login_url="/empresas/login")
@has_role_decorator("empresa")
def deletar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vagas, pk=vaga_id)
    if request.method == "POST":
        vaga.delete()
        return redirect("vagas")
    return render(request, "empresas/deletar_vaga.html", {"vaga": vaga})


@login_required(login_url="/empresas/login")
@has_role_decorator("empresa")
def candidatos_vaga(request, vaga_id):
    vaga = get_object_or_404(Vagas, pk=vaga_id)
    candidaturas = Candidatura.objects.filter(vaga=vaga)
    return render(request, "empresas/candidatos_vaga.html", {"vaga": vaga, "candidaturas": candidaturas})
