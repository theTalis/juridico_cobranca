from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
from .services import *
from django.core.files.storage import FileSystemStorage

def home(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return redirect('login')
    
    titulos = get_titulos()
    for titulo in titulos:
        if titulo.forma_contato.descricao == 'Whatsapp':
            titulo.whatsapp = get_whatsapp(titulo.sacado.nome, titulo.contato)

    dados = {
        'titulos': titulos,
        'links': get_links()
    }
    return render(request, 'home.html', dados)

def login(request):
    return render(request, 'login.html')

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

def submit_importacao(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        content = file.read()

        set_arquivo(file)
        
        lines = content.splitlines()
        for line in lines:
            line = str(line)
            items = line.split(',')

            if len(items[4]) > 0:
                dados = {
                    'cedente': items[0]
                }
                import_titulo(request, dados)

    messages.success(request, 'Dados importados com sucesso')
    return redirect('importacao')
    
    