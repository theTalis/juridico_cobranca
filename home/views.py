from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import authenticate
from .services import *
from django.utils.dateformat import DateFormat
from datetime import datetime, timedelta
import calendar
from django.http import JsonResponse
import json

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

    supervisor_filtro = ''
    if 'supervisor_filtro' in request.POST:
        supervisor_filtro = request.POST['supervisor_filtro']

    operador_filtro = ''
    if 'operador_filtro' in request.POST:
        operador_filtro = request.POST['operador_filtro']

    situacao_filtro = ''
    if 'situacao_filtro' in request.POST:
        situacao_filtro = request.POST['situacao_filtro']

    if situacao_filtro == '' and 'situacao_filtro' in request.session:
        situacao_filtro = request.session['situacao_filtro']

    request.session['situacao_filtro'] = situacao_filtro

    cedentes = []
    sacados = []
    filtered_titulos = []

    titulos = get_titulos_em_aberto()
    for titulo in titulos:
        titulo.whatsapp = get_whatsapp(titulo.sacado.nome, titulo.contato)
        if titulo.data_vencimento:
            titulo.data_vencimento_formatada = DateFormat(titulo.data_vencimento)
            titulo.data_vencimento_formatada = titulo.data_vencimento_formatada.format('Y-m-d')
        if titulo.data_pagamento:
            titulo.data_pagamento_formatada = DateFormat(titulo.data_pagamento)
            titulo.data_pagamento_formatada = titulo.data_pagamento_formatada.format('Y-m-d')
        titulo.anexos = get_titulo_anexos(titulo.id)
        titulo.observacoes = get_titulo_observacoes(titulo.id)

        if valor_filtro:
            valor_filtro = float(valor_filtro)

        valor_titulo = 0
        if titulo.valor:
            valor_titulo = float(titulo.valor)

        supervisor_titulo = ''
        if titulo.supervisor:
            supervisor_titulo = titulo.supervisor.nome

        operador_titulo = ''
        if titulo.operador:
            operador_titulo = titulo.operador.nome

        has_value = len(search) > 0 and (str(search).lower() in str(titulo.cedente.nome).lower() or str(search).lower() in str(titulo.sacado.nome).lower())
        has_valor_filtro = valor_filtro == valor_titulo
        has_situacao_filtro = len(situacao_filtro) > 0 and situacao_filtro == titulo.situacao.descricao or situacao_filtro == 'TODAS'
        has_supervisor_filtro = len(supervisor_filtro) > 0 and supervisor_filtro == supervisor_titulo or supervisor_filtro == 'TODOS'
        has_operador_filtro = len(operador_filtro) > 0 and operador_filtro == operador_titulo or operador_filtro == 'TODOS'

        dados_sacado = {
            "cedente": titulo.cedente.nome,
            "sacado": titulo.sacado.nome
        }

        if (not search or has_value) and (not valor_filtro or has_valor_filtro) and (not situacao_filtro or has_situacao_filtro) and (not supervisor_filtro or has_supervisor_filtro) and (not operador_filtro or has_operador_filtro):
            if not titulo.cedente.nome in cedentes:
                cedentes.append(titulo.cedente.nome)
            
            if not dados_sacado in sacados:
                sacados.append(dados_sacado)
            
            filtered_titulos.append(titulo)

    dados = {
        'cedentes': cedentes,
        'sacados': sacados,
        "pagadores": get_pagadores(),
        'titulos': filtered_titulos,
        'links': get_links(),
        'search': search,
        'valor_filtro': valor_filtro,
        'supervisor_filtro': supervisor_filtro,
        'operador_filtro': operador_filtro,
        'situacao_filtro': situacao_filtro,
        'situacoes': get_situacoes(),
        "formas_contato": get_formas_contato(),
        "supervisores": get_supervisores(),
        "operadores": get_operadores()
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
        "formas_contato": get_formas_contato(),
        "situacoes": get_situacoes()
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
    if not erros_cadastro:
        set_titulo(request)
        messages.success(request, 'Cadastro gravado com sucesso')
    else:
        messages.warning(request, erros_cadastro)
    return redirect('cadastro')

@csrf_exempt
def update_checked(request):
    json_body = json.loads(request.body)

    items = json_body["items"]
    for item in items:
        titulo_id = str(item["id"]).replace("marcado_", "")

        titulo = Titulo.objects.get(pk=titulo_id)
        titulo.marcado = item["checked"]
        titulo.save()

    return JsonResponse({})

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
            items = line.split(';')

            if len(items[2]) > 0:
                tipo = ''
                if items[8] == 'DP':
                    tipo = 'DUPLICATA'
                elif items[8] == 'CQ':
                    tipo = 'CHEQUE'

                data_vencimento = ''
                if (len(items[0]) > 0):
                    data_vencimento = str(items[0]).replace('b', '').replace("'", '')
                    data_vencimento = datetime.strptime(data_vencimento, "%d/%m/%Y").strftime("%Y-%m-%d")

                data_protesto = ''
                if (len(items[14]) > 0):
                    data_protesto = str(items[14]).replace('b', '').replace("'", '')
                    data_protesto = datetime.strptime(data_protesto, "%d/%m/%Y").strftime("%Y-%m-%d")

                valor = 0
                if (len(items[10]) > 0):
                    valor = str(items[10]).replace('.', '').replace(',', '.')
                    valor = float(valor)
                
                origem = str(items[17]).replace("'", "")

                dados = {
                    'cedente': cedente,
                    'data_vencimento': data_vencimento,
                    'cpf_cnpj': items[1],
                    'sacado': items[2],
                    'tipo': tipo, 
                    'contato': get_contato(items[7]), 
                    'valor': valor, 
                    'data_protesto': data_protesto,
                    'origem': origem,
                    'forma_contato': 'WHATSAPP',
                    'pagador': 'SACADO'
                }
                import_titulo(request, dados)

    messages.success(request, 'Dados importados com sucesso')
    return redirect('importacao')
    
def submit_update_titulo(request):
    upset_titulo(request)

    upset_observacoes(request)

    set_pagamento_parcial(request)
    messages.success(request, 'Titulo atualizado com sucesso')
    return redirect('home')

def submit_update_titulo_acordo(request):
    upset_titulo(request)

    upset_observacoes(request)

    set_pagamento_parcial(request)
    messages.success(request, 'Acordo atualizado com sucesso')
    return redirect('acordo')

def submit_update_pagamento(request):
    upset_pagamento(request)
    messages.success(request, 'Cadastro atualizado com sucesso')
    return redirect('pagamento')

def submit_update_acordo(request):
    upset_pagamento(request)
    messages.success(request, 'Cadastro atualizado com sucesso')
    return redirect('acordo')

def submit_update_juridico_externo(request):
    upset_pagamento(request)
    messages.success(request, 'Cadastro atualizado com sucesso')
    return redirect('juridico_externo')

def pagamento(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return redirect('login')
    
    data_inicial = get_data_inicial_mes()
    if 'data_inicial' in request.POST:
        data_inicial = request.POST['data_inicial']

    data_final = get_data_final_mes()
    if 'data_final' in request.POST:
        data_final = request.POST['data_final']

    search = ''
    if 'search' in request.POST:
        search = request.POST['search']

    pagamentos = get_pagamentos(data_inicial, data_final)
    filtered_pagamentos = []

    quantidade_pagamentos = 0
    valor_pago = 0
    valores_face = 0
    encargos = 0
    for pagamento in pagamentos:
        quantidade_pagamentos += 1
        valor_pago += pagamento.valor
        if pagamento.valor_face:
            valores_face += float(pagamento.valor_face)
        else:
            valores_face += float(pagamento.valor)

        if pagamento.encargo:
            encargos += float(pagamento.encargo)

        if pagamento.data_pagamento:
            pagamento.data_pagamento_formatada = DateFormat(pagamento.data_pagamento)
            pagamento.data_pagamento_formatada = pagamento.data_pagamento_formatada.format('Y-m-d')

        has_value = len(search) > 0 and (str(search).lower() in str(pagamento.cedente.nome).lower() or str(search).lower() in str(pagamento.sacado.nome).lower())

        if (not search or has_value):
            filtered_pagamentos.append(pagamento)

    dados = {
        'pagamentos': filtered_pagamentos,
        'search': search,
        'quantidade_pagamentos': quantidade_pagamentos,
        'valor_pago': valor_pago,
        'valores_face': valores_face,
        'encargos': encargos,
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

    search = ''
    if 'search' in request.POST:
        search = request.POST['search']
    
    data_inicial = '2020-01-01'
    if 'data_inicial' in request.POST:
        data_inicial = request.POST['data_inicial']

    data_final = get_data_final_mes()
    if 'data_final' in request.POST:
        data_final = request.POST['data_final']

    cedentes = []
    sacados = []
    filtered_acordos = []

    acordos = get_acordos(data_inicial, data_final)
    for acordo in acordos:
        acordo.whatsapp = get_whatsapp(acordo.sacado.nome, acordo.contato)
        if acordo.data_pagamento:
            acordo.data_pagamento_formatada = DateFormat(acordo.data_pagamento)
            acordo.data_pagamento_formatada = acordo.data_pagamento_formatada.format('Y-m-d')

        if acordo.data_vencimento:
            acordo.data_vencimento_formatada = DateFormat(acordo.data_vencimento)
            acordo.data_vencimento_formatada = acordo.data_vencimento_formatada.format('Y-m-d')
        acordo.observacoes = get_titulo_observacoes(acordo.id)
        acordo.anexos = get_titulo_anexos(acordo.id)
    
        has_value = len(search) > 0 and (str(search).lower() in str(acordo.cedente.nome).lower() or str(search).lower() in str(acordo.sacado.nome).lower())

        dados_sacado = {
            "cedente": acordo.cedente.nome,
            "sacado": acordo.sacado.nome
        }

        if (not search or has_value):
            if not acordo.cedente.nome in cedentes:
                cedentes.append(acordo.cedente.nome)

            if not dados_sacado in sacados:
                sacados.append(dados_sacado)

            filtered_acordos.append(acordo)

    dados = {
        'cedentes': cedentes,
        'sacados': sacados,
        'acordos': filtered_acordos,
        'search': search,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'situacoes': get_situacoes(),
        "formas_contato": get_formas_contato(),
        "supervisores": get_supervisores(),
        "operadores": get_operadores()
    }
    return render(request, 'acordo.html', dados)

def juridico_externo(request):
    if not 'user' in request.session:
        messages.warning(
            request, 'Efetue o login')
        return redirect('login')

    data_inicial = get_data_inicial_mes()
    if 'data_inicial' in request.POST:
        data_inicial = request.POST['data_inicial']

    data_final = get_data_final_mes()
    if 'data_final' in request.POST:
        data_final = request.POST['data_final']

    titulos = get_juridico_externo(data_inicial, data_final)

    for titulo in titulos:
        if titulo.data_pagamento:
            titulo.data_pagamento_formatada = DateFormat(titulo.data_pagamento)
            titulo.data_pagamento_formatada = titulo.data_pagamento_formatada.format('Y-m-d')

        if titulo.data_vencimento:
            titulo.data_vencimento_formatada = DateFormat(titulo.data_vencimento)
            titulo.data_vencimento_formatada = titulo.data_vencimento_formatada.format('Y-m-d')

    dados = {
        'titulos': titulos,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'situacoes': get_situacoes()
    }
    return render(request, 'juridico_externo.html', dados)

def get_data_inicial_mes():
    return str(datetime.today().replace(day=1))[0:10]

def get_data_final_mes():
    data_inicial = str(datetime.today().replace(day=1))[0:10]
    ultimo_dia_mes = calendar.monthrange(int(data_inicial[0:4]), int(data_inicial[5:7]))[1]
    return str(datetime.today().replace(day=ultimo_dia_mes))[0:10]