# Generated by Django 4.2.7 on 2023-12-02 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_anexo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cedente',
            name='contato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sacado',
            name='contato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
