# Generated by Django 5.1.2 on 2024-11-23 19:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=100)),
                ('bairro', models.CharField(max_length=100)),
                ('rua', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=10)),
                ('tipo_moradia', models.CharField(max_length=50)),
                ('lat', models.CharField(max_length=100, null=True)),
                ('lon', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao_padrao', models.TextField(default='Descrição padrão')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('telefone_secundario', models.CharField(blank=True, max_length=15, null=True)),
                ('numero_licenca', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('nome_fantasia', models.CharField(blank=True, max_length=100, null=True)),
                ('razao_social', models.CharField(blank=True, max_length=200, null=True)),
                ('imagem_contrato_social', models.ImageField(blank=True, null=True, upload_to='contratos_sociais/')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo_empresas/')),
                ('endereco', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa', to='api.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nome_completo', models.CharField(max_length=200)),
                ('telefone', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(default='pbkdf2_sha256$870000$TCDx4HqgvhSarp6o566OJU$ktKQAtAUR1Z7ff27mx5bS+Zf3HxI0H89qZJyThOnSBY=', max_length=200)),
                ('codigo_verificacao', models.CharField(blank=True, max_length=5, null=True)),
                ('codigo_recuperacao', models.CharField(blank=True, max_length=5, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('endereco', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.endereco')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrecoProdutoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descricao_personalizada', models.TextField(blank=True, null=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='precos', to='api.empresa')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='precos', to='api.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pedido', models.DateTimeField(auto_now_add=True)),
                ('expectativa', models.DateTimeField(blank=True, null=True)),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.produto')),
            ],
        ),
    ]
