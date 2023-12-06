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
            valor=params['valor'],
            contato=params['contato'],
            pagador=params['pagador'],
            situacao=situacao,
            forma_contato=forma_contato,
            observacao=params['observacao'],
            data_vencimento=params['data_vencimento'],
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

def get_dados_titulos():
    return Titulo.objects.all()

def get_dados_situacoes():
    return Situacao.objects.all()

def get_dados_template_whatsapp():
    return TemplateWhatsapp.objects.first()

def get_dados_links():
    return Link.objects.all()

def update_titulo(request):
    situacao = Situacao.objects.get(descricao=request.POST['situacao'])

    titulo = Titulo.objects.get(pk=request.POST['titulo_id'])
    titulo.situacao = situacao
    titulo.data_pagamento = request.POST['data_pagamento']
    titulo.data_vencimento = request.POST['data_vencimento']
    titulo.observacao = request.POST['observacao']
    titulo.save()
    
    anexo = request.FILES['anexo']
    fs = FileSystemStorage()
    filename = fs.save(anexo.name, anexo)
    
    Anexo.objects.create(
        titulo=titulo,
        descricao=filename,
        arquivo=anexo
    )

def get_dados_titulo_anexos(titulo_id):
    return Anexo.objects.filter(titulo_id=titulo_id).all()

def get_dados_pagamentos():
    situacao = Situacao.objects.get(descricao='PAGO')
    return Titulo.objects.filter(situacao=situacao).order_by('-updated_at')