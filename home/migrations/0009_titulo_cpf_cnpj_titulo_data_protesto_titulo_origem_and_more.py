# Generated by Django 4.2.7 on 2023-12-13 23:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0008_remove_templatewhatsapp_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="titulo",
            name="cpf_cnpj",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="titulo",
            name="data_protesto",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="titulo",
            name="origem",
            field=models.CharField(
                blank=True,
                choices=[("SEC", "Secutirizadora"), ("FIDC", "Fidc")],
                default="SEC",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="titulo",
            name="tipo",
            field=models.CharField(
                blank=True,
                choices=[("DUPLICATA", "Duplicata"), ("CHEQUE", "Cheque")],
                default="DUPLICATA",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="titulo",
            name="pagador",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CEDENTE", "Cedente"),
                    ("SACADO", "Sacado"),
                    ("CEDENTE_SACADO", "Cedente/Sacado"),
                ],
                default="CEDENTE",
                max_length=20,
                null=True,
            ),
        ),
    ]
