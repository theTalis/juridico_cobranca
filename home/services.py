from .repository import *
from .validators import *
import re

def get_cedentes():
    return get_dados_cedentes()

def get_sacados():
    return get_dados_sacados()

def get_pagadores():
    return get_dados_pagadores()

def get_tipos_titulo():
    return get_dados_tipos_titulo()

def get_origens():
    return get_dados_origens()

def get_formas_contato():
    return get_dados_formas_contato()

def get_erros_cadastro(request):
    forma_contato = request.POST['forma_contato']
    contato = request.POST['contato']
    data_vencimento = request.POST['data_vencimento']

    erros = []
    if forma_contato == "E-mail":
        if not is_valid_email(contato):
            erros.append("E-mail inválido")

    if not is_valid_date(data_vencimento):
        erros.append("Data de vencimento inválida")

    if len(erros) > 0:
        return erros
    return None

def set_titulo(request):
    params = request.POST
    return create_titulo(request, params)

def upset_titulo(request):
    return update_titulo(request)

def set_arquivo(filename):
    return create_arquivo(filename)

def import_titulo(request, dados):
    return create_titulo(request, dados)

def get_titulos_em_aberto():
    return get_dados_titulos_em_aberto()

def get_situacoes():
    return get_dados_situacoes()

def get_whatsapp(nome, telefone):
    template = get_dados_template_whatsapp()

    telefone = str(int(''.join(filter(str.isdigit, f'55{telefone}'))))
    link_whatsapp = template.conteudo.replace('NOME', nome)
    link_whatsapp = link_whatsapp.replace('TELEFONE', telefone)
    return link_whatsapp

def get_links():
    return get_dados_links()

def get_titulo_anexos(titulo_id):
    return get_dados_titulo_anexos(titulo_id)

def get_titulo_observacoes(titulo_id):
    return get_dados_titulo_observacoes(titulo_id)

def get_pagamentos():
    return get_dados_pagamentos()

def get_acordos():
    return get_dados_acordos()

def get_juridico_externo():
    return get_dados_juridico_externo()

def get_cedentes():
    return get_dados_cedentes()

def get_sacados():
    return get_dados_sacados()