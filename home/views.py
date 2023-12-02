from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
from .services import *

def home(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return render(request, 'login.html')
    return render(request, 'home.html')

@csrf_protect
def submit_login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        request.session['user'] = user.username
        messages.success(
            request, 'Login efetuado')
        return redirect('home')
    messages.warning(
        request, 'Login ou senha inválido')
    return render(request, 'login.html')

def logout(request):
    if not 'user' in request.session:
        del request.session['user']
    messages.success(
        request, 'Logout efetuado')
    return render(request, 'login.html')

def cadastro(request):
    params = {
        "cedentes": get_cedentes(),
        "sacados": get_sacados(),
        "pagadores": get_pagadores(),
        "formas_contato": get_formas_contato()
    }
    return render(request, 'cadastro.html', params)

def importacao(request):
    return render(request, 'importacao.html')

def submit_cadastro(request):
    erros_cadastro = get_erros_cadastro(request)
    if erros_cadastro == None:
        set_titulo(request)
        messages.success(request, 'Cadastro gravado com sucesso')
    else:
        messages.warning(request, erros_cadastro)
    return redirect('cadastro')