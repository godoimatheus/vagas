# pylint: disable=C0103
# Generated by Django 4.2.3 on 2023-08-01 02:04
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app_vagas", "0003_candidatura_pontuacao"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Candidatura",
        ),
    ]