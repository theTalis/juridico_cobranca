from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return render(request, 'login.html')
    return render(request, 'home.html')

def submit_login(request):
    messages.success(
        request, 'Login efetuado')
    request.session['user'] = 'teste'
    return redirect('home')

def logout(request):
    del request.session['user']
    messages.success(
        request, 'Logout efetuado')
    return render(request, 'login.html')