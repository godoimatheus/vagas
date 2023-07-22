from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator

# Create your views here.


def cadastro_candidatos(request):
    if request.method == "GET":
        return render(request, "candidatos/cadastro.html")
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            return redirect("login_candidatos")

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        assign_role(user, "candidato")
        return redirect("login_candidatos")


def login_candidatos(request):
    if request.method == "GET":
        return render(request, "candidatos/login.html")
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            return redirect("vagas_home")
        else:
            return render(request, "candidatos/login_erro.html")
