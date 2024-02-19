from django.contrib import admin
from .models import *

class ListandoCedentes(admin.ModelAdmin):
    list_display = ('id', 'nome', 'contato')
    list_display_links = ('id', 'nome')
    search_fields = ('nome', 'contato', )
    list_per_page = 30
    ordering = ('nome',)
    fields = ('nome', 'contato', )    
admin.site.register(Cedente, ListandoCedentes)

class ListandoSacados(admin.ModelAdmin):
    list_display = ('id', 'nome', 'contato')
    list_display_links = ('id', 'nome')
    search_fields = ('nome', 'contato', )
    list_per_page = 30
    ordering = ('nome',)
    fields = ('nome', 'contato', )    
admin.site.register(Sacado, ListandoSacados)

class ListandoSupervisores(admin.ModelAdmin):
    list_display = ('id', 'nome', )
    list_display_links = ('id', 'nome')
    search_fields = ('nome', )
    list_per_page = 30
    ordering = ('nome',)
    fields = ('nome', )    
admin.site.register(Supervisor, ListandoSupervisores)

class ListandoOperadores(admin.ModelAdmin):
    list_display = ('id', 'nome', )
    list_display_links = ('id', 'nome')
    search_fields = ('nome', )
    list_per_page = 30
    ordering = ('nome',)
    fields = ('nome', )    
admin.site.register(Operador, ListandoOperadores)

class ListandoSituacoes(admin.ModelAdmin):
    list_display = ('descricao', )
    list_display_links = ('descricao', )
    search_fields = ('descricao', )
    list_per_page = 30
    ordering = ('descricao',)
    fields = ('descricao', )    
admin.site.register(Situacao, ListandoSituacoes)

class ListandoFormasContato(admin.ModelAdmin):
    list_display = ('descricao', )
    list_display_links = ('descricao', )
    search_fields = ('descricao', )
    list_per_page = 30
    ordering = ('descricao',)
    fields = ('descricao', )    
admin.site.register(FormaContato, ListandoFormasContato)

class ListandoTitulos(admin.ModelAdmin):
    list_display = ('cedente', 'sacado', 'valor')
    list_display_links = ('cedente', 'sacado', 'valor' )
    search_fields = ('cedente__nome', 'sacado__nome')
    list_per_page = 30
    ordering = ('valor',)
    fields = ('cedente', 'sacado', 'supervisor', 'operador', 'valor', 'valor_face', 'encargo', 'contato', 'contato_secundario', 'pagador', 'situacao', 'forma_contato', 'marcado',
        'data_vencimento', 'data_pagamento', 'usuario', )    
admin.site.register(Titulo, ListandoTitulos)

class ListandoAnexos(admin.ModelAdmin):
    list_display = ('titulo', 'descricao',)
    list_display_links = ('titulo', 'descricao', )
    search_fields = ('titulo', 'descricao', )
    list_per_page = 30
    ordering = ('titulo', 'descricao',)
    fields = ('titulo', 'descricao', 'arquivo' )    
admin.site.register(Anexo, ListandoAnexos)

class ListandoObservacoes(admin.ModelAdmin):
    list_display = ('titulo', 'descricao',)
    list_display_links = ('titulo', 'descricao', )
    search_fields = ('titulo', 'descricao', )
    list_per_page = 30
    ordering = ('titulo', 'descricao',)
    fields = ('titulo', 'descricao', )    
admin.site.register(Observacao, ListandoObservacoes)

class ListandoArquivos(admin.ModelAdmin):
    list_display = ('file',)
    list_display_links = ('file', )
    search_fields = ('file', )
    list_per_page = 30
    ordering = ('file',)
    fields = ('file',)
admin.site.register(Arquivo, ListandoArquivos)

class ListandoTemplatesWhatsapp(admin.ModelAdmin):
    list_display = ('conteudo',)
    list_display_links = ('conteudo', )
    search_fields = ('conteudo', )
    list_per_page = 30
    ordering = ('conteudo',)
    fields = ('conteudo', )
admin.site.register(TemplateWhatsapp, ListandoTemplatesWhatsapp)

class ListandoLinks(admin.ModelAdmin):
    list_display = ('titulo', 'link', )
    list_display_links = ('titulo', )
    search_fields = ('titulo', )
    list_per_page = 30
    ordering = ('titulo',)
    fields = ('titulo', 'link', )
admin.site.register(Link, ListandoLinks)