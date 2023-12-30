# Generated by Django 4.2.7 on 2023-12-29 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0009_titulo_cpf_cnpj_titulo_data_protesto_titulo_origem_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="titulo",
            name="observacao",
        ),
        migrations.CreateModel(
            name="Observacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("observacao", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "titulo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.titulo"
                    ),
                ),
            ],
            options={
                "db_table": "observacao",
            },
        ),
    ]