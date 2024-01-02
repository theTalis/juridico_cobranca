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
        situacao = Situacao.objects.get(descricao="EM ABERTO")
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
            contato_secundario=params['contato_secundario'],
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
    return Titulo.objects.filter(data_pagamento=None).order_by("data_vencimento").all()

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
    titulo.contato = request.POST['contato']
    titulo.contato_secundario = request.POST['contato_secundario']
    if len(request.POST['data_pagamento']) > 0:
        titulo.data_pagamento = request.POST['data_pagamento']
    if len(request.POST['data_vencimento']) > 0:
        titulo.data_vencimento = request.POST['data_vencimento']
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

def get_dados_titulo_anexos(titulo_id):
    return Anexo.objects.filter(titulo_id=titulo_id).all()

def get_dados_titulo_observacoes(titulo_id):
    return Observacao.objects.filter(titulo_id=titulo_id).all()

def get_dados_pagamentos(data_inicial, data_final):
    situacoes = Situacao.objects.filter(descricao__in=['PAGO', 'ACORDO PAGO'])
    return Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes], data_pagamento__gte=data_inicial, data_pagamento__lte=data_final).order_by('-updated_at')

def get_dados_acordos(data_inicial, data_final):
    situacoes = Situacao.objects.filter(descricao__in=['ACORDO EM ABERTO'])
    return Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes], data_vencimento__gte=data_inicial, data_vencimento__lte=data_final).order_by('-updated_at')

def get_dados_juridico_externo(data_inicial, data_final):
    situacoes = Situacao.objects.filter(descricao__in=['JURIDICO EXTERNO'])
    return Titulo.objects.filter(situacao__in=[situacao.descricao for situacao in situacoes], data_vencimento__gte=data_inicial, data_vencimento__lte=data_final).order_by('-updated_at')