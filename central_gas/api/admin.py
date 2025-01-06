from django.contrib import admin
from .models.empresa import Empresa
from .models.cliente import Cliente
from .models.pedido import Pedido
from .models.produto import Produto, PrecoProdutoEmpresa
from .models.endereco import Endereco
from .models.user import CustomUser
from django.contrib.auth.admin import UserAdmin

# Admin para Endereço
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['id', 'rua', 'numero', 'cidade', 'estado']
    search_fields = ['rua', 'cidade', 'estado']
    list_filter = ['cidade', 'estado']



class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'get_telefone', 'endereco']
    search_fields = ['nome_completo', 'user__telefone']  # Considerando que 'telefone' está no CustomUser
    list_filter = ['endereco__cidade']

    def get_telefone(self, obj):
        return obj.user.telefone  # Acessa o telefone do CustomUser
    get_telefone.short_description = 'Telefone'


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'mostrar_telefone', 'listar_endereco']
    search_fields = ['nome', 'telefone']
    list_filter = ['endereco__cidade']  # Relacionamento direto com cidade no endereço

    def mostrar_telefone(self, obj):
        return obj.user.telefone  # Exibe o telefone da empresa
    mostrar_telefone.short_description = "Telefone"

    def listar_endereco(self, obj):
        return f"{obj.endereco.rua}, {obj.endereco.numero} - {obj.endereco.cidade}, {obj.endereco.estado}" if obj.endereco else "Sem endereço"
    listar_endereco.short_description = "Endereço"


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
    list_display = ['empresa', 'produto', 'preco', 'descricao_empresa_produto']
    search_fields = ['empresa__nome', 'produto__nome']
    list_filter = ['empresa', 'produto']  # Filtros laterais
    ordering = ['empresa', 'produto']  # Ordenação padrão
    autocomplete_fields = ['empresa', 'produto']  # Facilita seleção no formulário

    def descricao_empresa_produto(self, obj):
        # Exibe a descrição de forma mais clara
        return f"{obj.empresa.nome} - {obj.produto.nome} | Preço: {obj.preco}"
    descricao_empresa_produto.short_description = "Empresa e Produto"
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['telefone', 'tipo', 'is_active', 'is_staff', 'is_superuser', "codigo_verificacao", "codigo_recuperacao"]
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['telefone', 'tipo']
    ordering = ['telefone']

    fieldsets = (
        (None, {'fields': ('telefone', 'tipo', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telefone', 'tipo', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.save()

# Registra o modelo CustomUser no Django Admin
admin.site.register(CustomUser, CustomUserAdmin)


# Registro dos modelos no admin
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PrecoProdutoEmpresa, PrecoProdutoEmpresaAdmin)
