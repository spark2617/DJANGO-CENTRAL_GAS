from rest_framework import serializers
from api.serializers.endereco_serializer import EnderecoSerializer
from api.models.empresa import Empresa
from api.models.endereco import Endereco

class EmpresaSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()

    class Meta:
        model = Empresa
        fields = [
            "nome",
            "telefone",
            "numero_licenca",
            "email",
            "nome_fantasia",
            "razao_social",
            "empresa_apresentada",
            "imagem_contrato_social",
            "logo",
            "endereco",
        ]

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco', None)
        if endereco_data:
            endereco = Endereco.objects.create(**endereco_data)
            validated_data['endereco'] = endereco
        empresa = Empresa.objects.create(**validated_data)
        return empresa

    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.telefone = validated_data.get('telefone', instance.telefone)
        instance.numero_licenca = validated_data.get('numero_licenca', instance.numero_licenca)
        instance.email = validated_data.get('email', instance.email)
        instance.nome_fantasia = validated_data.get('nome_fantasia', instance.nome_fantasia)
        instance.razao_social = validated_data.get('razao_social', instance.razao_social)
        instance.empresa_apresentada = validated_data.get('empresa_apresentada', instance.empresa_apresentada)
        instance.imagem_contrato_social = validated_data.get(
            'imagem_contrato_social', instance.imagem_contrato_social
        )
        instance.logo = validated_data.get('logo', instance.logo)
        instance.save()

        endereco_data = validated_data.get('endereco')
        if endereco_data:
            endereco = instance.endereco
            for attr, value in endereco_data.items():
                setattr(endereco, attr, value)
            endereco.save()

        return instance
