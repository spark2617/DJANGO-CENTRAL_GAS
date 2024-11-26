from django.contrib import admin
from .models.empresa import Empresa
from .models.cliente import Cliente
from .models.pedido import Pedido
from .models.produto import Produto, PrecoProdutoEmpresa
from .models.endereco import Endereco


# Admin para Endereço
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['id', 'rua', 'numero', 'cidade', 'estado']
    search_fields = ['rua', 'cidade', 'estado']
    list_filter = ['cidade', 'estado']


# Admin para Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'telefone', 'endereco']
    search_fields = ['nome_completo', 'telefone']
    list_filter = ['endereco__cidade']  # Relacionamento direto com cidade no endereço


# Admin para Empresa
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'endereco']
    search_fields = ['nome', 'telefone']
    list_filter = ['endereco__cidade']  # Relacionamento direto com cidade no endereço


# Admin para Produto
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'listar_empresas']
    search_fields = ['nome']
    list_filter = ['nome']  # Remove a relação ManyToMany

    def listar_empresas(self, obj):
        # Obtém as empresas associadas ao produto por meio de PrecoProdutoEmpresa
        empresas = obj.precos.values_list('empresa__nome', flat=True)
        return ", ".join(empresas) if empresas else "Nenhuma empresa associada"
    listar_empresas.short_description = 'Empresas'


# Admin para Pedido
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'produto', 'data_pedido', 'quantidade']
    search_fields = ['cliente__nome_completo', 'produto__nome']
    list_filter = ['produto__nome', 'cliente__nome_completo']  # Campos relacionais diretos


# Admin para PrecoProdutoEmpresa
class PrecoProdutoEmpresaAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'produto', 'preco', 'descricao']
    search_fields = ['empresa__nome', 'produto__nome']
    list_filter = ['empresa', 'produto']  # Filtros laterais
    ordering = ['empresa', 'produto']  # Ordenação padrão
    autocomplete_fields = ['empresa', 'produto']  # Facilita seleção no formulário

    def descricao_empresa_produto(self, obj):
        # Exibe a descrição de forma mais clara
        return f"{obj.empresa.nome} - {obj.produto.nome}"
    descricao_empresa_produto.short_description = "Empresa e Produto"


# Registro dos modelos no admin
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PrecoProdutoEmpresa, PrecoProdutoEmpresaAdmin)
