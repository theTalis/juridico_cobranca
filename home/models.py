from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Cedente(models.Model):
    class Meta:
        db_table = 'cedente'
    nome = models.CharField(max_length=60)
    contato = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Sacado(models.Model):
    class Meta:
        db_table = 'sacado'
    nome = models.CharField(max_length=60)
    contato = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Pagador(models.TextChoices):
    CEDENTE = 'CEDENTE', _('Cedente')
    SACADO = 'SACADO', _('Sacado')

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
    cedente = models.ForeignKey(Cedente, on_delete=models.CASCADE)
    sacado = models.ForeignKey(Sacado, on_delete=models.CASCADE)
    valor = models.FloatField(null=True, blank=True)
    contato = models.CharField(max_length=100, null=True, blank=True)
    pagador = models.CharField(choices=Pagador.choices, default=Pagador.CEDENTE, max_length=10, null=True, blank=True)
    situacao = models.ForeignKey(Situacao, on_delete=models.CASCADE, null=True, blank=True)
    forma_contato = models.ForeignKey(FormaContato, on_delete=models.CASCADE, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.cedente} - {self.sacado} / {self.valor}'
