# Generated by Django 4.2.7 on 2024-02-17 12:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0013_titulo_marcado"),
    ]

    operations = [
        migrations.AddField(
            model_name="titulo",
            name="encargo",
            field=models.FloatField(blank=True, null=True),
        ),
    ]