# Generated by Django 4.2.6 on 2024-01-03 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_destinateur_nom_transaction_destinataire_nom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='numero_telephone',
            field=models.CharField(max_length=15),
        ),
    ]