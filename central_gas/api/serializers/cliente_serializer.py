from rest_framework import serializers
from api.models.cliente import Cliente
from api.models.endereco import Endereco
from api.serializers.endereco_serializer import EnderecoSerializer

class ClienteSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()

    class Meta:
        model = Cliente
        fields = ["nome_completo", "telefone", "endereco"]

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        endereco = Endereco.objects.create(**endereco_data)
        cliente = Cliente.objects.create(endereco=endereco, **validated_data)
        return cliente
    
    def update(self, instance, validated_data):

        instance.nome_completo = validated_data.get('nome_completo', instance.nome_completo)
        instance.telefone = validated_data.get('telefone', instance.telefone)
        instance.save()


        endereco_data = validated_data.get('endereco')
        if endereco_data:
            endereco = instance.endereco
            endereco.cidade = endereco_data.get('cidade', endereco.cidade)
            endereco.estado = endereco_data.get('estado', endereco.estado)
            endereco.bairro = endereco_data.get('bairro', endereco.bairro)
            endereco.rua = endereco_data.get('rua', endereco.rua)
            endereco.numero = endereco_data.get('numero', endereco.numero)
            endereco.tipo_moradia = endereco_data.get('tipo_moradia', endereco.tipo_moradia)
            endereco.save()

        return instance