# Generated by Django 4.2.3 on 2023-07-21 14:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_vagas", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="candidatura",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="experiencia",
            field=models.CharField(
                choices=[
                    ("Até 1 ano", "Até 1 ano"),
                    ("De 1 ano a 2 anos", "De 1 ano a 2 anos"),
                    ("De 2 anos a 3 anos", "De 2 anos a 3 anos"),
                    ("Acima de 3 anos", "Acima de 3 anos"),
                ],
                default="Até 1 ano",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="pretensao_salario",
            field=models.CharField(
                choices=[
                    ("Até 1000", "Até 1000"),
                    ("De 1000 a 2000", "De 1000 a 2000"),
                    ("De 2000 a 3000", "De 2000 a 3000"),
                    ("Acima de 3000", "Acima de 3000"),
                ],
                default="Até 1000",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="ultima_escolaridade",
            field=models.CharField(
                choices=[
                    ("Ensino fundamental", "Ensino fundamental"),
                    ("Ensino médio", "Ensino médio"),
                    ("Tecnólogo", "Tecnólogo"),
                    ("Ensino Superior", "Ensino Superior"),
                    ("Pós / MBA / Mestrado", "Pós / MBA / Mestrado"),
                    ("Doutorado", "Doutorado"),
                ],
                default="Ensino fundamental",
                max_length=50,
            ),
        ),
        migrations.RemoveField(
            model_name="candidatura",
            name="data_candidatura",
        ),
    ]
