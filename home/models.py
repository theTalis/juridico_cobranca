from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()

class Cedente(models.Model):
    class Meta:
        db_table = 'cedente'
    nome = models.CharField(max_length=60)
    contato = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.nome

class Sacado(models.Model):
    class Meta:
        db_table = 'sacado'
    nome = models.CharField(max_length=60)
    contato = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.nome

class Pagador(models.TextChoices):
    CEDENTE = 'CEDENTE', _('Cedente')
    SACADO = 'SACADO', _('Sacado')
    CEDENTE_SACADO = 'CEDENTE_SACADO', _('Cedente/Sacado')

class TipoTitulo(models.TextChoices):
    DUPLICATA = 'DUPLICATA', _('Duplicata')
    CHEQUE = 'CHEQUE', _('Cheque')

class Origem(models.TextChoices):
    SEC = 'SEC', _('Secutirizadora')
    FIDC = 'FIDC', _('Fidc')

class Situacao(models.Model):
    class Meta:
        db_table = 'situacao'
    descricao = models.CharField(max_length=60, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.descricao

class FormaContato(models.Model):
    class Meta:
        db_table = 'formacontato'
    descricao = models.CharField(max_length=60, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.descricao

class Titulo(models.Model):
    class Meta:
        db_table = 'titulo'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, blank=True)
    cedente = models.ForeignKey(Cedente, on_delete=models.CASCADE)
    sacado = models.ForeignKey(Sacado, on_delete=models.CASCADE)
    cpf_cnpj = models.CharField(max_length=30, null=True, blank=True)
    valor = models.FloatField(null=True, blank=True)
    contato = models.CharField(max_length=100, null=True, blank=True)
    pagador = models.CharField(choices=Pagador.choices, default=Pagador.CEDENTE, max_length=20, null=True, blank=True)
    situacao = models.ForeignKey(Situacao, on_delete=models.CASCADE, null=True, blank=True)
    forma_contato = models.ForeignKey(FormaContato, on_delete=models.CASCADE, null=True, blank=True)
    data_vencimento = models.DateField(null=True, blank=True)
    data_protesto = models.DateField(null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    tipo = models.CharField(choices=TipoTitulo.choices, default=TipoTitulo.DUPLICATA, max_length=20, null=True, blank=True)
    origem = models.CharField(choices=Origem.choices, default=Origem.SEC, max_length=20, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.cedente} - {self.sacado} / {self.valor}'

class Observacao(models.Model):
    class Meta:
        db_table = 'observacao'
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    descricao = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.titulo} - {self.created_at}'

class Anexo(models.Model):
    class Meta:
        db_table = 'anexo'
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=60, null=True, blank=True)
    arquivo = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.titulo} - {self.created_at}'

class Arquivo(models.Model):
    class Meta:
        db_table = 'arquivo'
    file = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.file}'
    
class TemplateWhatsapp(models.Model):
    class Meta:
        db_table = 'templatewhatsapp'
    conteudo = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.conteudo}'

class Link(models.Model):
    class Meta:
        db_table = 'link'
    titulo = models.CharField(max_length=100)
    link = models.CharField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.titulo}'
