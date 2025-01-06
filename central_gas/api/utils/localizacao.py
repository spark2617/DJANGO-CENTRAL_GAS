from ..models import Empresa, Cliente, Produto, CustomUser
from api.models.produto import PrecoProdutoEmpresa
from geopy.distance import geodesic


def buscar_empresa_com_produtos_proximas(token, lista_produtos):
    try:
        # Decodificando o token para pegar o cliente
        user = CustomUser.objects.get(auth_token=token)
        cliente = user.cliente
    except CustomUser.DoesNotExist:
        return {"error": "Cliente não encontrado"}

    coordenadas_cliente = (float(cliente.endereco.lat), float(cliente.endereco.lon))

    # Transformar lista de produtos em um dicionário com produto_id: quantidade
    produtos_restantes = {produto['id']: produto['quantidade'] for produto in lista_produtos}
    produtos_resultado = []

    while produtos_restantes:
        # Tentar buscar empresas não apresentadas primeiro
        empresas = Empresa.objects.filter(
            endereco__cidade=cliente.endereco.cidade, empresa_apresentada=False
        )

        # Se nenhuma empresa não apresentada estiver disponível, considerar todas as empresas da cidade
        if not empresas.exists():
            empresas = Empresa.objects.filter(endereco__cidade=cliente.endereco.cidade)
            empresas.update(empresa_apresentada=False)

        # Se nenhuma empresa for encontrada na cidade, encerrar a busca
        if not empresas.exists():
            return {
                "error": "Não há empresas disponíveis na cidade.",
                "produtos_nao_encontrados": list(produtos_restantes.keys()),
            }

        menor_distancia = None
        empresa_mais_proxima = None
        produtos_encontrados_na_empresa = []

        for empresa in empresas:
            coordenadas_empresa = (float(empresa.endereco.lat), float(empresa.endereco.lon))
            distancia = geodesic(coordenadas_cliente, coordenadas_empresa).km

            # Obter produtos disponíveis com preços definidos para a empresa
            produtos_com_precos = PrecoProdutoEmpresa.objects.filter(
                empresa=empresa, produto__id__in=produtos_restantes.keys()
            )

            if produtos_com_precos and (menor_distancia is None or distancia < menor_distancia):
                menor_distancia = distancia
                empresa_mais_proxima = empresa
                produtos_encontrados_na_empresa = produtos_com_precos

        if empresa_mais_proxima:
            # Adicionar os produtos encontrados ao resultado final
            for preco_produto in produtos_encontrados_na_empresa:
                produto_id = preco_produto.produto.id
                quantidade = produtos_restantes[produto_id]

                produtos_resultado.append({
                    "produto_id":produto_id,
                    "produto_nome": preco_produto.produto.nome,
                    "preco": preco_produto.preco,
                    "descricao": preco_produto.descricao,
                    "quantidade": quantidade,
                    "empresa_nome": empresa_mais_proxima.nome,
                    "empresa_id": empresa_mais_proxima.id,
                    "logo_empresa": empresa_mais_proxima.logo or None
                })

                # Reduzir a quantidade restante desse produto
                del produtos_restantes[produto_id]

            # Marcar a empresa como apresentada
            empresa_mais_proxima.empresa_apresentada = True
            empresa_mais_proxima.save()
        else:
            # Se não encontrar nenhuma empresa para os produtos restantes nas empresas não apresentadas,
            # agora buscar nas empresas já apresentadas
            empresas_apresentadas = Empresa.objects.filter(
                endereco__cidade=cliente.endereco.cidade, empresa_apresentada=True
            )

            menor_distancia = None
            empresa_mais_proxima = None
            produtos_encontrados_na_empresa = []

            for empresa in empresas_apresentadas:
                coordenadas_empresa = (float(empresa.endereco.lat), float(empresa.endereco.lon))
                distancia = geodesic(coordenadas_cliente, coordenadas_empresa).km

                # Obter produtos disponíveis com preços definidos para a empresa
                produtos_com_precos = PrecoProdutoEmpresa.objects.filter(
                    empresa=empresa, produto__id__in=produtos_restantes.keys()
                )

                if produtos_com_precos and (menor_distancia is None or distancia < menor_distancia):
                    menor_distancia = distancia
                    empresa_mais_proxima = empresa
                    produtos_encontrados_na_empresa = produtos_com_precos

            if empresa_mais_proxima:
                # Adicionar os produtos encontrados ao resultado final
                for preco_produto in produtos_encontrados_na_empresa:
                    produto_id = preco_produto.produto.id
                    quantidade = produtos_restantes[produto_id]

                    produtos_resultado.append({
                        "produto_id":produto_id,
                        "produto_nome": preco_produto.produto.nome,
                        "preco": preco_produto.preco,
                        "descricao": preco_produto.descricao,
                        "quantidade": quantidade,
                        "empresa_nome": empresa_mais_proxima.nome,
                        "empresa_id": empresa_mais_proxima.id,
                        "logo_empresa": empresa_mais_proxima.logo or None
                    })

                    # Reduzir a quantidade restante desse produto
                    del produtos_restantes[produto_id]

                # Não é necessário marcar a empresa como apresentada novamente, pois já foi
            else:
                # Se não encontrar nenhuma empresa nem nas empresas apresentadas, encerrar a busca
                break

    if produtos_restantes:
        return {
            "error": "Não foi possível encontrar todas as empresas com os produtos solicitados.",
            "produtos_nao_encontrados": list(produtos_restantes.keys()),
        }

    return {"produtos": produtos_resultado}
