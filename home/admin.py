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
    search_fields = ('cedente', 'sacado', 'valor' )
    list_per_page = 30
    ordering = ('valor',)
    fields = ('cedente', 'sacado', 'valor', 'contato', 'pagador', 'situacao', 'forma_contato',
        'observacao', 'usuario', )
    
admin.site.register(Titulo, ListandoTitulos)


class ListandoAnexos(admin.ModelAdmin):
    list_display = ('titulo', 'descricao',)
    list_display_links = ('titulo', 'descricao', )
    search_fields = ('titulo', 'descricao', )
    list_per_page = 30
    ordering = ('titulo', 'descricao',)
    fields = ('titulo', 'descricao', 'arquivo' )
    
admin.site.register(Anexo, ListandoAnexos)
