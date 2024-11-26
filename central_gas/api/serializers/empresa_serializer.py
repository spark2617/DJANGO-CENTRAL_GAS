from rest_framework import serializers
from api.serializers.endereco_serializer import EnderecoSerializer
from api.serializers.produto_serializer import ProdutoSerializer
from api.models.empresa import Empresa
from api.models.endereco import Endereco

class EmpresaSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    produtos = ProdutoSerializer(many=True, read_only=True)

    class Meta:
        model = Empresa
        fields = "__all__"

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        endereco = Endereco.objects.create(**endereco_data)
        empresa = Empresa.objects.create(endereco=endereco, **validated_data)
        return empresa

    def update(self, instance, validated_data):
        endereco_data = validated_data.pop('endereco', None)

        instance.nome = validated_data.get('nome', instance.nome)
        instance.save()


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