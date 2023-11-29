from django.shortcuts import render
from django.contrib import messages

def index(request):
    return render(request, 'login.html')

def submit_login(request):
    messages.success(
        request, 'Login efetuado')
    return render(request, 'login.html')