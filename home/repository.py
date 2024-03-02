from .models import *
from django.core.files.storage import FileSystemStorage

def get_dados_cedentes():
    try:
        return Cedente.objects.all()
    except Cedente.DoesNotExist:
        return "Cedentes não encontrados"
    
def get_dados_sacados():
    try:
        return Sacado.objects.all()
    except Sacado.DoesNotExist:
        return "Sacados não encontrados"
    
def get_dados_pagadores():
    return Pagador.choices

def get_dados_tipos_titulo():
    return TipoTitulo.choices

def get_dados_origens():
    return Origem.choices

def get_dados_formas_contato():
    try:
        return FormaContato.objects.all()
    except FormaContato.DoesNotExist:
        return "Formas de contato não encontrados"
    
def get_dados_supervisores():
    try:
        return Supervisor.objects.all()
    except Supervisor.DoesNotExist:
        return "Supervisor não encontrados"
    
def get_dados_operadores():
    try:
        return Operador.objects.all()
    except Operador.DoesNotExist:
        return "Operador não encontrados"
    
def create_titulo(request, params):
    try:
        cedente = Cedente.objects.get(nome=params['cedente'])
    except Cedente.DoesNotExist:
        cedente = Cedente.objects.create(
            nome=params['cedente']
        )

    try:
        sacado = Sacado.objects.get(nome=params['sacado'])
    except Sacado.DoesNotExist:
        sacado = Sacado.objects.create(
            nome=params['sacado']
        )

    try:
        situacao = Situacao.objects.filter(descricao="EM ABERTO").first()
    except Situacao.DoesNotExist:
        situacao = Situacao.objects.create(
            descricao="EM ABERTO"
        )

    try:
        forma_contato = FormaContato.objects.get(descricao=params['forma_contato'])
    except FormaContato.DoesNotExist:
        forma_contato = FormaContato.objects.create(
            descricao=params['forma_contato']
        )

    usuario = User.objects.get(username=request.session['user'])

    try:
        Titulo.objects.create(
            cedente=cedente,
            sacado=sacado,
            cpf_cnpj=params['cpf_cnpj'],
            valor=params['valor'],
            contato=params['contato'],
            pagador=params['pagador'],
            situacao=situacao,
            forma_contato=forma_contato,
            data_vencimento=params['data_vencimento'],
            tipo=params['tipo'],
            origem=params['origem'],
            usuario=usuario
        )
        return True
    except Exception as err:
        print(err)
        return err
    
def create_arquivo(filename):
    Arquivo.objects.create(
        file=filename
    )

def get_dados_titulos_em_aberto():
    situacoes = Situacao.objects.filter(descricao__in=['EM ABERTO', 'ARQUIVO', 'EM ABERTO - PRIORIDADE'])
    return Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes]).order_by('data_vencimento')

def get_dados_situacoes():
    return Situacao.objects.all()

def get_dados_template_whatsapp():
    return TemplateWhatsapp.objects.first()

def get_dados_links():
    return Link.objects.all()

def update_titulo(request):
    situacao = Situacao.objects.get(descricao=request.POST['situacao'])

    try:
        forma_contato = FormaContato.objects.get(descricao=request.POST['forma_contato'])
    except FormaContato.DoesNotExist:
        forma_contato = FormaContato.objects.create(
            descricao=request.POST['forma_contato']
        )

    titulo = Titulo.objects.get(pk=request.POST['titulo_id'])
    titulo.situacao = situacao
    titulo.forma_contato = forma_contato

    if len(request.POST['supervisor']) > 0:
        supervisor = Supervisor.objects.get(nome=request.POST['supervisor'])
        titulo.supervisor = supervisor
    else:
        titulo.supervisor = None

    if len(request.POST['operador']) > 0:
        operador = Operador.objects.get(nome=request.POST['operador'])
        titulo.operador = operador
    else:
        titulo.operador = None

    titulo.contato = request.POST['contato']
    titulo.contato_secundario = request.POST['contato_secundario']
    if len(request.POST['data_pagamento']) > 0:
        titulo.data_pagamento = request.POST['data_pagamento']
    else:
        titulo.data_pagamento = None

    if len(request.POST['data_vencimento']) > 0:
        titulo.data_vencimento = request.POST['data_vencimento']
    else:
        titulo.data_vencimento = None

    if len(request.POST['valor_encargo']) > 0:
        titulo.valor_face = titulo.valor - float(str(request.POST['valor_encargo']).replace(',', '.'))
        titulo.encargo = float(str(request.POST['valor_encargo']).replace(',', '.'))
    else:
        titulo.encargo = 0

    titulo.save()
    
    if "anexo" in request.FILES:
        anexo = request.FILES['anexo']
        fs = FileSystemStorage()
        filename = fs.save(anexo.name, anexo)
        
        Anexo.objects.create(
            titulo=titulo,
            descricao=filename,
            arquivo=anexo
        )

def update_pagamento(request):
    situacao = Situacao.objects.get(descricao=request.POST['situacao'])

    titulo = Titulo.objects.get(pk=request.POST['pagamento_id'])
    titulo.situacao = situacao
    if len(request.POST['data_pagamento']) > 0:
        titulo.data_pagamento = request.POST['data_pagamento']
    else:
        titulo.data_pagamento = None

    if 'data_vencimento' in request.POST and len(request.POST['data_vencimento']) > 0:
        titulo.data_vencimento = request.POST['data_vencimento']
    else:
        titulo.data_vencimento = None

    if len(request.POST['valor_encargo']) > 0:
        titulo.valor_face = titulo.valor - float(str(request.POST['valor_encargo']).replace(',', '.'))
        titulo.encargo = float(str(request.POST['valor_encargo']).replace(',', '.'))

    titulo.save()

def update_observacoes(request):
    titulo = Titulo.objects.get(pk=request.POST['titulo_id'])

    observacoes = Observacao.objects.filter(titulo_id=titulo.id).all()
    
    if "observacao" in request.POST and len(request.POST['observacao']) > 0:
        descricao = request.POST['observacao']
        Observacao.objects.create(
            titulo=titulo,
            descricao=descricao
        )

    for observacao in observacoes:
        if f'observacao_{observacao.id}' in request.POST:
            if len(request.POST[f'observacao_{observacao.id}']) == 0:
                observacao.delete()
            else:
                observacao.descricao = request.POST[f'observacao_{observacao.id}']
                observacao.save()

def create_pagamento_parcial(request, is_acordo):
    if "data_pagamento" in request.POST and len(request.POST['data_pagamento']) > 0 and "valor_pagamento" in request.POST and len(request.POST['valor_pagamento']) > 0 :
        data_pagamento = str(request.POST['data_pagamento'])
        valor_pagamento = float(str(request.POST['valor_pagamento']).replace(',', '.'))

        descricao = 'PAGO'
        if is_acordo:
            descricao = 'ACORDO PAGO'

        try:
            situacao = Situacao.objects.get(descricao=descricao)
        except Situacao.DoesNotExist:
            situacao = Situacao.objects.create(
                descricao="EM ABERTO"
            )

        titulo = Titulo.objects.get(pk=request.POST['titulo_id'])
        valor_original = titulo.valor
        
        titulo_parcial = Titulo.objects.get(pk=request.POST['titulo_id'])
        titulo_parcial.pk = None

        if 'pagador' in request.POST and len(request.POST['pagador']) > 0:
            titulo_parcial.pagador = request.POST['pagador']

        titulo_parcial.situacao = situacao
        titulo_parcial.data_pagamento = data_pagamento
        titulo_parcial.valor = valor_pagamento
        titulo_parcial.encargo = 0
        titulo_parcial.valor_face = titulo_parcial.valor
        titulo_parcial.save()

        titulo.valor = valor_original - valor_pagamento

        if titulo.encargo:
            titulo.valor_face = titulo.valor - titulo.encargo
        titulo.save()

def get_dados_titulo_anexos(titulo_id):
    return Anexo.objects.filter(titulo_id=titulo_id).all()

def get_dados_titulo_observacoes(titulo_id):
    return Observacao.objects.filter(titulo_id=titulo_id).all()

def get_dados_pagamentos(data_inicial, data_final):
    situacoes = Situacao.objects.filter(descricao__in=['PAGO', 'ACORDO PAGO'])
    titulos = Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes], data_pagamento__gte=data_inicial, data_pagamento__lte=data_final).order_by('-data_pagamento') | Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes], data_pagamento=None).order_by('-data_pagamento')
    return titulos

def get_dados_acordos(data_inicial, data_final):
    situacoes = Situacao.objects.filter(descricao__in=['ACORDO EM ABERTO'])
    titulos = Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes], data_vencimento__gte=data_inicial, data_vencimento__lte=data_final).order_by('data_vencimento') | Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes], data_vencimento=None).order_by('data_vencimento')
    return titulos

def get_dados_juridico_externo(data_inicial, data_final):
    situacoes = Situacao.objects.filter(descricao__in=['JURIDICO EXTERNO'])
    titulos = Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes], data_vencimento__gte=data_inicial, data_vencimento__lte=data_final).order_by('data_vencimento') | Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes], data_vencimento=None).order_by('data_vencimento')
    return titulos