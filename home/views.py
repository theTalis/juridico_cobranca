from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
from .services import *
from django.utils.dateformat import DateFormat
from datetime import datetime, timedelta

def home(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return redirect('login')

    search = ''
    if 'search' in request.POST:
        search = request.POST['search']

    valor_filtro = ''
    if 'valor_filtro' in request.POST:
        valor_filtro = request.POST['valor_filtro']

    situacao_filtro = ''
    if 'situacao_filtro' in request.POST:
        situacao_filtro = request.POST['situacao_filtro']

    cedentes = []
    sacados = []
    filtered_titulos = []

    titulos = get_titulos_em_aberto()
    for titulo in titulos:
        if titulo.forma_contato.descricao.upper() == 'WHATSAPP':
            titulo.whatsapp = get_whatsapp(titulo.sacado.nome, titulo.contato)
            if titulo.data_vencimento:
                titulo.data_vencimento_formatada = DateFormat(titulo.data_vencimento)
                titulo.data_vencimento_formatada = titulo.data_vencimento_formatada.format('Y-m-d')
            if titulo.data_pagamento:
                titulo.data_pagamento_formatada = DateFormat(titulo.data_pagamento)
                titulo.data_pagamento_formatada = titulo.data_pagamento_formatada.format('Y-m-d')
        titulo.anexos = get_titulo_anexos(titulo.id)
        titulo.observacoes = get_titulo_observacoes(titulo.id)
        
        has_value = len(search) > 0 and (str(search).lower() in str(titulo.cedente.nome).lower() or str(search).lower() in str(titulo.sacado.nome).lower())
        has_valor_filtro = len(valor_filtro) > 0 and float(valor_filtro) == float(titulo.valor)
        has_situacao_filtro = len(situacao_filtro) > 0 and situacao_filtro == titulo.situacao.descricao

        dados_sacado = {
            "cedente": titulo.cedente.nome,
            "sacado": titulo.sacado.nome
        }

        if (not search or has_value) and (not valor_filtro or has_valor_filtro) and (not situacao_filtro or has_situacao_filtro):
            if not titulo.cedente.nome in cedentes:
                cedentes.append(titulo.cedente.nome)
            
            if not dados_sacado in sacados:
                sacados.append(dados_sacado)
            
            filtered_titulos.append(titulo)

    dados = {
        'cedentes': cedentes,
        'sacados': sacados,
        'titulos': filtered_titulos,
        'links': get_links(),
        'search': search,
        'valor_filtro': valor_filtro,
        'situacao_filtro': situacao_filtro,
        'situacoes': get_situacoes(),
        "formas_contato": get_formas_contato()
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
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return redirect('login')

    params = {
        "cedentes": get_cedentes(),
        "sacados": get_sacados(),
        "pagadores": get_pagadores(),
        "tipos_titulo": get_tipos_titulo(),
        "origens": get_origens(),
        "formas_contato": get_formas_contato()
    }
    return render(request, 'cadastro.html', params)

def importacao(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return redirect('login')

    params = {
        "cedentes": get_cedentes(),
    }
    return render(request, 'importacao.html', params)

def submit_cadastro(request):
    erros_cadastro = get_erros_cadastro(request)
    if erros_cadastro == None:
        set_titulo(request)
        messages.success(request, 'Cadastro gravado com sucesso')
    else:
        messages.warning(request, erros_cadastro)
    return redirect('cadastro')

def submit_importacao(request):
    cedente = ''
    if 'cedente' in request.POST:
        cedente = request.POST['cedente']

    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        content = file.read()

        set_arquivo(file)
        
        lines = content.splitlines()
        for line in lines:
            line = str(line)
            items = line.split(',')

            if len(items[3]) > 0:
                tipo = ''
                if items[10] == 'DP':
                    tipo = 'DUPLICATA'
                elif items[10] == 'CQ':
                    tipo = 'CHEQUE'

                data_vencimento = ''
                if (len(items[0]) > 0):
                    data_vencimento = str(items[0]).replace('b', '').replace("'", '')
                    data_vencimento = datetime.strptime(data_vencimento, "%d/%m/%Y").strftime("%Y-%m-%d")

                data_protesto = ''
                if (len(items[19]) > 0):
                    data_protesto = str(items[19]).replace('b', '').replace("'", '')
                    data_protesto = datetime.strptime(data_protesto, "%d/%m/%Y").strftime("%Y-%m-%d")

                valor = 0
                if (len(items[12]) > 0):
                    valor = str(items[12]).replace('b', '').replace('"', '')
                    valor = float(valor)
                
                dados = {
                    'cedente': cedente,
                    'data_vencimento': data_vencimento,
                    'cpf_cnpj': items[2],
                    'sacado': items[3],
                    'tipo': tipo, 
                    'contato': get_contato(items[8]), 
                    'valor': valor, 
                    'data_protesto': data_protesto,
                    'origem': items[23],
                    'forma_contato': 'WHATSAPP',
                    'pagador': 'SACADO'
                }
                import_titulo(request, dados)

    messages.success(request, 'Dados importados com sucesso')
    return redirect('importacao')
    
def submit_update_titulo(request):
    upset_titulo(request)
    messages.success(request, 'Cadastro atualizado com sucesso')
    return redirect('home')

def submit_update_pagamento(request):
    upset_pagamento(request)
    messages.success(request, 'Cadastro atualizado com sucesso')
    return redirect('pagamento')

def submit_update_observacoes(request):
    upset_observacoes(request)
    messages.success(request, 'Cadastro atualizado com sucesso')
    return redirect('home')

def pagamento(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return redirect('login')

    data_atual = datetime.today()
    
    data_inicial = str(data_atual - timedelta(days=7))[0:10]
    if 'data_inicial' in request.POST:
        data_inicial = request.POST['data_inicial']

    data_final = str(data_atual + timedelta(days=7))[0:10]
    if 'data_final' in request.POST:
        data_final = request.POST['data_final']

    pagamentos = get_pagamentos(data_inicial, data_final)

    quantidade_pagamentos = 0
    valor_pago = 0
    for pagamento in pagamentos:
        quantidade_pagamentos += 1
        valor_pago += pagamento.valor

        if pagamento.data_pagamento:
            pagamento.data_pagamento_formatada = DateFormat(pagamento.data_pagamento)
            pagamento.data_pagamento_formatada = pagamento.data_pagamento_formatada.format('Y-m-d')

    dados = {
        'pagamentos': pagamentos,
        'quantidade_pagamentos': quantidade_pagamentos,
        'valor_pago': valor_pago,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'situacoes': get_situacoes()
    }
    return render(request, 'pagamento.html', dados)

def acordo(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return redirect('login')

    data_atual = datetime.today()
    
    data_inicial = str(data_atual - timedelta(days=7))[0:10]
    if 'data_inicial' in request.POST:
        data_inicial = request.POST['data_inicial']

    data_final = str(data_atual + timedelta(days=7))[0:10]
    if 'data_final' in request.POST:
        data_final = request.POST['data_final']

    acordos = get_acordos(data_inicial, data_final)
    for acordo in acordos:
        if acordo.data_pagamento:
            acordo.data_pagamento_formatada = DateFormat(acordo.data_pagamento)
            acordo.data_pagamento_formatada = acordo.data_pagamento_formatada.format('Y-m-d')

    dados = {
        'acordos': acordos,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'situacoes': get_situacoes()
    }
    return render(request, 'acordo.html', dados)

def juridico_externo(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return redirect('login')

    data_atual = datetime.today()
    
    data_inicial = str(data_atual - timedelta(days=7))[0:10]
    if 'data_inicial' in request.POST:
        data_inicial = request.POST['data_inicial']

    data_final = str(data_atual + timedelta(days=7))[0:10]
    if 'data_final' in request.POST:
        data_final = request.POST['data_final']

    juridico_externo = get_juridico_externo(data_inicial, data_final)

    dados = {
        'titulos': juridico_externo,
        'data_inicial': data_inicial,
        'data_final': data_final
    }
    return render(request, 'juridico_externo.html', dados)
