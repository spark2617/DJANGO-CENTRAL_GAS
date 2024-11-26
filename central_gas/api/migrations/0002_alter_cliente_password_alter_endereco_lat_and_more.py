# Generated by Django 5.1.2 on 2024-11-23 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$gTDIQIBRUiaQrAjpNTE3gx$6XL1AUXA4gCckxgFvISqfAEz106FEz9Aedb5c6X8A9g=', max_length=200),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='lat',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='lon',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]