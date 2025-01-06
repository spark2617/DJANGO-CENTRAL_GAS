from rest_framework import serializers
from api.models.cliente import Cliente
from api.models.endereco import Endereco
from api.serializers.endereco_serializer import EnderecoSerializer


class ClienteSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()

    class Meta:
        model = Cliente
        fields = ["nome_completo", "endereco"]

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco', None)
        if endereco_data:
            endereco = Endereco.objects.create(**endereco_data)
            validated_data['endereco'] = endereco
        cliente = Cliente.objects.create(**validated_data)
        return cliente

    def update(self, instance, validated_data):
        instance.nome_completo = validated_data.get('nome_completo', instance.nome_completo)
        instance.telefone = validated_data.get('telefone', instance.telefone)
        instance.save()

        endereco_data = validated_data.get('endereco')
        if endereco_data:
            endereco = instance.endereco
            for attr, value in endereco_data.items():
                setattr(endereco, attr, value)
            endereco.save()

        return instance
